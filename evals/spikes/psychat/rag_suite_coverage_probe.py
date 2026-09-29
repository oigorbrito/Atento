#!/usr/bin/env python3
"""Coverage gate for the BLOCO I deterministic RAG evaluation set.

This measures benchmark composition, not donor quality. It prevents a green
result obtained from a narrow set containing only positive/easy retrievals.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.runner import load_cases


def run(cases_path: Path) -> dict:
    cases = list(load_cases(cases_path).values())
    rag_cases = [case for case in cases if case.suite == "rag"]
    if len(rag_cases) != len(cases):
        raise AssertionError("RAG case file contains non-RAG suites")

    positives = []
    negatives = []
    gold = []
    contextual = []
    multi_evidence = []
    insufficient = []
    forced_empty = []
    user_goal_controls = []

    for case in rag_cases:
        if len(case.steps) != 1:
            raise AssertionError(f"{case.id}: BLOCO I RAG v0 expects one step per case")
        step = case.steps[0]
        expected = step.expected
        attempted = bool(step.fixtures.get("rag_attempted", False))
        retrieved = [str(x) for x in step.fixtures.get("retrieval_fixture", [])]

        if expected.rag_required is True:
            positives.append(case.id)
        elif expected.rag_required is False:
            negatives.append(case.id)

        if "psychat_gold" in case.tags:
            gold.append(case.id)
        if case.context:
            contextual.append(case.id)
        if len(expected.rag_document_ids or []) >= 2:
            multi_evidence.append(case.id)
        if "acknowledge_insufficient_evidence" in expected.required_behaviors:
            insufficient.append(case.id)
        if attempted and not retrieved:
            forced_empty.append(case.id)
        if (
            expected.rag_required is False
            and "respect_user_goal" in expected.required_behaviors
        ):
            user_goal_controls.append(case.id)

    gates = {
        "case_count_at_least_20": len(rag_cases) >= 20,
        "positive_retrieval_cases_at_least_10": len(positives) >= 10,
        "negative_controls_at_least_5": len(negatives) >= 5,
        "psychat_gold_cases_at_least_4": len(gold) >= 4,
        "contextual_cases_at_least_2": len(contextual) >= 2,
        "multi_evidence_cases_at_least_1": len(multi_evidence) >= 1,
        "insufficient_evidence_cases_at_least_1": len(insufficient) >= 1,
        "attempted_empty_retrieval_cases_at_least_1": len(forced_empty) >= 1,
        "explicit_user_goal_negative_controls_at_least_2": len(user_goal_controls) >= 2,
    }
    failed = [name for name, passed in gates.items() if not passed]
    if failed:
        raise AssertionError(f"RAG suite coverage gates failed: {failed}")

    return {
        "metric_version": "atentoeval-rag-suite-coverage-v0.1",
        "quality_claim": False,
        "coverage_gate_pass": True,
        "case_count": len(rag_cases),
        "counts": {
            "positive_retrieval": len(positives),
            "negative_control": len(negatives),
            "psychat_gold": len(gold),
            "contextual": len(contextual),
            "multi_evidence": len(multi_evidence),
            "insufficient_evidence": len(insufficient),
            "attempted_empty_retrieval": len(forced_empty),
            "explicit_user_goal_negative_control": len(user_goal_controls),
        },
        "case_ids": {
            "psychat_gold": gold,
            "contextual": contextual,
            "multi_evidence": multi_evidence,
            "insufficient_evidence": insufficient,
            "attempted_empty_retrieval": forced_empty,
            "explicit_user_goal_negative_control": user_goal_controls,
        },
        "gates": gates,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run(args.cases)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
