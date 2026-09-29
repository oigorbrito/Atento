#!/usr/bin/env python3
"""Fail-closed evidence readiness gate for BLOCO I — RAG.

This gate does not decide fork vs greenfield. It answers a narrower question:
"is the evidence package complete enough for ADR-000 to be decided?"

By default it exits non-zero when evidence is incomplete. --report-only writes
the same report but exits zero so CI can publish the blocker list while the
block is still IN_PROGRESS.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Callable


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def load_optional(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def truthy(data: dict[str, Any], dotted: str) -> bool:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return bool(cur)


def equals(data: dict[str, Any], dotted: str, expected: Any) -> bool:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    return cur == expected


def at_least(data: dict[str, Any], dotted: str, minimum: float) -> bool:
    cur: Any = data
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    try:
        return float(cur) >= minimum
    except (TypeError, ValueError):
        return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument(
        "--repo-evidence-dir",
        type=Path,
        default=Path("evals/evidence"),
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()

    root = args.results_dir
    evidence_root = args.repo_evidence_dir
    requirements: list[tuple[str, str, Callable[[dict[str, Any]], bool]]] = [
        (
            "real_session_isolation",
            "psychat_real_isolation.json",
            lambda d: (
                truthy(d, "upstream_shared_instance_cross_session_state")
                and truthy(d, "adapted_bridge_isolated")
                and truthy(d, "adapted_bridge_session_continuity")
            ),
        ),
        (
            "minimal_fork_execution",
            "psychat_minimal_fork_patch.json",
            lambda d: (
                equals(d, "pinned_commit", PINNED_COMMIT)
                and equals(d, "direct_provider_bypass_count_in_patched_rag_surface", 0)
                and truthy(d, "model_gateway_injectable")
                and truthy(d, "embedding_gateway_injectable")
                and truthy(d, "external_rag_route_enforceable")
                and equals(d, "donor_files_touched_to_introduce_provider_boundary", 3)
                and equals(d, "donor_files_touched_for_bloco_i_rag_correctness", 4)
                and truthy(d, "qa_id_provenance_patch_required")
                and equals(d, "vector_distance_metric", "cosine")
                and truthy(d, "vector_clear_preserves_index_contract")
                and truthy(d, "clear_collection_uses_atomic_empty_generation")
                and truthy(d, "embedding_identity_required_by_vector_store")
                and truthy(d, "vector_collection_namespaced_by_embedding_identity")
                and truthy(d, "vector_collection_namespaced_by_corpus_identity")
                and truthy(d, "same_identity_rebuild_uses_upsert")
                and truthy(d, "collection_info_exposes_index_identity")
                and truthy(d, "persisted_collection_metadata_validated")
                and truthy(d, "collection_contract_mismatch_fails_closed")
                and truthy(d, "knowledge_base_rebuild_defaults_to_replace")
                and truthy(d, "knowledge_base_rebuild_clear_fails_closed")
                and truthy(d, "knowledge_base_rebuild_uses_staging_generation")
                and truthy(d, "active_index_pointer_promoted_atomically")
                and truthy(d, "partial_staging_index_never_promoted")
                and truthy(d, "long_lived_vector_store_refreshes_active_generation")
                and truthy(d, "incremental_writes_refresh_active_generation")
            ),
        ),
        (
            "provider_replacement",
            "psychat_provider_replacement.json",
            lambda d: (
                truthy(d, "model_provider_swap_pass")
                and truthy(d, "embedding_provider_swap_pass")
                and truthy(d, "embedding_index_identity_isolated")
                and truthy(d, "composition_provider_consistency_pass")
                and truthy(d, "knowledge_base_rebuild_replace_default_pass")
                and truthy(d, "knowledge_base_rebuild_clear_fail_closed_pass")
                and truthy(d, "knowledge_base_rebuild_atomic_path_pass")
                and truthy(d, "rag_model_gateway_swap_pass")
                and truthy(d, "external_rag_route_enforcement_pass")
                and equals(d, "donor_source_edit_required_for_swap", False)
                and equals(d, "files_touched_to_swap_provider_after_boundary", 0)
                and truthy(d, "shared_vector_resource_reused")
                and truthy(d, "distinct_session_runtimes")
                and truthy(d, "session_state_isolated")
            ),
        ),
        (
            "retrieval_preservation",
            "psychat_retrieval_preservation.json",
            lambda d: (
                truthy(d, "donor_replacement_test_pass")
                and truthy(d, "retrieval_mechanics_preserved")
            ),
        ),
        (
            "qa_id_provenance_upstream",
            "psychat_qa_id_provenance_upstream.json",
            lambda d: (
                equals(d, "pinned_commit", PINNED_COMMIT)
                and equals(d, "unknown_chunk_ratio", 1.0)
                and equals(d, "known_unique_qa_id_count", 0)
            ),
        ),
        (
            "qa_id_provenance_patched",
            "psychat_qa_id_provenance_patched.json",
            lambda d: (
                equals(d, "pinned_commit", PINNED_COMMIT)
                and equals(d, "unknown_chunk_count", 0)
                and equals(d, "missing_raw_id_count", 0)
                and truthy(d, "gold_id_survival.328")
                and truthy(d, "gold_id_survival.350")
                and truthy(d, "gold_id_survival.1864")
                and truthy(d, "gold_id_survival.1882")
            ),
        ),
        (
            "vector_metric_upstream",
            "psychat_vector_metric_upstream.json",
            lambda d: (
                equals(d, "runtime_shape", "upstream")
                and equals(d, "semantic_status", "IMPLICIT_CHROMA_DEFAULT")
            ),
        ),
        (
            "vector_metric_patched",
            "psychat_vector_metric_patched.json",
            lambda d: (
                equals(d, "runtime_shape", "patched")
                and equals(d, "explicit_hnsw_space", "cosine")
                and equals(d, "semantic_status", "EXPLICIT_COSINE_VERSIONED_INDEX")
                and truthy(d, "clear_collection_contract_preserved")
                and truthy(d, "clear_collection_atomic_empty_generation")
                and truthy(d, "embedding_identity")
                and truthy(d, "corpus_identity")
                and truthy(d, "corpus_identity_isolated")
                and truthy(d, "same_identity_rebuild_uses_upsert")
                and truthy(d, "collection_info_exposes_index_identity")
                and truthy(d, "persisted_collection_metadata_validation_pass")
                and truthy(d, "collection_contract_mismatch_fails_closed")
                and truthy(d, "atomic_generation_promotion_pass")
                and truthy(d, "partial_staging_never_promoted")
                and truthy(d, "promoted_generation_survives_restart")
                and truthy(d, "corrupt_pointer_fails_closed")
                and truthy(d, "long_lived_reader_refreshes_active_generation")
                and truthy(d, "incremental_writer_refreshes_active_generation")
            ),
        ),
        (
            "adapter_dynamic_chassis",
            "psychat_adapter_dynamic_chassis.json",
            lambda d: (
                equals(d, "schema_validation.schema_validation_coverage", 1.0)
                and equals(d, "trace.trace_coverage", 1.0)
                and truthy(d, "trace.observable_index_identity_pass")
                and truthy(d, "rollback.rollback_test_pass")
                and truthy(d, "safety.independent_safety_enforcement_pass")
                and truthy(d, "resilience.resilience_boundary_dynamic_pass")
            ),
        ),
        (
            "rag_suite_coverage",
            "psychat_rag_suite_coverage.json",
            lambda d: truthy(d, "coverage_gate_pass"),
        ),
        (
            "rag_end_to_end_plumbing",
            "psychat_rag_harness_plumbing.json",
            lambda d: (
                truthy(d, "all_deterministic_rag_metrics_pass")
                and at_least(d, "bridge_case_count", 1)
                and at_least(d, "forced_empty_retrieval_case_count", 1)
                and equals(d, "quality_claim", False)
            ),
        ),
        (
            "gold_provenance",
            "psychat_gold_source.json",
            lambda d: (
                truthy(d, "all_gold_ids_found")
                and equals(d, "pinned_commit", PINNED_COMMIT)
            ),
        ),
        (
            "upstream_cfs_report",
            "psychat_static_chassis.json",
            lambda d: equals(d, "syntax_error_count", 0),
        ),
        (
            "adapter_cfs_report",
            "psychat_adapted_chassis.json",
            lambda d: equals(d, "syntax_error_count", 0),
        ),
        (
            "patched_composed_cfs_report",
            "psychat_patched_rag_chassis.json",
            lambda d: equals(d, "syntax_error_count", 0),
        ),
    ]

    static_requirements: list[
        tuple[str, Path, Callable[[dict[str, Any]], bool]]
    ] = [
        (
            "donor_license_known",
            evidence_root / "psychat_license.json",
            lambda d: (
                equals(d, "pinned_donor_commit", PINNED_COMMIT)
                and equals(d, "license", "MIT")
                and truthy(d, "fork_modification_permission_present")
                and truthy(d, "distribution_permission_present")
                and truthy(d, "notice_retention_required")
            ),
        ),
        (
            "minimal_fork_git_surface",
            evidence_root / "psychat_minimal_fork_git.json",
            lambda d: (
                equals(d, "pinned_donor_commit", PINNED_COMMIT)
                and equals(d, "files_touched_exact", 3)
                and equals(d, "static_patched_invariants.direct_requests_post_count", 0)
                and truthy(d, "static_patched_invariants.psychology_agent_model_gateway_injected")
                and truthy(d, "static_patched_invariants.vector_store_embedding_gateway_injected")
                and truthy(d, "static_patched_invariants.rag_system_force_retrieval_signature")
            ),
        ),
        (
            "full_bloco_i_git_surface",
            evidence_root / "psychat_block_i_git.json",
            lambda d: (
                equals(d, "pinned_donor_commit", PINNED_COMMIT)
                and equals(d, "files_touched_exact", 4)
                and equals(d, "provider_boundary_files_touched", 3)
                and equals(d, "static_patched_invariants.direct_requests_post_count", 0)
                and truthy(d, "static_patched_invariants.rag_system_force_retrieval_signature")
                and truthy(d, "static_patched_invariants.rag_system_force_retrieval_propagated")
                and truthy(d, "static_patched_invariants.final_response_messages_constructed_locally")
                and equals(d, "static_patched_invariants.explicit_hnsw_space", "cosine")
                and truthy(d, "static_patched_invariants.embedding_identity_required")
                and truthy(d, "static_patched_invariants.corpus_identity_required")
                and truthy(d, "static_patched_invariants.index_schema_constant_defined")
                and truthy(d, "static_patched_invariants.default_corpus_identity_constant_defined")
                and truthy(d, "static_patched_invariants.collection_namespaced_by_index_identity")
                and truthy(d, "static_patched_invariants.same_identity_rebuild_uses_upsert")
                and equals(d, "static_patched_invariants.legacy_collection_add_remaining", False)
                and truthy(d, "static_patched_invariants.collection_info_exposes_index_identity")
                and truthy(d, "static_patched_invariants.persisted_collection_metadata_validated")
                and truthy(d, "static_patched_invariants.collection_contract_mismatch_fails_closed")
                and truthy(d, "static_patched_invariants.knowledge_base_rebuild_defaults_to_replace")
                and truthy(d, "static_patched_invariants.knowledge_base_rebuild_clear_fails_closed")
                and truthy(d, "static_patched_invariants.knowledge_base_rebuild_uses_staging_generation")
                and truthy(d, "static_patched_invariants.active_index_pointer_promoted_atomically")
                and truthy(d, "static_patched_invariants.staging_validated_before_pointer_promotion")
                and truthy(d, "static_patched_invariants.partial_staging_index_never_promoted")
                and truthy(d, "static_patched_invariants.clear_collection_uses_atomic_empty_generation")
                and truthy(d, "static_patched_invariants.long_lived_vector_store_refreshes_active_generation")
                and truthy(d, "static_patched_invariants.incremental_writes_refresh_active_generation")
                and truthy(d, "static_patched_invariants.rag_destructive_preclear_removed")
                and truthy(d, "static_patched_invariants.qa_id_carry_forward_present")
                and equals(d, "pinned_corpus_parser_evidence.upstream_unknown_qa_id_sections", 4760)
                and equals(d, "pinned_corpus_parser_evidence.patched_unknown_qa_id_sections", 0)
                and equals(d, "pinned_corpus_parser_evidence.patched_missing_raw_ids", 0)
                and truthy(d, "pinned_corpus_parser_evidence.gold_id_survival.328")
                and truthy(d, "pinned_corpus_parser_evidence.gold_id_survival.350")
                and truthy(d, "pinned_corpus_parser_evidence.gold_id_survival.1864")
                and truthy(d, "pinned_corpus_parser_evidence.gold_id_survival.1882")
            ),
        ),
        (
            "adapter_git_change_surface",
            evidence_root / "psychat_adapter_change_surface_git.json",
            lambda d: (
                equals(d, "scenarios.swap_registered_executor.files_touched_total", 0)
                and equals(d, "scenarios.introduce_new_executor.files_touched_total", 1)
                and equals(d, "scenarios.introduce_new_executor.existing_chassis_files_touched", 0)
                and equals(d, "scenarios.add_new_capability.files_touched_total", 1)
                and equals(d, "scenarios.add_new_capability.existing_chassis_files_touched", 0)
            ),
        ),
    ]

    checks = []
    blockers = []

    for requirement_id, path, predicate in static_requirements:
        data = load_optional(path)
        if data is None:
            status = "MISSING"
            detail = "required versioned Git evidence does not exist"
        else:
            passed = bool(predicate(data))
            status = "PASS" if passed else "FAIL"
            detail = (
                "versioned Git evidence satisfied"
                if passed
                else "versioned Git evidence failed required assertions"
            )
        row = {
            "id": requirement_id,
            "file": str(path),
            "status": status,
            "detail": detail,
        }
        checks.append(row)
        if status != "PASS":
            blockers.append(row)

    for requirement_id, filename, predicate in requirements:
        path = root / filename
        data = load_optional(path)
        if data is None:
            status = "MISSING"
            detail = "required evidence artifact does not exist"
        else:
            try:
                passed = bool(predicate(data))
            except Exception as exc:
                passed = False
                detail = f"evidence predicate raised: {exc}"
            else:
                detail = "required assertions satisfied" if passed else "required assertions not satisfied"
            status = "PASS" if passed else "FAIL"

        row = {
            "id": requirement_id,
            "file": filename,
            "status": status,
            "detail": detail,
        }
        checks.append(row)
        if status != "PASS":
            blockers.append(row)

    # Semantic RAG quality is intentionally separate from plumbing. It is
    # required for ADR readiness, but this gate does not impose an arbitrary
    # score threshold. The quality report must explicitly state that the
    # multilingual/gold evaluation is complete so ADR-000 can inspect metrics.
    quality_path = root / "psychat_rag_quality.json"
    quality = load_optional(quality_path)
    if quality is None:
        quality_row = {
            "id": "rag_quality_evidence",
            "file": quality_path.name,
            "status": "MISSING",
            "detail": "real semantic RAG quality report is required for ADR readiness",
        }
    else:
        quality_ok = (
            truthy(quality, "quality_evidence_complete")
            and truthy(quality, "cross_language_gold_evaluated")
            and truthy(quality, "behavioral_gold_evaluated")
            and equals(quality, "pinned_commit", PINNED_COMMIT)
            and at_least(quality, "gold_case_count", 4)
            and at_least(quality, "multilingual_retrieval.gold_pair_count", 4)
            and equals(
                quality,
                "retrieval_query_languages",
                ["pt-BR", "zh-CN"],
            )
        )
        quality_row = {
            "id": "rag_quality_evidence",
            "file": quality_path.name,
            "status": "PASS" if quality_ok else "FAIL",
            "detail": (
                "quality evidence complete"
                if quality_ok
                else "quality report exists but required multilingual/gold evidence is incomplete"
            ),
        }
    checks.append(quality_row)
    if quality_row["status"] != "PASS":
        blockers.append(quality_row)

    ready = not blockers
    report = {
        "metric_version": "psychat-block-i-readiness-v0.25",
        "block": "BLOCO I — RAG",
        "decision_scope": "evidence readiness only; does not choose fork vs greenfield",
        "ready_for_adr": ready,
        "required_check_count": len(checks),
        "passed_check_count": sum(1 for row in checks if row["status"] == "PASS"),
        "blocker_count": len(blockers),
        "checks": checks,
        "blockers": blockers,
    }

    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")

    if not ready and not args.report_only:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
