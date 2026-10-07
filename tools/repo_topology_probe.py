#!/usr/bin/env python3
"""Empirical monorepo-vs-multirepo separability probe for Atento.

The probe does not score repository topology by preference. It checks whether the
current tree contains the minimum evidence needed to extract NAIA, Anna and Apollo
as independently buildable/testable projects without first inventing new seams.
"""

from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path

ROLES = ("NAIA", "ANNA", "APOLLO")
MARKERS = {
    "NAIA": re.compile(r"(^|[/_.-])naia([/_.-]|$)", re.I),
    "ANNA": re.compile(r"(^|[/_.-])anna([/_.-]|$)", re.I),
    "APOLLO": re.compile(r"(^|[/_.-])apollo([/_.-]|$)", re.I),
}
BUILD_MANIFESTS = {
    "pyproject.toml", "package.json", "requirements.txt", "setup.py",
    "Cargo.toml", "go.mod", "pom.xml", "build.gradle", "Dockerfile",
}
CODE_SUFFIXES = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".go", ".rs",
    ".java", ".kt", ".sh", ".sql", ".yaml", ".yml", ".json",
}
DOC_PREFIXES = ("docs/",)
SHARED_IMPLEMENTATION_PREFIXES = ("services/", "tools/", "evals/")


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True)


def role_for_path(path: str) -> set[str]:
    return {role for role, pattern in MARKERS.items() if pattern.search(path)}


def is_code(path: str) -> bool:
    p = Path(path)
    if path.startswith(DOC_PREFIXES):
        return False
    if p.name in BUILD_MANIFESTS:
        return True
    return p.suffix.lower() in CODE_SUFFIXES


def parent_has_role(path: str, role: str) -> bool:
    parts = [part.lower() for part in Path(path).parts[:-1]]
    return role.lower() in parts


def cross_role_reference(path: str, text: str, own_roles: set[str]) -> list[str]:
    hits = []
    for role in ROLES:
        if role not in own_roles and re.search(rf"\b{role}\b", text, re.I):
            hits.append(role)
    return hits


def history_metrics() -> dict:
    raw = git("log", "--format=@@%H", "--name-only", "--no-renames")
    commits: list[set[str]] = []
    current: set[str] | None = None
    for line in raw.splitlines():
        if line.startswith("@@"):
            if current is not None:
                commits.append(current)
            current = set()
            continue
        if current is not None and line.strip():
            current.update(role_for_path(line.strip()))
    if current is not None:
        commits.append(current)

    role_touch = Counter()
    multi_role = 0
    all_three = 0
    for roles in commits:
        for role in roles:
            role_touch[role] += 1
        if len(roles) >= 2:
            multi_role += 1
        if len(roles) == 3:
            all_three += 1
    role_commits = sum(1 for roles in commits if roles)
    return {
        "commits_total": len(commits),
        "commits_touching_role_named_paths": role_commits,
        "commits_touching_2plus_roles": multi_role,
        "commits_touching_all_3_roles": all_three,
        "per_role_commits": dict(role_touch),
        "multi_role_ratio_among_role_commits": (
            round(multi_role / role_commits, 4) if role_commits else None
        ),
    }


def main() -> int:
    files = [line for line in git("ls-files").splitlines() if line.strip()]

    role_named_files: dict[str, list[str]] = {role: [] for role in ROLES}
    role_code_files: dict[str, list[str]] = {role: [] for role in ROLES}
    role_manifests: dict[str, list[str]] = {role: [] for role in ROLES}
    role_tests: dict[str, list[str]] = {role: [] for role in ROLES}
    direct_cross_role_refs: list[dict] = []

    for path in files:
        roles = role_for_path(path)
        for role in roles:
            role_named_files[role].append(path)
            if is_code(path):
                role_code_files[role].append(path)
            if Path(path).name in BUILD_MANIFESTS and parent_has_role(path, role):
                role_manifests[role].append(path)
            low = path.lower()
            if parent_has_role(path, role) and (
                "/test" in low or "/tests/" in low or low.endswith("_test.py")
                or ".test." in low or ".spec." in low
            ):
                role_tests[role].append(path)

        if roles and is_code(path):
            try:
                text = Path(path).read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            refs = cross_role_reference(path, text, roles)
            if refs:
                direct_cross_role_refs.append(
                    {"path": path, "own_roles": sorted(roles), "references": refs}
                )

    shared_impl = [
        path for path in files
        if is_code(path)
        and path.startswith(SHARED_IMPLEMENTATION_PREFIXES)
        and not role_for_path(path)
    ]

    per_role = {}
    necessary_conditions = {}
    for role in ROLES:
        per_role[role] = {
            "role_named_files": len(role_named_files[role]),
            "role_named_code_files": len(role_code_files[role]),
            "independent_build_manifests": role_manifests[role],
            "independent_test_files": role_tests[role],
        }
        necessary_conditions[role] = {
            "has_role_specific_code": bool(role_code_files[role]),
            "has_independent_build_manifest": bool(role_manifests[role]),
            "has_independent_tests": bool(role_tests[role]),
        }

    conditions = [v for role in ROLES for v in necessary_conditions[role].values()]
    physical_split_ready = all(conditions) and not direct_cross_role_refs

    result = {
        "schema": "atento.repo-topology-separability.v1",
        "method": {
            "decision_rule": (
                "Physical split is eligible only if each role already has role-specific "
                "code, its own build manifest, its own tests, and no direct cross-role "
                "references in role-specific code. Missing evidence => NOT_PROVEN."
            ),
            "note": (
                "This is a necessary-condition probe, not a universal claim that monorepo "
                "or multirepo is superior."
            ),
        },
        "tree": {
            "tracked_files": len(files),
            "shared_implementation_files": len(shared_impl),
            "per_role": per_role,
            "direct_cross_role_reference_count": len(direct_cross_role_refs),
            "direct_cross_role_references": direct_cross_role_refs[:50],
        },
        "history": history_metrics(),
        "necessary_conditions": necessary_conditions,
        "decision": {
            "physical_three_repo_split": (
                "ELIGIBLE_FOR_EXTRACTION_EXPERIMENT"
                if physical_split_ready
                else "NOT_PROVEN"
            ),
            "logical_bounded_contexts_in_one_repo": (
                "TESTABLE_NOW" if any(role_named_files[r] for r in ROLES) else "NOT_PROVEN"
            ),
            "reason": (
                "All necessary extraction conditions are present."
                if physical_split_ready
                else "At least one role lacks already-existing independent code/build/test evidence or cross-role references remain."
            ),
        },
    }

    Path("artifacts").mkdir(exist_ok=True)
    out = Path("artifacts/repo-topology-separability.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
