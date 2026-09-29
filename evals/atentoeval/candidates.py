from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class CandidateVariant(str, Enum):
    UPSTREAM = "UPSTREAM"
    WRAPPED = "WRAPPED"
    FORKED = "FORKED"
    NATIVE = "NATIVE"
    MODEL_ADAPTER = "MODEL_ADAPTER"


class EvidenceStatus(str, Enum):
    PASS_EMPIRICAL = "PASS_EMPIRICAL"
    PASS_STATIC = "PASS_STATIC"
    PENDING_EXECUTION = "PENDING_EXECUTION"
    INFRA_BLOCKED = "INFRA_BLOCKED"
    QUALITY_RISK = "QUALITY_RISK"
    ARCH_RISK = "ARCH_RISK"
    NOT_DECIDED = "NOT_DECIDED"


@dataclass(frozen=True)
class CandidateSpec:
    candidate_id: str
    block: str
    source_id: str
    variant: CandidateVariant
    adapter_id: str
    repository: str | None = None
    upstream_sha: str | None = None
    ci_enabled: bool = False
    ci_profile: str | None = None
    external_terms_note: str = ""

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "CandidateSpec":
        candidate = cls(
            candidate_id=str(raw["candidate_id"]),
            block=str(raw["block"]),
            source_id=str(raw["source_id"]),
            variant=CandidateVariant(raw["variant"]),
            adapter_id=str(raw["adapter_id"]),
            repository=raw.get("repository"),
            upstream_sha=raw.get("upstream_sha"),
            ci_enabled=bool(raw.get("ci_enabled", False)),
            ci_profile=raw.get("ci_profile"),
            external_terms_note=str(raw.get("external_terms_note", "")),
        )
        candidate.validate()
        return candidate

    def validate(self) -> None:
        if not self.candidate_id:
            raise ValueError("candidate_id is required")
        if not self.block:
            raise ValueError(f"{self.candidate_id}: block is required")
        if not self.source_id:
            raise ValueError(f"{self.candidate_id}: source_id is required")
        if not self.adapter_id:
            raise ValueError(f"{self.candidate_id}: adapter_id is required")

        external = self.variant is not CandidateVariant.NATIVE
        if external and (not self.repository or not self.upstream_sha):
            raise ValueError(
                f"{self.candidate_id}: external candidates require repository + upstream_sha"
            )
        if self.variant is CandidateVariant.NATIVE and (self.repository or self.upstream_sha):
            raise ValueError(
                f"{self.candidate_id}: NATIVE candidates must not claim an external upstream pin"
            )
        if self.upstream_sha and len(self.upstream_sha) != 40:
            raise ValueError(f"{self.candidate_id}: upstream_sha must be a full 40-char Git SHA")
        if self.ci_enabled and not self.ci_profile:
            raise ValueError(f"{self.candidate_id}: ci_enabled requires ci_profile")


@dataclass
class CandidateResult:
    candidate_id: str
    block: str
    source_id: str
    variant: str
    evidence_status: str
    evaluation_kind: str
    atento_sha: str
    repository: str | None = None
    upstream_sha: str | None = None
    case_set_hash: str | None = None
    policy_hash: str | None = None
    chassis: dict[str, Any] = field(default_factory=dict)
    benchmark: dict[str, Any] = field(default_factory=dict)
    safety: dict[str, Any] = field(default_factory=dict)
    latency: dict[str, Any] = field(default_factory=dict)
    cost: dict[str, Any] = field(default_factory=dict)
    git_surface: dict[str, Any] = field(default_factory=dict)
    blockers: list[dict[str, Any]] = field(default_factory=list)

    def validate(self) -> None:
        CandidateVariant(self.variant)
        EvidenceStatus(self.evidence_status)
        if not self.candidate_id or not self.block or not self.source_id:
            raise ValueError("candidate identity fields are required")
        if not self.evaluation_kind:
            raise ValueError("evaluation_kind is required")
        if not self.atento_sha:
            raise ValueError("atento_sha is required")
        if self.upstream_sha and len(self.upstream_sha) != 40:
            raise ValueError("upstream_sha must be a full 40-char Git SHA")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


def load_registry(path: Path) -> list[CandidateSpec]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    candidates = [CandidateSpec.from_dict(item) for item in raw.get("candidates", [])]
    ids = [candidate.candidate_id for candidate in candidates]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate candidate_id in registry")
    return candidates


def github_matrix(path: Path) -> dict[str, list[dict[str, Any]]]:
    include: list[dict[str, Any]] = []
    for candidate in load_registry(path):
        if not candidate.ci_enabled:
            continue
        if candidate.ci_profile != "python_static_chassis":
            raise ValueError(
                f"{candidate.candidate_id}: unsupported ci_profile {candidate.ci_profile!r}"
            )
        include.append(
            {
                "candidate_id": candidate.candidate_id,
                "block": candidate.block,
                "source_id": candidate.source_id,
                "variant": candidate.variant.value,
                "repository": candidate.repository,
                "upstream_sha": candidate.upstream_sha,
                "ci_profile": candidate.ci_profile,
            }
        )
    if not include:
        raise ValueError("candidate registry has no CI-enabled candidates")
    return {"include": include}


def write_static_result(
    *,
    registry: Path,
    candidate_id: str,
    audit: Path,
    atento_sha: str,
    output: Path,
) -> CandidateResult:
    by_id = {candidate.candidate_id: candidate for candidate in load_registry(registry)}
    if candidate_id not in by_id:
        raise ValueError(f"unknown candidate_id: {candidate_id}")
    candidate = by_id[candidate_id]
    audit_data = json.loads(audit.read_text(encoding="utf-8"))
    result = CandidateResult(
        candidate_id=candidate.candidate_id,
        block=candidate.block,
        source_id=candidate.source_id,
        variant=candidate.variant.value,
        evidence_status=EvidenceStatus.PASS_STATIC.value,
        evaluation_kind="static_chassis",
        atento_sha=atento_sha,
        repository=candidate.repository,
        upstream_sha=candidate.upstream_sha,
        chassis=audit_data,
    )
    result.validate()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result.to_dict(), ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Atento candidate registry/result utilities")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-registry")
    validate.add_argument("--registry", type=Path, required=True)

    matrix = sub.add_parser("github-matrix")
    matrix.add_argument("--registry", type=Path, required=True)

    static = sub.add_parser("static-result")
    static.add_argument("--registry", type=Path, required=True)
    static.add_argument("--candidate-id", required=True)
    static.add_argument("--audit", type=Path, required=True)
    static.add_argument("--atento-sha", required=True)
    static.add_argument("--output", type=Path, required=True)

    args = parser.parse_args()

    if args.command == "validate-registry":
        loaded = load_registry(args.registry)
        print(json.dumps({"valid": True, "candidate_count": len(loaded)}))
        return 0

    if args.command == "github-matrix":
        print(json.dumps(github_matrix(args.registry), separators=(",", ":")))
        return 0

    if args.command == "static-result":
        result = write_static_result(
            registry=args.registry,
            candidate_id=args.candidate_id,
            audit=args.audit,
            atento_sha=args.atento_sha,
            output=args.output,
        )
        print(json.dumps(result.to_dict(), ensure_ascii=False, separators=(",", ":")))
        return 0

    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
