from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence


HARNESS_VERSION = "NAIA-GATE2-COMPOSITION-V1"
COMMON_ASSERTIONS: tuple[str, ...] = ("ISO-1", "ISO-2", "ISO-3", "ISO-4", "ISO-5", "ISO-6")
RESULT_STATES = {
    "PASS_WITH_SCOPE",
    "FAIL_LOCALIZED",
    "FAIL_STRUCTURAL",
    "BLOCKED_ENVIRONMENT",
    "INVALID_EVIDENCE",
}
ASSERTION_STATES = {"PASS", "FAIL", "BLOCKED", "INVALID"}


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


class CompositionValidationError(ValueError):
    def __init__(self, issues: Sequence[ValidationIssue]):
        self.issues = list(issues)
        super().__init__("; ".join(f"{i.code}: {i.message}" for i in self.issues))


def canonical_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_json(data: Any) -> str:
    return hashlib.sha256(canonical_json(data).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _candidate_map(matrix: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    return {str(x["name"]): x for x in matrix.get("candidates", [])}


def validate_matrix(matrix: Mapping[str, Any]) -> None:
    issues: List[ValidationIssue] = []
    if matrix.get("version") != HARNESS_VERSION:
        issues.append(ValidationIssue("matrix.version", f"expected {HARNESS_VERSION}"))
    if int(matrix.get("common_assertions_per_candidate", -1)) != len(COMMON_ASSERTIONS):
        issues.append(ValidationIssue("matrix.common_count", "common assertion count mismatch"))

    names: set[str] = set()
    for item in matrix.get("candidates", []):
        name = str(item.get("name", ""))
        if not name:
            issues.append(ValidationIssue("matrix.candidate.name", "candidate missing name"))
        elif name in names:
            issues.append(ValidationIssue("matrix.candidate.duplicate", name))
        names.add(name)

        repo = str(item.get("repo", ""))
        sha = str(item.get("sha", ""))
        if "/" not in repo:
            issues.append(ValidationIssue("matrix.candidate.repo", f"{name}: invalid repo"))
        if len(sha) != 40 or any(c not in "0123456789abcdef" for c in sha.lower()):
            issues.append(ValidationIssue("matrix.candidate.sha", f"{name}: invalid exact SHA"))

    if issues:
        raise CompositionValidationError(issues)


def validate_result(matrix: Mapping[str, Any], result: Mapping[str, Any]) -> Dict[str, Any]:
    validate_matrix(matrix)
    issues: List[ValidationIssue] = []

    candidate_name = str(result.get("candidate", ""))
    candidate = _candidate_map(matrix).get(candidate_name)
    if candidate is None:
        issues.append(ValidationIssue("result.candidate", f"unknown candidate {candidate_name!r}"))
        candidate = {}

    if result.get("harness_version") != HARNESS_VERSION:
        issues.append(ValidationIssue("result.harness_version", f"expected {HARNESS_VERSION}"))

    if str(result.get("upstream_repo", "")) != str(candidate.get("repo", "")):
        issues.append(ValidationIssue("result.repo", "result repo does not match frozen matrix"))
    if str(result.get("upstream_sha", "")) != str(candidate.get("sha", "")):
        issues.append(ValidationIssue("result.sha", "result SHA does not match frozen matrix"))

    state = str(result.get("state", ""))
    if state not in RESULT_STATES:
        issues.append(ValidationIssue("result.state", f"invalid state {state!r}"))

    profile = result.get("composition_profile")
    policy = result.get("policy")
    if not isinstance(profile, dict):
        issues.append(ValidationIssue("result.profile", "composition_profile must be an object"))
    if not isinstance(policy, dict):
        issues.append(ValidationIssue("result.policy", "policy must be an object"))

    if isinstance(profile, dict):
        expected = sha256_json(profile)
        if result.get("composition_profile_hash") != expected:
            issues.append(ValidationIssue("result.profile_hash", "composition profile hash mismatch"))
    if isinstance(policy, dict):
        expected = sha256_json(policy)
        if result.get("policy_hash") != expected:
            issues.append(ValidationIssue("result.policy_hash", "policy hash mismatch"))

    raw_assertions = result.get("assertions", [])
    if not isinstance(raw_assertions, list):
        issues.append(ValidationIssue("result.assertions", "assertions must be a list"))
        raw_assertions = []

    by_id: Dict[str, Mapping[str, Any]] = {}
    for raw in raw_assertions:
        if not isinstance(raw, dict):
            issues.append(ValidationIssue("assertion.shape", "assertion must be an object"))
            continue
        aid = str(raw.get("id", ""))
        if aid in by_id:
            issues.append(ValidationIssue("assertion.duplicate", aid))
        by_id[aid] = raw
        astate = str(raw.get("state", ""))
        if astate not in ASSERTION_STATES:
            issues.append(ValidationIssue("assertion.state", f"{aid}: invalid state {astate!r}"))

        kind = str(raw.get("evidence_kind", ""))
        if astate == "PASS" and kind in {"", "synthetic_fixture", "static_source_only"}:
            issues.append(
                ValidationIssue(
                    "assertion.evidence_kind",
                    f"{aid}: PASS requires runtime evidence, not {kind or 'empty evidence'}",
                )
            )

    missing = [aid for aid in COMMON_ASSERTIONS if aid not in by_id]
    if missing and state not in {"BLOCKED_ENVIRONMENT", "INVALID_EVIDENCE"}:
        issues.append(ValidationIssue("assertion.missing_common", ",".join(missing)))

    # ISO-6 is intentionally strict: a synthetic echo function is not evidence
    # that the explicit Atento broker path is actually wired to the candidate.
    iso6 = by_id.get("ISO-6")
    if iso6 and iso6.get("state") == "PASS":
        if iso6.get("evidence_kind") != "runtime_broker":
            issues.append(
                ValidationIssue(
                    "iso6.synthetic_broker",
                    "ISO-6 PASS requires evidence_kind=runtime_broker",
                )
            )
        if not iso6.get("broker_endpoint_or_adapter"):
            issues.append(
                ValidationIssue(
                    "iso6.broker_identity",
                    "ISO-6 PASS requires broker_endpoint_or_adapter",
                )
            )

    required_addons = set(candidate.get("add_ons", []))
    raw_addons = result.get("add_ons", [])
    if not isinstance(raw_addons, list):
        issues.append(ValidationIssue("result.add_ons", "add_ons must be a list"))
        raw_addons = []
    addon_by_id = {
        str(x.get("id")): x
        for x in raw_addons
        if isinstance(x, dict) and x.get("id") is not None
    }
    missing_addons = sorted(required_addons - set(addon_by_id))
    if missing_addons and state not in {"BLOCKED_ENVIRONMENT", "INVALID_EVIDENCE"}:
        issues.append(ValidationIssue("addon.missing", ",".join(missing_addons)))

    for aid, raw in addon_by_id.items():
        if str(raw.get("state", "")) not in ASSERTION_STATES:
            issues.append(ValidationIssue("addon.state", f"{aid}: invalid state"))
        if raw.get("state") == "PASS" and raw.get("evidence_kind") in {
            None,
            "",
            "synthetic_fixture",
            "static_source_only",
        }:
            issues.append(ValidationIssue("addon.evidence_kind", f"{aid}: PASS lacks runtime evidence"))

    if state == "PASS_WITH_SCOPE":
        all_required = [by_id.get(x, {}) for x in COMMON_ASSERTIONS]
        if any(x.get("state") != "PASS" for x in all_required):
            issues.append(ValidationIssue("result.false_pass", "PASS_WITH_SCOPE requires ISO-1..ISO-6 PASS"))
        if any(addon_by_id.get(x, {}).get("state") != "PASS" for x in required_addons):
            issues.append(ValidationIssue("result.false_pass_addon", "PASS_WITH_SCOPE requires all add-ons PASS"))

    if state == "FAIL_STRUCTURAL":
        if not result.get("structural_failure"):
            issues.append(
                ValidationIssue(
                    "result.structural_reason",
                    "FAIL_STRUCTURAL requires structural_failure description",
                )
            )

    if state == "BLOCKED_ENVIRONMENT":
        if not result.get("blocker_id"):
            issues.append(ValidationIssue("result.blocker", "BLOCKED_ENVIRONMENT requires blocker_id"))

    if issues:
        raise CompositionValidationError(issues)

    return {
        "valid": True,
        "candidate": candidate_name,
        "state": state,
        "common_passed": sum(1 for x in COMMON_ASSERTIONS if by_id.get(x, {}).get("state") == "PASS"),
        "common_total": len(COMMON_ASSERTIONS),
        "required_add_ons": sorted(required_addons),
    }


def _validate_cmd(args: argparse.Namespace) -> int:
    matrix = load_json(args.matrix)
    result = load_json(args.result)
    try:
        summary = validate_result(matrix, result)
    except CompositionValidationError as exc:
        payload = {
            "valid": False,
            "issues": [{"code": i.code, "message": i.message} for i in exc.issues],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate NAIA Gate-2 composition evidence")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate-result")
    validate.add_argument("--matrix", required=True, type=Path)
    validate.add_argument("--result", required=True, type=Path)
    validate.set_defaults(func=_validate_cmd)
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
