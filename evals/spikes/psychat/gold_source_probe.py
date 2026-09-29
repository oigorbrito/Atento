#!/usr/bin/env python3
"""Verify PsyChat-mapped AtentoEval gold IDs against the pinned donor corpus."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.runner import load_cases


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def find_id(knowledge_dir: Path, doc_id: str) -> str | None:
    needles = (f"ID: {doc_id}", f"ID:{doc_id}")
    for path in sorted(knowledge_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(needle in text for needle in needles):
            return path.name
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
    for case in gold:
        if case.metadata.get("gold_source") != "SRC-PSYCHAT":
            raise AssertionError(f"{case.id}: unexpected gold_source")
        if case.metadata.get("gold_commit") != PINNED_COMMIT:
            raise AssertionError(f"{case.id}: gold commit is not pinned donor commit")

        expected_ids = case.steps[0].expected.rag_document_ids or []
        if not expected_ids:
            raise AssertionError(f"{case.id}: gold case has no expected document IDs")

        found = {}
        for doc_id in expected_ids:
            filename = find_id(knowledge_dir, str(doc_id))
            if filename is None:
                raise AssertionError(
                    f"{case.id}: document ID {doc_id} not found in pinned corpus"
                )
            found[str(doc_id)] = filename

        rows.append(
            {
                "case_id": case.id,
                "expected_ids": [str(x) for x in expected_ids],
                "corpus_files": found,
            }
        )

    report = {
        "probe": "psychat_gold_source",
        "pinned_commit": PINNED_COMMIT,
        "gold_case_count": len(rows),
        "all_gold_ids_found": True,
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
