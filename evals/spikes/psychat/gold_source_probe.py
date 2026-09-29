#!/usr/bin/env python3
"""Verify PsyChat-mapped AtentoEval gold IDs against the pinned donor corpus.

This probe proves source identity/provenance only. It also records whether a
pt-BR case maps to evidence containing CJK text so cross-language retrieval is
not accidentally treated as already validated.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from evals.atentoeval.runner import load_cases


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


def find_id(knowledge_dir: Path, doc_id: str) -> dict | None:
    needles = (f"ID: {doc_id}", f"ID:{doc_id}")
    for path in sorted(knowledge_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        positions = [text.find(needle) for needle in needles]
        positions = [pos for pos in positions if pos >= 0]
        if not positions:
            continue

        pos = min(positions)
        start = max(0, pos - 500)
        end = min(len(text), pos + 1500)
        window = text[start:end]
        cjk_count = len(CJK_RE.findall(window))
        return {
            "filename": path.name,
            "contains_cjk_near_gold": cjk_count > 0,
            "cjk_char_count_near_gold": cjk_count,
        }
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    knowledge_dir = args.donor_root / "resources" / "knowledge"
    if not knowledge_dir.exists():
        raise AssertionError(f"missing donor knowledge directory: {knowledge_dir}")

    cases = load_cases(args.cases)
    gold = [case for case in cases.values() if "psychat_gold" in case.tags]
    if not gold:
        raise AssertionError("no psychat_gold cases found")

    rows = []
    cross_language = []
    for case in gold:
        if case.metadata.get("gold_source") != "SRC-PSYCHAT":
            raise AssertionError(f"{case.id}: unexpected gold_source")
        if case.metadata.get("gold_commit") != PINNED_COMMIT:
            raise AssertionError(f"{case.id}: gold commit is not pinned donor commit")

        expected_ids = case.steps[0].expected.rag_document_ids or []
        if not expected_ids:
            raise AssertionError(f"{case.id}: gold case has no expected document IDs")

        found = {}
        case_requires_multilingual = False
        for doc_id in expected_ids:
            evidence = find_id(knowledge_dir, str(doc_id))
            if evidence is None:
                raise AssertionError(
                    f"{case.id}: document ID {doc_id} not found in pinned corpus"
                )
            found[str(doc_id)] = evidence
            if (
                case.language.lower().startswith("pt")
                and evidence["contains_cjk_near_gold"]
            ):
                case_requires_multilingual = True

        row = {
            "case_id": case.id,
            "query_language": case.language,
            "expected_ids": [str(x) for x in expected_ids],
            "corpus_evidence": found,
            "multilingual_retrieval_required": case_requires_multilingual,
        }
        rows.append(row)
        if case_requires_multilingual:
            cross_language.append(case.id)

    report = {
        "probe": "psychat_gold_source",
        "pinned_commit": PINNED_COMMIT,
        "quality_claim": False,
        "provenance_claim": True,
        "gold_case_count": len(rows),
        "all_gold_ids_found": True,
        "cross_language_gold_case_count": len(cross_language),
        "cross_language_gold_case_ids": cross_language,
        "multilingual_retrieval_quality_status": (
            "REQUIRES_DYNAMIC_RETRIEVAL_EVIDENCE"
            if cross_language
            else "NOT_IDENTIFIED_BY_HEURISTIC"
        ),
        "rows": rows,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
