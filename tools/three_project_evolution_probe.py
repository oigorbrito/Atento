#!/usr/bin/env python3
"""Probe independent role evolution followed by deterministic re-merge.

This is a topology experiment. It intentionally mutates only role-owned files,
never shared host/runtime files, then checks whether the independently evolved
projects can be reassembled without overlap or boundary violations.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROLES = {
    "naia": ("NAIA", "atento_naia"),
    "anna": ("ANNA", "atento_anna"),
    "apollo": ("APOLLO", "atento_apollo"),
}


def run(*args: str, cwd: Path | None = None) -> str:
    return subprocess.check_output(args, cwd=cwd, text=True).strip()


def call(*args: str, cwd: Path | None = None) -> None:
    subprocess.check_call(args, cwd=cwd)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def tracked_files(root: Path) -> set[str]:
    return {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and ".git" not in p.parts and "__pycache__" not in p.parts and p.name != ".DS_Store"
    }


def main() -> int:
    source = Path.cwd()
    validator = source / "tools/validate_logical_agent_boundaries.py"
    if not validator.is_file():
        raise SystemExit("missing boundary validator")

    result: dict[str, object] = {
        "schema": "atento.independent-evolution-remerge.v1",
        "roles": {},
        "overlap": {},
        "decision": {},
    }

    with tempfile.TemporaryDirectory(prefix="atento-evolution-") as td:
        temp = Path(td)
        extracted = temp / "extracted"
        merged = temp / "merged"
        extracted.mkdir()
        (merged / "agents").mkdir(parents=True)

        changed_global: dict[str, set[str]] = {}

        for slug, (role, package) in ROLES.items():
            src = source / "agents" / slug
            dst = extracted / slug
            shutil.copytree(src, dst)

            call("git", "init", "-q", cwd=dst)
            call("git", "config", "user.email", "topology-probe@atento.invalid", cwd=dst)
            call("git", "config", "user.name", "Atento topology probe", cwd=dst)
            call("git", "add", ".", cwd=dst)
            call("git", "commit", "-q", "-m", "baseline", cwd=dst)
            baseline_commit = run("git", "rev-parse", "HEAD", cwd=dst)

            package_file = dst / package / "__init__.py"
            token = f"{role.lower()}-independent-v2"
            with package_file.open("a", encoding="utf-8") as f:
                f.write(f'\nEVOLUTION_TOKEN = "{token}"\n')

            test_file = dst / "tests" / "test_independent_evolution.py"
            test_file.write_text(
                "from " + package + " import EVOLUTION_TOKEN\n\n"
                "def test_independent_evolution_token():\n"
                f"    assert EVOLUTION_TOKEN == \"{token}\"\n",
                encoding="utf-8",
            )

            call(sys.executable, "-m", "compileall", "-q", ".", cwd=dst)
            call(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v", cwd=dst)

            call("git", "add", ".", cwd=dst)
            call("git", "commit", "-q", "-m", f"{slug}: independent evolution", cwd=dst)
            evolved_commit = run("git", "rev-parse", "HEAD", cwd=dst)
            changed = set(run("git", "diff", "--name-only", baseline_commit, evolved_commit, cwd=dst).splitlines())
            changed.discard("")
            changed_global[slug] = {f"agents/{slug}/{p}" for p in changed}

            # Build independently after evolution.
            dist = dst / "dist"
            call(
                sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "--no-build-isolation", "-w", str(dist),
                cwd=dst,
            )
            wheels = list(dist.glob("*.whl"))
            if len(wheels) != 1:
                raise SystemExit(f"{role}: expected exactly one wheel")

            # Remove generated artifacts before the re-merge.
            shutil.rmtree(dist)
            for cache in list(dst.rglob("__pycache__")):
                shutil.rmtree(cache)
            shutil.rmtree(dst / ".git")

            shutil.copytree(dst, merged / "agents" / slug)

            result["roles"][role] = {
                "baseline_commit": baseline_commit,
                "evolved_commit": evolved_commit,
                "changed_paths": sorted(changed),
                "wheel_built": True,
                "tests_passed": True,
                "package_sha256_after_evolution": sha256(package_file),
            }

        pairs = [("naia", "anna"), ("naia", "apollo"), ("anna", "apollo")]
        collisions = {}
        for a, b in pairs:
            common = sorted(changed_global[a] & changed_global[b])
            collisions[f"{a}:{b}"] = common
        result["overlap"] = {
            "pairwise_changed_path_collisions": collisions,
            "collision_count": sum(len(v) for v in collisions.values()),
        }

        shutil.copy2(validator, merged / "validate.py")
        call(sys.executable, "validate.py", cwd=merged)

        for slug, (_role, _package) in ROLES.items():
            call(sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v", cwd=merged / "agents" / slug)

        result["decision"] = {
            "independent_role_evolution_3_of_3": "PASS",
            "remerge_after_independent_role_changes": "PASS",
            "changed_path_collision_count": result["overlap"]["collision_count"],
            "shared_contract_change_coordination": "NOT_TESTED",
            "hosted_multirepo_operational_cost": "NOT_TESTED",
        }

    Path("artifacts").mkdir(exist_ok=True)
    out = Path("artifacts/independent-evolution-remerge.json")
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
