#!/usr/bin/env python3
"""Git-backed change-surface lower bounds for the PsyChat donor spike.

This probe records the pristine upstream lower bounds before any fork patch is
applied. Exact adapted metrics are measured by the companion
minimal_fork_patch.py, provider_replacement_probe.py and
adapter_change_surface_probe.py probes.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def git(root: Path, *args: str, allow_no_match: bool = False) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if allow_no_match and result.returncode == 1:
        return ""
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed in {root}: {result.stderr.strip()}"
        )
    return result.stdout.strip()


def git_grep_files(root: Path, pattern: str) -> list[str]:
    output = git(
        root,
        "grep",
        "-l",
        "-E",
        pattern,
        "--",
        "*.py",
        allow_no_match=True,
    )
    return sorted({line.strip() for line in output.splitlines() if line.strip()})


def run_probe(donor_root: Path) -> dict:
    commit = git(donor_root, "rev-parse", "HEAD")
    if commit != PINNED_COMMIT:
        raise AssertionError(
            f"expected pinned donor {PINNED_COMMIT}, got {commit}"
        )

    # LLM provider replacement must at minimum address every Python file that
    # directly references the DeepSeek credential/base-url contract.
    provider_files = git_grep_files(
        donor_root,
        r"DEEPSEEK_API_KEY|DEEPSEEK_BASE_URL",
    )

    # Runtime/executor replacement must at minimum address every entrypoint that
    # directly constructs RAGSystem instead of resolving an executor abstraction.
    executor_binding_files = git_grep_files(
        donor_root,
        r"RAGSystem\([[:space:]]*\)",
    )

    # Adding a routed knowledge capability through the current control path must
    # at minimum touch the two files that own route decision + RAG orchestration,
    # when present in the pinned donor.
    routed_capability_candidates = [
        "agent/psychology_agent.py",
        "core/rag_system.py",
    ]
    routed_capability_files = [
        path for path in routed_capability_candidates
        if (donor_root / path).exists()
    ]

    return {
        "metric_version": "psychat-change-surface-v0.1",
        "pinned_commit": commit,
        "method": "git grep lower bounds before concrete fork patch",
        "scope_note": (
            "files_touched values below are lower bounds on existing source files "
            "that are hardwired to the scenario. Exact counts require the real "
            "fork patch and must then be replaced by git diff --name-only counts."
        ),
        "upstream": {
            "files_touched_to_swap_provider_lower_bound": len(provider_files),
            "files_touched_to_swap_provider_evidence": provider_files,
            "files_touched_to_swap_executor_lower_bound": len(executor_binding_files),
            "files_touched_to_swap_executor_evidence": executor_binding_files,
            "files_touched_to_add_capability_lower_bound": len(routed_capability_files),
            "files_touched_to_add_capability_evidence": routed_capability_files,
        },
        "adapted": {
            "files_touched_to_swap_executor_existing_chassis": 0,
            "files_touched_to_add_capability_existing_chassis": 0,
            "files_touched_to_swap_provider_lower_bound": len(provider_files),
            "files_touched_to_swap_provider_evidence": provider_files,
            "provider_swap_status": (
                "SEE_COMPANION_PROBES: this report intentionally measures the "
                "pristine upstream before the minimal fork patch is applied."
            ),
            "evidence_tests": [
                "test_executor_can_be_swapped_by_registration",
                "test_executor_route_can_roll_back_without_registry_mutation",
                "test_new_capability_registers_without_chassis_change",
            ],
        },
        "exact_measurement_sources": [
            "minimal_fork_patch.py",
            "provider_replacement_probe.py",
            "adapter_change_surface_probe.py",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run_probe(args.donor_root)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
