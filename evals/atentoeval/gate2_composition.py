from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Sequence

HARNESS_VERSION = "NAIA-GATE2-COMPOSITION-V1"

COMMON_ASSERTIONS: Sequence[str] = (
    "ISO-1",
    "ISO-2",
    "ISO-3",
    "ISO-4",
    "ISO-5",
    "ISO-6",
)

VALID_ASSERTION_STATES = {"PASS", "FAIL", "BLOCKED", "INVALID"}
VALID_RESULT_STATES = {
    "PASS_WITH_SCOPE",
    "FAIL_LOCALIZED",
    "FAIL_STRUCTURAL",
    "BLOCKED_ENVIRONMENT",
    "INVALID_EVIDENCE",
}


@dataclass(frozen=True)
class AssertionRecord:
    assertion_id: str
    state: str
    detail: str = ""
    repair_class: str = ""

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> "AssertionRecord":
        assertion_id = str(data.get("assertion_id", "")).strip()
        state = str(data.get("state", "")).strip().upper()
        if not assertion_id:
            raise ValueError("assertion_id is required")
        if state not in VALID_ASSERTION_STATES:
            raise ValueError(f"{assertion_id}: invalid state {state!r}")
        return cls(
            assertion_id=assertion_id,
            state=state,
            detail=str(data.get("detail", "")),
            repair_class=str(data.get("repair_class", "")).strip().upper(),
        )


def canonical_json_hash(data: Mapping[str, object]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_assertions(path: Path) -> List[AssertionRecord]:
    records: List[AssertionRecord] = []
    with path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc}") from exc
            records.append(AssertionRecord.from_dict(raw))
    return records


def validate_manifest(manifest: Mapping[str, object]) -> None:
    required = (
        "agent_scope",
        "candidate",
        "upstream_repo",
        "upstream_sha",
        "composition_profile_hash",
        "policy_hash",
        "harness_version",
    )
    missing = [key for key in required if not str(manifest.get(key, "")).strip()]
    if missing:
        raise ValueError(f"manifest missing required fields: {missing}")
    if manifest["agent_scope"] != "NAIA":
        raise ValueError(f"agent_scope must be NAIA, got {manifest['agent_scope']!r}")
    if manifest["harness_version"] != HARNESS_VERSION:
        raise ValueError(
            f"harness_version must be {HARNESS_VERSION}, got {manifest['harness_version']!r}"
        )
    sha = str(manifest["upstream_sha"])
    if len(sha) != 40 or any(ch not in "0123456789abcdef" for ch in sha.lower()):
        raise ValueError("upstream_sha must be a full 40-character git SHA")


def evaluate_assertions(
    assertions: Iterable[AssertionRecord],
    *,
    required_ids: Sequence[str] = COMMON_ASSERTIONS,
) -> dict:
    rows = list(assertions)
    by_id: Dict[str, AssertionRecord] = {}
    duplicates: List[str] = []
    for row in rows:
        if row.assertion_id in by_id:
            duplicates.append(row.assertion_id)
        by_id[row.assertion_id] = row

    missing = [assertion_id for assertion_id in required_ids if assertion_id not in by_id]
    unexpected = sorted(set(by_id) - set(required_ids))

    if duplicates or missing:
        return {
            "state": "INVALID_EVIDENCE",
            "duplicates": sorted(set(duplicates)),
            "missing": missing,
            "unexpected": unexpected,
        }

    common = [by_id[assertion_id] for assertion_id in required_ids]

    blocked = [r.assertion_id for r in common if r.state == "BLOCKED"]
    invalid = [r.assertion_id for r in common if r.state == "INVALID"]
    failed = [r for r in common if r.state == "FAIL"]

    if invalid:
        state = "INVALID_EVIDENCE"
    elif blocked:
        state = "BLOCKED_ENVIRONMENT"
    elif failed:
        if any(r.repair_class == "CROSS_CUTTING_STRUCTURAL_REWRITE" for r in failed):
            state = "FAIL_STRUCTURAL"
        else:
            state = "FAIL_LOCALIZED"
    else:
        state = "PASS_WITH_SCOPE"

    return {
        "state": state,
        "failed": [r.assertion_id for r in failed],
        "blocked": blocked,
        "invalid": invalid,
        "unexpected": unexpected,
        "assertions": [
            {
                "assertion_id": r.assertion_id,
                "state": r.state,
                "detail": r.detail,
                "repair_class": r.repair_class,
            }
            for r in common
        ],
    }


def build_summary(manifest: Mapping[str, object], assertions: Iterable[AssertionRecord]) -> dict:
    validate_manifest(manifest)
    result = evaluate_assertions(assertions)
    return {
        "harness_version": HARNESS_VERSION,
        "candidate": manifest["candidate"],
        "upstream_repo": manifest["upstream_repo"],
        "upstream_sha": manifest["upstream_sha"],
        "composition_profile_hash": manifest["composition_profile_hash"],
        "policy_hash": manifest["policy_hash"],
        "result": result,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Atento NAIA Gate-2 composition result validator")
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--assertions", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    assertions = load_assertions(args.assertions)
    summary = build_summary(manifest, assertions)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    state = summary["result"]["state"]
    if state == "PASS_WITH_SCOPE":
        return 0
    if state == "BLOCKED_ENVIRONMENT":
        return 3
    if state == "FAIL_LOCALIZED":
        return 4
    if state == "FAIL_STRUCTURAL":
        return 5
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
