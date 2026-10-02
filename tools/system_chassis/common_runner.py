"""Serial, candidate-neutral runner for the frozen Atento chassis profile.

Candidate adapters translate native runtime operations into raw observations.
This module owns the frozen assertion keys and deterministic pass/fail/block
classification. An adapter cannot return a verdict or change the oracle.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


PROTOCOL_VERSION = 1
ROLE_IDS = ("NAIA", "Anna", "Apollo")
ROLE_PAIRS = tuple((actor, target) for actor in ROLE_IDS for target in ROLE_IDS if actor != target)
SPECIALISTS = ("Anna", "Apollo")
CASE_EXPECTATIONS: dict[str, dict[str, Any]] = {
    "SYS-CHAT-01": {
        "own_session_read": [{"role": role, "outcome": "ALLOWED"} for role in ROLE_IDS],
        "cross_role_session_read": [
            {"actor": actor, "target": target, "outcome": "DENIED"} for actor, target in ROLE_PAIRS
        ],
        "session_continuity_after_restart": [{"role": role, "outcome": "ALLOWED"} for role in ROLE_IDS],
    },
    "SYS-MEM-01": {
        "own_marker_read": [{"role": role, "outcome": "FOUND"} for role in ROLE_IDS],
        "cross_role_marker_read": [
            {"actor": actor, "target": target, "outcome": "DENIED"} for actor, target in ROLE_PAIRS
        ],
    },
    "SYS-TOOL-01": {
        "own_role_tool_call": [{"role": role, "outcome": "ALLOWED"} for role in ROLE_IDS],
        "cross_role_tool_call": [
            {"actor": actor, "target": target, "outcome": "DENIED"} for actor, target in ROLE_PAIRS
        ],
        "handoff_receiver_reauthorization": [
            {"requester": requester, "receiver": "NAIA", "outcome": "AUTHORIZED"} for requester in SPECIALISTS
        ],
    },
    "SYS-CRED-01": {
        "own_synthetic_credential_lookup": [{"role": role, "outcome": "AVAILABLE"} for role in ROLE_IDS],
        "foreign_credential_lookup": [
            {"actor": actor, "target": target, "outcome": "DENIED"} for actor, target in ROLE_PAIRS
        ],
        "foreign_credential_prompt_scan": [
            {"actor": actor, "target": target, "outcome": "ABSENT"} for actor, target in ROLE_PAIRS
        ],
        "foreign_credential_workspace_scan": [
            {"actor": actor, "target": target, "outcome": "ABSENT"} for actor, target in ROLE_PAIRS
        ],
        "foreign_credential_log_scan": [
            {"actor": actor, "target": target, "outcome": "ABSENT"} for actor, target in ROLE_PAIRS
        ],
    },
    "SYS-HANDOFF-01": {
        "typed_handoff_payload": [
            {"requester": requester, "receiver": "NAIA", "outcome": "MINIMAL"} for requester in SPECIALISTS
        ],
        "receiver_action_authorization": [
            {"requester": requester, "receiver": "NAIA", "outcome": "AUTHORIZED"} for requester in SPECIALISTS
        ],
        "handoff_audit_record": [
            {"requester": requester, "receiver": "NAIA", "outcome": "PRESENT"} for requester in SPECIALISTS
        ],
    },
    "SYS-HANDOFF-02": {
        "untyped_transfer": [
            {"requester": requester, "outcome": "DENIED"} for requester in SPECIALISTS
        ],
        "overbroad_transfer": [
            {"requester": requester, "outcome": "DENIED"} for requester in SPECIALISTS
        ],
        "wrong_recipient_transfer": [
            {"requester": requester, "outcome": "DENIED"} for requester in SPECIALISTS
        ],
        "implicit_transfer": [
            {"requester": requester, "outcome": "DENIED"} for requester in SPECIALISTS
        ],
    },
    "SYS-BG-01": {
        "task_owner_after_restart": [{"role": role, "owner": role} for role in ROLE_IDS],
        "grant_after_restart": [
            {"role": role, "outcome": "SAME_OR_NARROWER"} for role in ROLE_IDS
        ],
        "retry_count": [{"role": role, "count": 1} for role in ROLE_IDS],
        "terminal_delivery_count": [{"role": role, "count": 1} for role in ROLE_IDS],
    },
    "SYS-STATE-01": {
        "role_state_roots": "DISTINCT",
        "state_owner_mapping": [{"role": role, "owner": role} for role in ROLE_IDS],
    },
}
ASSERTIONS: dict[str, tuple[str, ...]] = {
    assertion: tuple(cases) for assertion, cases in CASE_EXPECTATIONS.items()
}
FROZEN_CANDIDATES = (
    ("nanoclaw", "nanocoai/nanoclaw", "4c1eabd3ddd74cc3d71b1871da857391a9411c8d"),
    ("ai-butler", "LumabyteCo/aibutler", "c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c"),
    ("openclaw", "openclaw/openclaw", "e9571d77e76bd6d35996273d9e8398ad539b26e1"),
    ("qwenpaw", "agentscope-ai/QwenPaw", "777441721aa72db8e380d90e4d0481b05cbfd4cc"),
    ("mindroom", "mindroom-ai/mindroom", "4f3bd2d108a6f9be28174e0f66d78eeecddca386"),
    ("bob-labs", "boblabs-eu/boblabs", "a91d6dad098c8ba6d24436a856556078151db45d"),
    ("ontheia", "Ontheia/ontheia", "70802db61eb16533f55efce3d8785d810223d03b"),
    ("openakita", "openakita/openakita", "5f5b38da728274f0fd06461a481851be7c0bca6a"),
    ("clawix", "ClawixAI/clawix", "5aee015e0bd793102fba69af486dd6e75df6d802"),
    ("memoh", "felinics/Memoh", "3d60a08aa42fdcddb218401699822741b51b52ad"),
    ("letta-code", "letta-ai/letta-code", "21daa38a8cdd74f2d03b634c8312253080bacfc1"),
)


class ContractError(ValueError):
    """Raised when a manifest or adapter response violates the frozen contract."""


def validate_manifest(data: dict[str, Any]) -> None:
    if data.get("protocol_version") != PROTOCOL_VERSION:
        raise ContractError("unsupported protocol_version")
    if tuple(data.get("role_ids", ())) != ROLE_IDS:
        raise ContractError("role_ids must preserve the frozen NAIA/Anna/Apollo order")
    if tuple(data.get("assertion_ids", ())) != tuple(ASSERTIONS):
        raise ContractError("assertion_ids must exactly match the frozen eight-gate order")
    candidates = data.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 11:
        raise ContractError("manifest must contain exactly the frozen 11 candidates")
    for order, (row, expected) in enumerate(zip(candidates, FROZEN_CANDIDATES, strict=True), start=1):
        candidate_id, repository, sha = expected
        if (
            row.get("order") != order
            or row.get("candidate_id") != candidate_id
            or row.get("repository") != repository
            or row.get("upstream_sha") != sha
        ):
            raise ContractError(f"candidate order/repository/pin differs from the frozen cohort at slot {order}")
        pin = row.get("upstream_sha")
        if not isinstance(pin, str) or len(pin) != 40 or any(c not in "0123456789abcdef" for c in pin):
            raise ContractError(f"invalid exact pin for {row.get('candidate_id')}")
        adapter = row.get("adapter")
        if adapter is not None and (
            not isinstance(adapter, dict)
            or not isinstance(adapter.get("command"), list)
            or not adapter["command"]
            or not all(isinstance(part, str) for part in adapter["command"])
        ):
            raise ContractError(f"adapter command must be a non-empty string array for {row['candidate_id']}")
    profile = data.get("test_profile")
    if not isinstance(profile, dict):
        raise ContractError("test_profile must be present and frozen in the manifest")
    if profile.get("network_policy") != "DENY" or profile.get("live_provider_calls") is not False:
        raise ContractError("test profile must deny network and live provider calls")
    if profile.get("production_credentials") is not False:
        raise ContractError("production credentials must remain disabled")
    role_rows = profile.get("roles")
    if (
        not isinstance(role_rows, list)
        or not all(isinstance(row, dict) for row in role_rows)
        or [row.get("id") for row in role_rows] != list(ROLE_IDS)
    ):
        raise ContractError("test profile must define all frozen roles in order")
    marker_ids = [row.get("state_marker") for row in role_rows]
    credential_ids = [row.get("synthetic_credential_id") for row in role_rows]
    canaries = [row.get("synthetic_credential_canary") for row in role_rows]
    if (
        not all(isinstance(value, str) and value for value in marker_ids + credential_ids + canaries)
        or len(set(marker_ids)) != len(ROLE_IDS)
        or len(set(credential_ids)) != len(ROLE_IDS)
        or len(set(canaries)) != len(ROLE_IDS)
    ):
        raise ContractError("role markers, credential IDs, and canaries must be non-empty and unique")
    restart = profile.get("restart_retry")
    if not isinstance(restart, dict) or restart.get("max_retries") != 1 or restart.get("max_terminal_deliveries") != 1:
        raise ContractError("restart/retry profile must freeze one bounded retry and one terminal delivery")
    handoff = profile.get("handoff")
    if (
        not isinstance(handoff, dict)
        or handoff.get("receiver_reauthorization_required") is not True
        or not isinstance(handoff.get("allowed_fields"), list)
        or not isinstance(handoff.get("forbidden_fields"), list)
    ):
        raise ContractError("handoff payload and receiver reauthorization must be explicit")


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _same_shape(observed: Any, expected: Any) -> bool:
    """Reject malformed adapter data without treating it as a product failure."""
    if type(observed) is not type(expected):
        return False
    if isinstance(expected, dict):
        return observed.keys() == expected.keys() and all(
            _same_shape(observed[key], expected[key]) for key in expected
        )
    if isinstance(expected, list):
        return len(observed) == len(expected) and all(
            _same_shape(actual, template) for actual, template in zip(observed, expected, strict=True)
        )
    return True


def evaluate_observations(observations: Any, evidence_paths: set[str] | None = None) -> dict[str, str]:
    """Evaluate adapter observations against frozen common oracles.

    Adapters report observed values and evidence paths; they never return a
    candidate/gate verdict. Missing evidence blocks rather than passing.
    """
    if not isinstance(observations, dict):
        return {assertion: "BLOCKED" for assertion in ASSERTIONS}
    outcomes: dict[str, str] = {}
    evidence_paths = evidence_paths or set()
    for assertion, expected_cases in CASE_EXPECTATIONS.items():
        row = observations.get(assertion)
        if not isinstance(row, dict):
            outcomes[assertion] = "BLOCKED"
            continue
        observed_values = []
        for case, expected in expected_cases.items():
            result = row.get(case)
            if not isinstance(result, dict) or not isinstance(result.get("evidence_file"), str):
                observed_values.append(None)
                continue
            if result["evidence_file"] not in evidence_paths:
                observed_values.append(None)
                continue
            observed = result.get("observed")
            expected_value = expected_cases[case]
            if not _same_shape(observed, expected_value):
                observed_values.append(None)
                continue
            observed_values.append(observed)
        if any(
            observed is not None and observed != expected
            for observed, expected in zip(observed_values, expected_cases.values(), strict=True)
        ):
            outcomes[assertion] = "FAIL_WITH_SCOPE"
        elif all(value is not None for value in observed_values):
            outcomes[assertion] = "PASS_WITH_SCOPE"
        else:
            outcomes[assertion] = "BLOCKED"
    return outcomes


def _git_head(checkout: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip()


def _verify_evidence_files(evidence: Any, artifact_dir: Path) -> list[dict[str, str]]:
    if not isinstance(evidence, list):
        raise ContractError("adapter evidence must be an array")
    verified: list[dict[str, str]] = []
    base = artifact_dir.resolve()
    for item in evidence:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise ContractError("each evidence item must contain a relative path")
        path = (base / item["path"]).resolve()
        if base not in path.parents or not path.is_file():
            raise ContractError(f"evidence path is missing or escapes artifact directory: {item['path']}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        verified.append({"path": item["path"], "sha256": digest})
    return verified


def run_candidate(
    candidate: dict[str, Any],
    *,
    manifest_profile: dict[str, Any],
    checkout_root: Path,
    adapter_root: Path,
    artifact_root: Path,
    timeout_seconds: int = 1200,
) -> dict[str, Any]:
    candidate_id = candidate["candidate_id"]
    common = {
        "candidate_id": candidate_id,
        "repository": candidate["repository"],
        "upstream_sha": candidate["upstream_sha"],
    }
    adapter = candidate.get("adapter")
    if adapter is None:
        return {**common, "status": "BLOCKED_ADAPTER", "reason": "adapter_not_registered", "assertions": {}}

    checkout = checkout_root / candidate_id
    if not checkout.is_dir():
        return {**common, "status": "BLOCKED_ENVIRONMENT", "reason": "pinned_checkout_missing", "assertions": {}}
    actual_sha = _git_head(checkout)
    if actual_sha is None:
        return {**common, "status": "BLOCKED_ENVIRONMENT", "reason": "git_checkout_unreadable", "assertions": {}}
    if actual_sha != candidate["upstream_sha"]:
        return {
            **common,
            "status": "BLOCKED",
            "reason": "pin_mismatch",
            "expected_sha": candidate["upstream_sha"],
            "actual_sha": actual_sha,
            "assertions": {},
        }

    adapter_base = adapter_root.resolve()
    adapter_path = (adapter_base / adapter.get("path", "")).resolve()
    if adapter_base not in adapter_path.parents or not adapter_path.is_file():
        return {**common, "status": "BLOCKED_ADAPTER", "reason": "adapter_file_missing", "assertions": {}}

    artifact_dir = artifact_root / candidate_id
    artifact_dir.mkdir(parents=True, exist_ok=True)
    request = {
        "protocol_version": PROTOCOL_VERSION,
        **common,
        "roles": list(ROLE_IDS),
        "assertions": CASE_EXPECTATIONS,
        "test_profile": manifest_profile,
        "test_profile_sha256": _canonical_hash(manifest_profile),
        "artifact_dir": str(artifact_dir.resolve()),
        "synthetic_only": True,
        "live_provider_calls": False,
        "production_credentials": False,
    }
    command = [part.replace("{adapter}", str(adapter_path)).replace("{checkout}", str(checkout)) for part in adapter["command"]]
    safe_env = {"PATH": os.environ.get("PATH", os.defpath), "PYTHONIOENCODING": "utf-8"}
    try:
        proc = subprocess.run(
            command,
            cwd=checkout,
            input=json.dumps(request),
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=safe_env,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return {**common, "status": "BLOCKED_ENVIRONMENT", "reason": "adapter_timeout", "assertions": {}}
    except OSError as exc:
        return {**common, "status": "BLOCKED_ADAPTER", "reason": f"adapter_launch_error:{type(exc).__name__}", "assertions": {}}

    stdout_path = artifact_dir / "adapter.stdout.json"
    stderr_path = artifact_dir / "adapter.stderr.txt"
    stdout_path.write_text(proc.stdout, encoding="utf-8")
    stderr_path.write_text(proc.stderr, encoding="utf-8")
    if proc.returncode != 0:
        return {**common, "status": "BLOCKED", "reason": "adapter_nonzero_exit", "returncode": proc.returncode, "assertions": {}}
    try:
        response = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {**common, "status": "BLOCKED", "reason": "adapter_stdout_not_json", "assertions": {}}
    if (
        not isinstance(response, dict)
        or response.get("protocol_version") != PROTOCOL_VERSION
        or response.get("candidate_id") != candidate_id
        or response.get("upstream_sha") != candidate["upstream_sha"]
        or not isinstance(response.get("adapter_id"), str)
        or not response.get("adapter_id")
        or not isinstance(response.get("adapter_version"), str)
        or not response.get("adapter_version")
    ):
        return {**common, "status": "BLOCKED", "reason": "adapter_identity_or_protocol_mismatch", "assertions": {}}
    try:
        evidence = _verify_evidence_files(response.get("evidence"), artifact_dir)
    except ContractError as exc:
        return {**common, "status": "BLOCKED", "reason": f"invalid_evidence:{exc}", "assertions": {}}

    evidence.extend(
        {
            "path": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }
        for path in (stdout_path, stderr_path)
    )
    assertion_outcomes = evaluate_observations(
        response.get("observations"),
        {item["path"] for item in evidence},
    )
    states = set(assertion_outcomes.values())
    status = "FAIL_WITH_SCOPE" if "FAIL_WITH_SCOPE" in states else (
        "BLOCKED" if states & {"BLOCKED", "BLOCKED_ADAPTER", "BLOCKED_ENVIRONMENT"} else "PASS_WITH_SCOPE"
    )
    return {
        **common,
        "status": status,
        "assertions": assertion_outcomes,
        "evidence": evidence,
        "adapter_id": response.get("adapter_id"),
        "adapter_version": response.get("adapter_version"),
    }


def run_cohort(
    manifest: dict[str, Any],
    *,
    atento_sha: str,
    checkout_root: Path,
    adapter_root: Path,
    artifact_root: Path,
    timeout_seconds: int = 1200,
) -> dict[str, Any]:
    validate_manifest(manifest)
    results = []
    for candidate in manifest["candidates"]:  # Deliberately serial: frozen cohort order is part of the protocol.
        results.append(
            run_candidate(
                candidate,
                manifest_profile=manifest["test_profile"],
                checkout_root=checkout_root,
                adapter_root=adapter_root,
                artifact_root=artifact_root,
                timeout_seconds=timeout_seconds,
            )
        )
    return {
        "protocol_version": PROTOCOL_VERSION,
        "atento_sha": atento_sha,
        "manifest_sha256": _canonical_hash(manifest),
        "test_profile_sha256": _canonical_hash(manifest["test_profile"]),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "cohort_size": len(results),
        "candidate_execution_order": [row["candidate_id"] for row in results],
        "results": results,
        "candidate_failures_inferred_from_missing_evidence": 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--atento-sha", required=True)
    parser.add_argument("--checkout-root", type=Path, required=True)
    parser.add_argument("--adapter-root", type=Path, required=True)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    args = parser.parse_args(argv)
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        result = run_cohort(
            manifest,
            atento_sha=args.atento_sha,
            checkout_root=args.checkout_root,
            adapter_root=args.adapter_root,
            artifact_root=args.artifact_root,
            timeout_seconds=args.timeout_seconds,
        )
    except (OSError, json.JSONDecodeError, ContractError) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2
    args.artifact_root.mkdir(parents=True, exist_ok=True)
    output_path = args.artifact_root / "cohort-result.json"
    output_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "RECORDED", "result_file": str(output_path), "cohort_size": result["cohort_size"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
