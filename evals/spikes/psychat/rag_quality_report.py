#!/usr/bin/env python3
"""Build semantic PsyChat RAG quality evidence consumed by BLOCO I.

The report requires two independent real-evidence inputs:

1. actual AtentoEval TurnResult rows for every pinned PsyChat gold case,
   including behavioral judge output;
2. a completed paired pt-BR/zh-CN multilingual retrieval microbenchmark.

It imposes no political/product-choice verdict and no arbitrary quality
threshold. ADR-000 consumes the measured values; this script only establishes
that the evidence package is complete enough to inspect.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.metrics import score_results, summarize_scores
from evals.atentoeval.runner import load_cases, load_results


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_multilingual(report: dict) -> dict:
    if report.get("quality_claim") is not True:
        raise AssertionError(
            "multilingual retrieval evidence is absent/skipped or is not a quality run"
        )

    hit_rate = report.get("hit_rate_by_language")
    mrr = report.get("mrr_by_language")
    if not isinstance(hit_rate, dict) or set(hit_rate) != {"pt-BR", "zh-CN"}:
        raise AssertionError(
            f"multilingual hit-rate must contain pt-BR + zh-CN, got {hit_rate!r}"
        )
    if not isinstance(mrr, dict) or set(mrr) != {"pt-BR", "zh-CN"}:
        raise AssertionError(
            f"multilingual MRR must contain pt-BR + zh-CN, got {mrr!r}"
        )

    rows = report.get("rows")
    if not isinstance(rows, list):
        raise AssertionError("multilingual report is missing query rows")
    row_languages = {str(row.get("query_language")) for row in rows}
    if row_languages != {"pt-BR", "zh-CN"}:
        raise AssertionError(
            f"multilingual rows do not cover both languages: {row_languages}"
        )

    pair_ids = {str(row.get("pair_id")) for row in rows}
    if len(pair_ids) < 4:
        raise AssertionError(
            f"expected at least 4 paired multilingual golds, got {len(pair_ids)}"
        )
    for pair_id in pair_ids:
        langs = {
            str(row.get("query_language"))
            for row in rows
            if str(row.get("pair_id")) == pair_id
        }
        if langs != {"pt-BR", "zh-CN"}:
            raise AssertionError(
                f"{pair_id}: paired retrieval did not execute both languages"
            )

    return {
        "metric_version": report.get("metric_version"),
        "embedding_model": report.get("embedding_model"),
        "gold_pair_count": len(pair_ids),
        "query_count": len(rows),
        "hit_rate_by_language": hit_rate,
        "mrr_by_language": mrr,
        "zh_minus_pt_hit_rate_gap": report.get("zh_minus_pt_hit_rate_gap"),
        "zh_minus_pt_mrr_gap": report.get("zh_minus_pt_mrr_gap"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--multilingual-report", type=Path, required=True)
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
            raise AssertionError(
                f"{case.id}: gold commit does not match pinned donor"
            )

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
            f"gold result coverage mismatch: missing={missing}, "
            f"unexpected={unexpected}"
        )

    missing_judge = []
    for result in results:
        required = ("weighted_behavior_score", "critical_failure")
        absent = [key for key in required if key not in result.judge]
        if absent:
            missing_judge.append(
                {
                    "case_id": result.case_id,
                    "step_index": result.step_index,
                    "missing": absent,
                }
            )
    if missing_judge:
        raise AssertionError(
            "gold TurnResults are missing behavioral judge evidence: "
            f"{missing_judge}"
        )

    rows = score_results(gold_cases, results)
    summary = summarize_scores(rows)

    rag_summary = summary.get("by_suite", {}).get("rag", {})
    required_metrics = (
        "rag_route_hit",
        "rag_retrieval_precision",
        "rag_retrieval_recall",
        "rag_retrieval_f1",
        "weighted_behavior_score",
        "critical_failure_count",
    )
    missing_metrics = [key for key in required_metrics if key not in rag_summary]
    if missing_metrics:
        raise AssertionError(
            f"quality result is missing required metrics: {missing_metrics}"
        )

    multilingual = validate_multilingual(load_json(args.multilingual_report))

    report = {
        "metric_version": "psychat-rag-quality-v0.2",
        "pinned_commit": PINNED_COMMIT,
        "quality_claim": True,
        "quality_evidence_complete": True,
        "cross_language_gold_evaluated": True,
        "behavioral_gold_evaluated": True,
        "gold_case_count": len(gold_cases),
        "turn_result_query_languages": sorted(
            {case.language for case in gold_cases.values()}
        ),
        "retrieval_query_languages": ["pt-BR", "zh-CN"],
        "source_scope": (
            "actual judged TurnResult evidence for pinned PsyChat gold cases "
            "plus paired real-evidence multilingual retrieval"
        ),
        "summary": rag_summary,
        "multilingual_retrieval": multilingual,
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
