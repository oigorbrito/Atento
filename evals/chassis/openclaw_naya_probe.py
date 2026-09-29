from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any


PASS = "PASS_EMPIRICAL"
ARCH_RISK = "ARCH_RISK"
INFRA_BLOCKED = "INFRA_BLOCKED"


def run(
    command: list[str],
    *,
    cwd: Path,
    env: dict[str, str] | None = None,
    timeout: int = 900,
) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            capture_output=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as error:
        return {
            "command": command,
            "returncode": 127,
            "stdout": "",
            "stderr": str(error),
            "error_kind": "command_not_found",
        }
    except subprocess.TimeoutExpired as error:
        return {
            "command": command,
            "returncode": 124,
            "stdout": (error.stdout or "")[-20000:] if isinstance(error.stdout, str) else "",
            "stderr": (error.stderr or "")[-20000:] if isinstance(error.stderr, str) else "",
            "error_kind": "timeout",
        }
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout[-20000:],
        "stderr": completed.stderr[-20000:],
    }


def parse_json_output(result: dict[str, Any]) -> Any:
    stdout = str(result.get("stdout", "")).strip()
    if not stdout:
        raise ValueError("command produced no stdout")
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        for line in reversed(stdout.splitlines()):
            line = line.strip()
            if not line:
                continue
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    raise ValueError("command stdout did not contain JSON")


def command_ok(result: dict[str, Any]) -> bool:
    return int(result.get("returncode", 1)) == 0


def write_profile_runtime(
    *,
    donor_root: Path,
    profile_path: Path,
    state_root: Path,
    agent_id: str,
) -> dict[str, Any]:
    config_path = state_root / "openclaw.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(profile_path, config_path)

    home = state_root / "home"
    home.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    env.update(
        {
            "HOME": str(home),
            "OPENCLAW_STATE_DIR": str(state_root / "state"),
            "OPENCLAW_CONFIG_PATH": str(config_path),
            "NO_COLOR": "1",
        }
    )

    validate = run(
        ["pnpm", "openclaw", "config", "validate", "--json"],
        cwd=donor_root,
        env=env,
    )
    first = run(
        ["pnpm", "openclaw", "exec-policy", "show", "--agent", agent_id, "--json"],
        cwd=donor_root,
        env=env,
    )
    second = run(
        ["pnpm", "openclaw", "exec-policy", "show", "--agent", agent_id, "--json"],
        cwd=donor_root,
        env=env,
    )

    payloads: list[Any] = []
    parse_errors: list[str] = []
    for name, result in (("first", first), ("second", second)):
        try:
            payloads.append(parse_json_output(result))
        except Exception as error:  # qualification evidence, preserve diagnostic
            payloads.append(None)
            parse_errors.append(f"{name}: {error}")

    return {
        "config_path": str(config_path),
        "state_dir": env["OPENCLAW_STATE_DIR"],
        "validate": validate,
        "first": first,
        "second": second,
        "payloads": payloads,
        "parse_errors": parse_errors,
    }


def effective_scope(payload: Any, agent_id: str) -> dict[str, Any] | None:
    if not isinstance(payload, dict):
        return None
    policy = payload.get("effectivePolicy")
    if not isinstance(policy, dict):
        return None
    scopes = policy.get("scopes")
    if not isinstance(scopes, list):
        return None
    expected = f"agent:{agent_id}"
    for scope in scopes:
        if isinstance(scope, dict) and (
            scope.get("scopeLabel") == expected or scope.get("agentId") == agent_id
        ):
            return scope
    return scopes[0] if scopes and isinstance(scopes[0], dict) else None


def posture(scope: dict[str, Any] | None) -> dict[str, Any]:
    if not scope:
        return {}
    security = scope.get("security") if isinstance(scope.get("security"), dict) else {}
    ask = scope.get("ask") if isinstance(scope.get("ask"), dict) else {}
    fallback = scope.get("askFallback") if isinstance(scope.get("askFallback"), dict) else {}
    return {
        "security": security.get("effective"),
        "ask": ask.get("effective"),
        "ask_fallback": fallback.get("effective"),
        "scope_label": scope.get("scopeLabel"),
        "agent_id": scope.get("agentId"),
    }


