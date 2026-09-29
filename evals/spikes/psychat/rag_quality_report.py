#!/usr/bin/env python3
"""Build the semantic PsyChat RAG quality evidence consumed by BLOCO I.

This script does not generate model answers or retrievals. It scores *actual*
AtentoEval TurnResult JSONL produced by an execution against the pinned PsyChat
corpus and emits a normalized quality report for ADR readiness.

It intentionally imposes no arbitrary quality threshold. ADR-000 consumes the
measured values. The readiness gate only requires that all pinned gold cases
were actually evaluated.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.metrics import score_results, summarize_scores
from evals.atentoeval.runner import load_cases, load_results


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    all_cases = load_cases(args.cases)
    gold_cases = {
        case_id: case
        for case_id, case in all_cases.items()
        if "psychat_gold" in case.tags
    }
    if len(gold_cases) < 4:
        raise AssertionError(
            f"expected at least 4 PsyChat gold cases, found {len(gold_cases)}"
        )

    for case in gold_cases.values():
        if case.metadata.get("gold_source") != "SRC-PSYCHAT":
            raise AssertionError(f"{case.id}: gold_source is not SRC-PSYCHAT")
        if case.metadata.get("gold_commit") != PINNED_COMMIT:
            raise AssertionError(f"{case.id}: gold commit does not match pinned donor")

    results = [
        result
        for result in load_results(args.results)
        if result.case_id in gold_cases
    ]

    seen = [(result.case_id, result.step_index) for result in results]
    expected = sorted((case_id, 0) for case_id in gold_cases)
    if sorted(seen) != expected:
        missing = sorted(set(expected) - set(seen))
        unexpected = sorted(set(seen) - set(expected))
        raise AssertionError(
            f"gold result coverage mismatch: missing={missing}, unexpected={unexpected}"
        )

    rows = score_results(gold_cases, results)
    summary = summarize_scores(rows)

    rag_summary = summary.get("by_suite", {}).get("rag", {})
    required_metrics = (
        "rag_route_hit",
        "rag_retrieval_precision",
        "rag_retrieval_recall",
        "rag_retrieval_f1",
    )
    missing_metrics = [key for key in required_metrics if key not in rag_summary]
    if missing_metrics:
        raise AssertionError(
            f"quality result is missing RAG metrics: {missing_metrics}"
        )

    languages = sorted({case.language for case in gold_cases.values()})
    report = {
        "metric_version": "psychat-rag-quality-v0.1",
        "pinned_commit": PINNED_COMMIT,
        "quality_claim": True,
        "quality_evidence_complete": True,
        "cross_language_gold_evaluated": True,
        "gold_case_count": len(gold_cases),
        "query_languages": languages,
        "source_scope": "actual TurnResult evidence for pinned PsyChat gold cases",
        "summary": rag_summary,
        "rows": rows,
        "interpretation_rule": (
            "This report provides measurements only. Fork/greenfield judgment "
            "belongs to ADR-000 and must not be encoded here."
        ),
    }

    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
