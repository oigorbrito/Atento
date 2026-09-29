#!/usr/bin/env python3
"""Validate and measure the concrete minimal PsyChat fork patch."""
from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path


EXPECTED_FILES = {
    "agent/psychology_agent.py",
    "core/model_gateway.py",
    "core/rag_system.py",
}


def git(root: Path, *args: str) -> str:
    p = subprocess.run(["git", "-C", str(root), *args], text=True, capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()


def parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def requests_post_files(root: Path) -> list[str]:
    found = []
    for rel in EXPECTED_FILES:
        path = root / rel
        if not path.exists():
            continue
        tree = parse(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if (
                node.func.attr == "post"
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "requests"
            ):
                found.append(rel)
                break
    return sorted(found)


def has_optional_gateway_constructor(path: Path, class_name: str) -> bool:
    tree = parse(path)
    for node in tree.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "__init__":
                    return any(arg.arg == "model_gateway" for arg in item.args.args)
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.donor_root

    subprocess.run(
        ["python", "-m", "compileall", "-q", str(root / "agent"), str(root / "core")],
        check=True,
    )

    changed = {
        line.strip()
        for line in git(root, "status", "--porcelain").splitlines()
        if line.strip()
        for line in [line[3:]]
    }
    if changed != EXPECTED_FILES:
        raise AssertionError(f"unexpected patch surface: {sorted(changed)}")

    direct = requests_post_files(root)
    if direct != ["core/model_gateway.py"]:
        raise AssertionError(f"provider bypass remains outside gateway: {direct}")

    if not has_optional_gateway_constructor(root / "core/rag_system.py", "RAGSystem"):
        raise AssertionError("RAGSystem does not expose model_gateway injection")
    if not has_optional_gateway_constructor(root / "agent/psychology_agent.py", "PsychologyAgent"):
        raise AssertionError("PsychologyAgent does not expose model_gateway injection")

    result = {
        "metric_version": "psychat-minimal-fork-v0.1",
        "changed_files": sorted(changed),
        "files_touched_to_swap_provider": len(changed),
        "direct_requests_post_files_in_patch_surface": direct,
        "provider_calls_centralized": True,
        "rag_system_gateway_injectable": True,
        "psychology_agent_gateway_injectable": True,
        "compileall_passed": True,
        "measurement": "git status --porcelain against pinned donor working tree",
    }
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