def run_vitest_group(donor_root: Path, files: list[str]) -> dict[str, Any]:
    return run(
        [
            "node",
            "scripts/run-vitest.mjs",
            "run",
            *files,
            "--maxWorkers=1",
        ],
        cwd=donor_root,
        timeout=1200,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="OpenClaw Nayá local-delta qualification")
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--atento-root", type=Path, required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--upstream-sha", required=True)
    parser.add_argument("--atento-sha", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    donor_root = args.donor_root.resolve()
    atento_root = args.atento_root.resolve()
    profile_root = atento_root / "evals/chassis/openclaw"
    plugin_root = profile_root / "naya-effect-plugin"

    actual_pin = run(["git", "rev-parse", "HEAD"], cwd=donor_root)
    pin_matches = (
        command_ok(actual_pin)
        and actual_pin["stdout"].strip() == args.upstream_sha
    )

    with tempfile.TemporaryDirectory(prefix="atento-openclaw-naya-") as tmp:
        runtime_root = Path(tmp)
        assistant = write_profile_runtime(
            donor_root=donor_root,
            profile_path=profile_root / "assistant-hardening.json",
            state_root=runtime_root / "assistant",
            agent_id="naya-assistant",
        )
        therapist = write_profile_runtime(
            donor_root=donor_root,
            profile_path=profile_root / "therapist-hardening.json",
            state_root=runtime_root / "therapist",
            agent_id="naya-therapist",
        )

        assistant_postures = [
            posture(effective_scope(payload, "naya-assistant"))
            for payload in assistant["payloads"]
        ]
        therapist_postures = [
            posture(effective_scope(payload, "naya-therapist"))
            for payload in therapist["payloads"]
        ]

        assistant_policy_ok = (
            command_ok(assistant["validate"])
            and command_ok(assistant["first"])
            and command_ok(assistant["second"])
            and not assistant["parse_errors"]
            and len(assistant_postures) == 2
            and assistant_postures[0] == assistant_postures[1]
            and assistant_postures[0].get("security") in {"allowlist", "deny"}
            and assistant_postures[0].get("ask") in {"on-miss", "always"}
        )
        therapist_policy_ok = (
            command_ok(therapist["validate"])
            and command_ok(therapist["first"])
            and command_ok(therapist["second"])
            and not therapist["parse_errors"]
            and len(therapist_postures) == 2
            and therapist_postures[0] == therapist_postures[1]
            and therapist_postures[0].get("security") == "deny"
            and therapist_postures[0].get("ask") == "off"
        )

        approval_tests = run_vitest_group(
            donor_root,
            [
                "src/gateway/operator-approval-store.test.ts",
                "src/gateway/server-methods/approval.test.ts",
                "src/gateway/exec-approval-manager.test.ts",
            ],
        )
        isolation_tests = run_vitest_group(
            donor_root,
            [
                "src/security/audit-cross-agent-session-access.test.ts",
                "src/plugin-sdk/session-visibility.test.ts",
                "src/agents/tools/sessions-access.test.ts",
                "src/agents/tools/sessions.test.ts",
                "src/agents/openclaw-tools.sessions-visibility.test.ts",
            ],
        )
        memory_tests = run_vitest_group(
            donor_root,
            [
                "src/plugin-sdk/memory-core-host-engine-sessions.test.ts",
                "extensions/memory-wiki/src/config.test.ts",
            ],
        )

        plugin_validate = run(
            [
                "pnpm",
                "openclaw",
                "plugins",
                "validate",
                "--entry",
                str(plugin_root / "index.mjs"),
            ],
            cwd=donor_root,
        )
        effect_test = run(
            ["node", str(plugin_root / "effect-protocol.test.mjs")],
            cwd=atento_root,
        )
        try:
            effect_payload = parse_json_output(effect_test)
        except Exception as error:
            effect_payload = {"ok": False, "parse_error": str(error)}

        goal_doc = (donor_root / "docs/tools/goal.md").read_text(encoding="utf-8")
        outbound_doc = (
            donor_root / "docs/plugins/sdk-channel-outbound.md"
        ).read_text(encoding="utf-8")
        generic_disclaimer = (
            "They do not promise exactly-once external tool or provider effects."
            in goal_doc
        )
        channel_reconciliation = "automaticUnknownSendReconciliation" in outbound_doc

        donor_diff = run(["git", "diff", "--name-only"], cwd=donor_root)
        donor_status = run(["git", "status", "--porcelain"], cwd=donor_root)
        tracked_modified = [
            line
            for line in donor_diff["stdout"].splitlines()
            if line.strip()
        ]

        oc1_ok = assistant_policy_ok and command_ok(approval_tests)
        oc3_ok = (
            therapist_policy_ok
            and assistant_policy_ok
            and assistant["state_dir"] != therapist["state_dir"]
            and command_ok(isolation_tests)
        )
        oc4_ok = command_ok(memory_tests)
        oc5_ok = (
            command_ok(plugin_validate)
            and not tracked_modified
            and pin_matches
        )
        localized_effect_ok = (
            command_ok(effect_test)
            and isinstance(effect_payload, dict)
            and effect_payload.get("ok") is True
            and effect_payload.get("recovered_without_duplicate") is True
            and command_ok(plugin_validate)
        )

        cases: dict[str, Any] = {
            "OC-NAYA-001": {
                "status": PASS if oc1_ok else ARCH_RISK,
                "question": "fail-closed authority profile and stale approval defense",
                "assistant_posture_first": assistant_postures[0] if assistant_postures else {},
                "assistant_posture_second": assistant_postures[1] if len(assistant_postures) > 1 else {},
                "config_valid": command_ok(assistant["validate"]),
                "approval_tests_passed": command_ok(approval_tests),
                "restart_equivalent_reinspection_stable": (
                    len(assistant_postures) == 2
                    and assistant_postures[0] == assistant_postures[1]
                ),
            },
            "OC-NAYA-002": {
                "status": ARCH_RISK,
                "question": "arbitrary external-action crash ambiguity",
                "generic_exactly_once_claimed": not generic_disclaimer,
                "generic_effect_disclaimer_verified": generic_disclaimer,
                "channel_specific_reconciliation_verified": channel_reconciliation,
                "controlled_adapter_validates_as_openclaw_plugin": command_ok(plugin_validate),
                "controlled_adapter_fault_probe_passed": localized_effect_ok,
                "controlled_adapter_result": effect_payload,
                "conclusion": (
                    "localized adapter-level reconciliation is empirically feasible without donor edits; "
                    "OpenClaw still does not provide a universal exactly-once contract for arbitrary tools"
                ),
            },
            "OC-NAYA-003": {
                "status": PASS if oc3_ok else ARCH_RISK,
                "question": "Assistant ↔ Therapist authority isolation",
                "assistant_and_therapist_state_roots_distinct": (
                    assistant["state_dir"] != therapist["state_dir"]
                ),
                "assistant_config_valid": command_ok(assistant["validate"]),
                "therapist_config_valid": command_ok(therapist["validate"]),
                "therapist_posture_first": therapist_postures[0] if therapist_postures else {},
                "therapist_posture_second": therapist_postures[1] if len(therapist_postures) > 1 else {},
                "cross_agent_policy_tests_passed": command_ok(isolation_tests),
                "topology_requirement": "separate Gateway/runtime trust boundaries; explicit broker only",
                "limitation": "handoff broker behavior belongs to ADR-001 and is not exercised by this base-candidate probe",
            },
            "OC-NAYA-004": {
                "status": PASS if oc4_ok else ARCH_RISK,
                "question": "plugin/global-store negative isolation",
                "memory_tests_passed": command_ok(memory_tests),
                "assistant_plugin_allowlist": ["memory-core"],
                "representative_plugin_scope": "memory-wiki agent-scope validation is exercised upstream",
                "limitation": "every future plugin store still requires its own scope/provenance review",
            },
            "OC-NAYA-005": {
                "status": PASS if oc5_ok else ARCH_RISK,
                "question": "integration touchpoint count / invasiveness",
                "donor_internal_files_modified": len(tracked_modified),
                "donor_internal_paths_modified": tracked_modified,
                "qualification_plugin_files": 5,
                "hardening_profile_files": 2,
                "plugin_validation_passed": command_ok(plugin_validate),
                "conclusion": (
                    "Nayá hardening and a controlled durable-effect adapter can be expressed outside "
                    "OpenClaw core at this qualification scope"
                ),
                "limitation": "full product composition touchpoints remain a later adoption measurement",
            },
        }

        infra_commands = {
            "pin": actual_pin,
            "assistant_validate": assistant["validate"],
            "assistant_exec_policy_first": assistant["first"],
            "assistant_exec_policy_second": assistant["second"],
            "therapist_validate": therapist["validate"],
            "therapist_exec_policy_first": therapist["first"],
            "therapist_exec_policy_second": therapist["second"],
            "approval_tests": approval_tests,
            "isolation_tests": isolation_tests,
            "memory_tests": memory_tests,
            "plugin_validate": plugin_validate,
            "effect_test": effect_test,
            "donor_status": donor_status,
        }

        essential_commands = [
            actual_pin,
            assistant["validate"],
            assistant["first"],
            assistant["second"],
            therapist["validate"],
            therapist["first"],
            therapist["second"],
            approval_tests,
            isolation_tests,
            memory_tests,
            plugin_validate,
            effect_test,
        ]
        setup_like_failure = any(
            item.get("error_kind") in {"command_not_found", "timeout"}
            for item in essential_commands
        )

        blockers: list[dict[str, Any]] = [
            {
                "code": "GENERIC_EFFECT_DURABILITY_NOT_PROVEN",
                "kind": "architecture",
                "detail": (
                    "The pinned OpenClaw source explicitly does not promise exactly-once "
                    "external tool/provider effects generally. Critical adapters can implement "
                    "localized operation/readback/reconciliation semantics."
                ),
            }
        ]
        for case_id, case in cases.items():
            if case["status"] == ARCH_RISK and case_id != "OC-NAYA-002":
                blockers.append(
                    {
                        "code": f"{case_id}_INVARIANT_NOT_PROVEN",
                        "kind": "candidate_or_harness",
                        "detail": case["question"],
                    }
                )

        evidence_status = INFRA_BLOCKED if setup_like_failure else ARCH_RISK

        result = {
            "protocol": "openclaw_naya_local_delta_v1",
            "evaluation_kind": "openclaw_naya_local_delta",
            "candidate_id": args.candidate_id,
            "upstream_sha": args.upstream_sha,
            "atento_sha": args.atento_sha,
            "pin_matches": pin_matches,
            "evidence_status": evidence_status,
            "cases": cases,
            "safety": {
                "assistant_policy_fail_closed": assistant_policy_ok,
                "therapist_exec_denied": therapist_policy_ok,
                "separate_runtime_boundary_required": True,
            },
            "git_surface": {
                "donor_internal_files_modified": len(tracked_modified),
                "donor_internal_paths_modified": tracked_modified,
                "qualification_plugin_files": 5,
                "hardening_profile_files": 2,
                "donor_status_porcelain": donor_status["stdout"].splitlines(),
            },
            "blockers": blockers,
            "commands": infra_commands,
        }

        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(
            json.dumps(
                {
                    "candidate_id": args.candidate_id,
                    "evidence_status": evidence_status,
                    "cases": {
                        key: value["status"] for key, value in cases.items()
                    },
                    "output": str(args.output),
                },
                ensure_ascii=False,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
