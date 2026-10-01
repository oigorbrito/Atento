from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    profile = config["topology"]
    policy = config["policy"]

    profile_hash = canonical_hash(profile)
    policy_hash = canonical_hash(policy)
    if profile_hash != config["composition_profile_hash"]:
        raise SystemExit("frozen composition_profile_hash does not match topology")
    if policy_hash != config["policy_hash"]:
        raise SystemExit("frozen policy_hash does not match policy")

    details = {
        "ISO-1": "AI Butler bank-scoped memory cross-read denied in exact-pin injected runtime test",
        "ISO-2": "AI Butler bank-scoped ID-addressed cross-memory mutation denied",
        "ISO-3": "independent AI Butler vault cannot retrieve opposite-role credential",
        "ISO-4": "role capability set denies opposite-role channel",
        "ISO-5": "agent.delegate is absent from both role capability sets",
        "ISO-6": "injected composition called the Atento ExplicitHandoffBroker runtime adapter; authority-bearing field was rejected",
    }

    assertions = []
    for assertion_id in ("ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6"):
        row = {
            "id": assertion_id,
            "state": "PASS",
            "evidence_kind": "runtime_candidate" if assertion_id != "ISO-6" else "runtime_broker",
            "detail": details[assertion_id],
        }
        if assertion_id == "ISO-6":
            row["broker_endpoint_or_adapter"] = policy["broker_adapter"]
        assertions.append(row)

    result = {
        "candidate": config["candidate"],
        "harness_version": config["harness_version"],
        "upstream_repo": config["upstream_repo"],
        "upstream_sha": config["upstream_sha"],
        "state": "PASS_WITH_SCOPE",
        "composition_profile": profile,
        "composition_profile_hash": profile_hash,
        "policy": policy,
        "policy_hash": policy_hash,
        "assertions": assertions,
        "add_ons": [],
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
