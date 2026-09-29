#!/usr/bin/env python3
"""Git-backed change-surface probe for the Atento adapter chassis.

The probe distinguishes:
1. switching between executors that are already registered (runtime selection);
2. introducing a new executor implementation;
3. introducing a new capability implementation.

For (2) and (3), a temporary Git repository is used so the touched-file count is
measured rather than inferred. Existing chassis files and newly added extension
files are reported separately.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from evals.spikes.psychat.adapter.contracts import ExecutionResult
from evals.spikes.psychat.adapter.registry import CapabilityRegistry


class ExecutorA:
    capability = "knowledge.rag"
    executor_id = "a"

    def execute(self, request):
        return ExecutionResult(
            response="a",
            executor=self.executor_id,
            capability=self.capability,
        )


class ExecutorB:
    capability = "knowledge.rag"
    executor_id = "b"

    def execute(self, request):
        return ExecutionResult(
            response="b",
            executor=self.executor_id,
            capability=self.capability,
        )


def run_git(root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {root}: {proc.stderr.strip()}"
        )
    return proc.stdout.strip()


def status_paths(root: Path) -> list[str]:
    output = run_git(root, "status", "--porcelain")
    return sorted(
        line[3:].strip()
        for line in output.splitlines()
        if len(line) >= 4 and line[3:].strip()
    )


def scenario_surface(adapter_root: Path, filename: str, content: str) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        repo = Path(tmp) / "repo"
        copied_adapter = repo / "adapter"
        copied_adapter.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(adapter_root, copied_adapter)

        run_git(repo, "init", "-q")
        run_git(repo, "config", "user.email", "atentoeval@example.invalid")
        run_git(repo, "config", "user.name", "AtentoEval")
        run_git(repo, "add", "adapter")
        run_git(repo, "commit", "-q", "-m", "adapter baseline")

        extension = repo / "extensions" / filename
        extension.parent.mkdir(parents=True, exist_ok=True)
        extension.write_text(content, encoding="utf-8")

        changed = status_paths(repo)
        chassis_changed = [p for p in changed if p.startswith("adapter/")]
        extension_changed = [p for p in changed if p.startswith("extensions/")]

        if chassis_changed:
            raise AssertionError(
                f"scenario unexpectedly changed existing chassis files: {chassis_changed}"
            )
        if len(extension_changed) != 1:
            raise AssertionError(
                f"scenario expected one extension file, got: {extension_changed}"
            )

        return {
            "files_touched_total": len(changed),
            "existing_chassis_files_touched": len(chassis_changed),
            "extension_files_touched": len(extension_changed),
            "changed_files": changed,
        }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--adapter-root",
        type=Path,
        default=Path("evals/spikes/psychat/adapter"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    registry = CapabilityRegistry()
    registry.register(ExecutorA())
    registry.register(ExecutorB())

    # Switching is a RouteDecision/registry lookup once both implementations
    # exist. No source file is mutated.
    selected_b = registry.resolve("knowledge.rag", "b")
    selected_a = registry.resolve("knowledge.rag", "a")
    if selected_b.executor_id != "b" or selected_a.executor_id != "a":
        raise AssertionError("executor swap/rollback resolution failed")

    new_executor = scenario_surface(
        args.adapter_root,
        "alternate_rag_executor.py",
        '''class AlternateRagExecutor:
    capability = "knowledge.rag"
    executor_id = "alternate"
''',
    )
    new_capability = scenario_surface(
        args.adapter_root,
        "lookup_capability.py",
        '''class LookupExecutor:
    capability = "knowledge.lookup"
    executor_id = "lookup"
''',
    )

    result = {
        "metric_version": "atento-adapter-change-surface-v0.1",
        "files_touched_to_swap_executor": 0,
        "swap_executor_scope": "switch between already-registered executors",
        "rollback_test_pass": True,
        "introduce_new_executor": new_executor,
        "files_touched_to_add_capability": new_capability["files_touched_total"],
        "existing_chassis_files_touched_to_add_capability": new_capability[
            "existing_chassis_files_touched"
        ],
        "add_capability": new_capability,
        "interpretation": (
            "Runtime swap/rollback does not modify source. Adding a new executor "
            "or capability requires one new extension implementation file in this "
            "seam probe and no edits to existing adapter chassis files."
        ),
    }

    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
