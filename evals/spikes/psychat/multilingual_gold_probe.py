#!/usr/bin/env python3
"""Validate paired multilingual PsyChat retrieval golds against pinned corpus."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def exact_id_present(path: Path, doc_id: str) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return re.search(rf"(?m)^ID:\s*{re.escape(doc_id)}\s*$", text) is not None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rows = load_jsonl(args.manifest)
    pairs: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        pairs[str(row["pair_id"])].append(row)

    if len(pairs) != 4:
        raise AssertionError(f"expected 4 multilingual gold pairs, got {len(pairs)}")

    validated = []
    for pair_id, items in sorted(pairs.items()):
        langs = {str(item["query_language"]) for item in items}
        if langs != {"pt-BR", "zh-CN"}:
            raise AssertionError(f"{pair_id}: expected pt-BR + zh-CN, got {sorted(langs)}")
        ids = {str(item["expected_id"]) for item in items}
        sources = {str(item["source_file"]) for item in items}
        commits = {str(item["gold_commit"]) for item in items}
        if len(ids) != 1 or len(sources) != 1:
            raise AssertionError(f"{pair_id}: pair must share one gold ID/source")
        if commits != {PINNED_COMMIT}:
            raise AssertionError(f"{pair_id}: commit mismatch")

        doc_id = next(iter(ids))
        source = next(iter(sources))
        source_path = args.donor_root / source
        if not source_path.exists():
            raise AssertionError(f"{pair_id}: source file missing: {source}")
        if not exact_id_present(source_path, doc_id):
            raise AssertionError(f"{pair_id}: exact ID {doc_id} missing in {source}")

        validated.append(
            {
                "pair_id": pair_id,
                "expected_id": doc_id,
                "source_file": source,
                "languages": sorted(langs),
            }
        )

    report = {
        "metric_version": "psychat-multilingual-gold-v0.1",
        "pinned_commit": PINNED_COMMIT,
        "pair_count": len(validated),
        "query_count": len(rows),
        "all_exact_gold_ids_verified": True,
        "paired_language_control": True,
        "quality_claim": False,
        "purpose": (
            "Future real retrieval can compare pt-BR vs zh-CN recall for the same "
            "gold ID, separating general retrieval failure from multilingual failure."
        ),
        "pairs": validated,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
