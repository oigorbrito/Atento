from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATRIX_PATH = ROOT / "evals/config/naia_gate2_composition_v1.json"

COMMON = {"ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6"}

CONFIGS = {
    "AI Butler": "evals/config/naia_gate2_aibutler_v1.json",
    "OpenMausBot": "evals/config/naia_gate2_openmausbot_v1.json",
    "NanoClaw": "evals/config/naia_gate2_nanoclaw_v1.json",
    "AgentOS": "evals/config/naia_gate2_agentos_v1.json",
    "Rome": "evals/config/naia_gate2_rome_v1.json",
    "Suna": "evals/config/naia_gate2_suna_v1.json",
    "Rakazo": "evals/config/naia_gate2_rakazo_v1.json",
    "Letta Code": "evals/config/naia_gate2_letta_code_v1.json",
    "Octop": "evals/config/naia_gate2_octop_v1.json",
    "QwenPaw": "evals/config/naia_gate2_qwenpaw_v1.json",
    "RustFox": "evals/config/naia_gate2_rustfox_v1.json",
    "Engram": "evals/config/naia_gate2_engram_v1.json",
}

ADD_ON_ASSERTIONS = {
    "AI Butler": set(),
    "OpenMausBot": {"SAME-OWNER-ROLE-BOUNDARY"},
    "NanoClaw": {"RECIPE-FREEZE"},
    "AgentOS": {"BROWSER-1"},
    "Rome": {"ACTION-COVERAGE", "PROVIDER-BYPASS"},
    "Suna": {"CONNECTOR-POLICY"},
    "Rakazo": {"CONSEQUENTIAL-RULES"},
    "Letta Code": {"HARDENED-PERMISSION-PROFILE"},
    "Octop": {"AUTH-FAIL-CLOSED", "CRON-CONNECTOR"},
    "QwenPaw": {"SANDBOX-UNAVAILABLE", "CRON-AUTHORITY"},
    "RustFox": {"UNIVERSAL-EFFECT-OWNER"},
    "Engram": {"BROWSER-1", "TRUSTED-RUN-EFFECT"},
}

MATRIX_ADD_ONS = {
    "AI Butler": [],
    "OpenMausBot": ["same_owner_role_boundary"],
    "NanoClaw": ["recipe_freeze"],
    "AgentOS": ["browser_effect_policy"],
    "Rome": ["consequential_action_coverage", "provider_bypass"],
    "Suna": ["connector_policy"],
    "Rakazo": ["consequential_rules"],
    "Letta Code": ["hardened_permission_profile"],
    "Octop": ["authority_fail_closed", "cron_connector_authority"],
    "QwenPaw": ["sandbox_unavailable_fail_closed", "cron_authority"],
    "RustFox": ["universal_effect_owner"],
    "Engram": ["browser_effect_policy", "trusted_run_effect"],
}


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    failures: list[str] = []
    matrix = load(MATRIX_PATH)
    if matrix.get("version") != "NAIA-GATE2-COMPOSITION-V1":
        failures.append("matrix harness version mismatch")

    candidates = matrix.get("candidates")
    if not isinstance(candidates, list) or len(candidates) != 12:
        failures.append(f"matrix candidate count must be 12, got {len(candidates) if isinstance(candidates, list) else 'invalid'}")
        candidates = []

    by_name = {str(row.get("name")): row for row in candidates if isinstance(row, dict)}
    if set(by_name) != set(CONFIGS):
        failures.append(
            f"matrix/config candidate sets differ: matrix={sorted(by_name)} configs={sorted(CONFIGS)}"
        )

    if matrix.get("common_assertions_per_candidate") != 6:
        failures.append("common_assertions_per_candidate must remain 6")
    if matrix.get("common_assertions_total") != 72:
        failures.append("common_assertions_total must remain 72")

    checked: list[dict[str, Any]] = []
    for name, relative in CONFIGS.items():
        path = ROOT / relative
        if not path.exists():
            failures.append(f"{name}: missing frozen config {relative}")
            continue
        cfg = load(path)
        row = by_name.get(name)
        if row is None:
            failures.append(f"{name}: absent from common matrix")
            continue

        expected = {
            "candidate": name,
            "upstream_repo": row.get("repo"),
            "upstream_sha": row.get("sha"),
            "harness_version": matrix.get("version"),
        }
        for key, value in expected.items():
            if cfg.get(key) != value:
                failures.append(f"{name}: {key}={cfg.get(key)!r}, expected {value!r}")

        topology = cfg.get("topology")
        policy = cfg.get("policy")
        if not isinstance(topology, dict) or not topology:
            failures.append(f"{name}: topology missing/empty")
            continue
        if not isinstance(policy, dict) or not policy:
            failures.append(f"{name}: policy missing/empty")
            continue

        profile_hash = canonical_hash(topology)
        policy_hash = canonical_hash(policy)
        if cfg.get("composition_profile_hash") != profile_hash:
            failures.append(
                f"{name}: composition_profile_hash drift: stored={cfg.get('composition_profile_hash')} computed={profile_hash}"
            )
        if cfg.get("policy_hash") != policy_hash:
            failures.append(
                f"{name}: policy_hash drift: stored={cfg.get('policy_hash')} computed={policy_hash}"
            )

        assertions = set(cfg.get("required_assertions") or [])
        expected_assertions = COMMON | ADD_ON_ASSERTIONS[name]
        if assertions != expected_assertions:
            failures.append(
                f"{name}: required_assertions={sorted(assertions)}, expected={sorted(expected_assertions)}"
            )

        if list(row.get("add_ons") or []) != MATRIX_ADD_ONS[name]:
            failures.append(
                f"{name}: common-matrix add-ons changed: {row.get('add_ons')!r}, expected {MATRIX_ADD_ONS[name]!r}"
            )

        checked.append(
            {
                "candidate": name,
                "config": relative,
                "upstream_sha": cfg.get("upstream_sha"),
                "composition_profile_hash": profile_hash,
                "policy_hash": policy_hash,
                "assertions": sorted(assertions),
            }
        )

    summary = {
        "harness_version": matrix.get("version"),
        "candidate_count": len(checked),
        "expected_candidate_count": 12,
        "state": "PASS" if not failures and len(checked) == 12 else "FAIL",
        "failures": failures,
        "checked": checked,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0 if summary["state"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
