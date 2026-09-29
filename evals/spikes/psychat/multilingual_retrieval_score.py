#!/usr/bin/env python3
"""Score paired multilingual retrieval results for PsyChat gold documents.

Input results are JSONL rows:
{
  "pair_id": "...",
  "query_language": "pt-BR" | "zh-CN",
  "retrieved_ids": ["...", ...]
}

The scorer is intentionally provider/index agnostic. It measures the semantic
retrieval outcome after a real retrieval runner has produced ranked IDs.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    manifest = load_jsonl(args.manifest)
    results = load_jsonl(args.results)

    expected = {
        (str(row["pair_id"]), str(row["query_language"])): str(row["expected_id"])
        for row in manifest
    }
    actual = {
        (str(row["pair_id"]), str(row["query_language"])): [
            str(x) for x in row.get("retrieved_ids", [])
        ]
        for row in results
    }

    if set(actual) != set(expected):
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise AssertionError(
            f"retrieval result key mismatch; missing={missing} extra={extra}"
        )

    rows = []
    by_language: dict[str, list[float]] = defaultdict(list)
    reciprocal_by_language: dict[str, list[float]] = defaultdict(list)

    for key in sorted(expected):
        pair_id, language = key
        gold = expected[key]
        retrieved = actual[key]
        hit = 1.0 if gold in retrieved else 0.0
        rank = retrieved.index(gold) + 1 if gold in retrieved else None
        reciprocal_rank = (1.0 / rank) if rank else 0.0
        by_language[language].append(hit)
        reciprocal_by_language[language].append(reciprocal_rank)
        rows.append(
            {
                "pair_id": pair_id,
                "query_language": language,
                "expected_id": gold,
                "retrieved_ids": retrieved,
                "hit": bool(hit),
                "rank": rank,
                "reciprocal_rank": reciprocal_rank,
            }
        )

    def avg(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    hit_rate = {lang: avg(vals) for lang, vals in sorted(by_language.items())}
    mrr = {
        lang: avg(vals)
        for lang, vals in sorted(reciprocal_by_language.items())
    }

    if set(hit_rate) != {"pt-BR", "zh-CN"}:
        raise AssertionError(f"expected pt-BR and zh-CN results, got {hit_rate}")

    report = {
        "metric_version": "psychat-multilingual-retrieval-v0.1",
        "pair_count": len(expected) // 2,
        "query_count": len(expected),
        "hit_rate_by_language": hit_rate,
        "mrr_by_language": mrr,
        "zh_minus_pt_hit_rate_gap": hit_rate["zh-CN"] - hit_rate["pt-BR"],
        "zh_minus_pt_mrr_gap": mrr["zh-CN"] - mrr["pt-BR"],
        "interpretation": (
            "A positive zh-minus-pt gap indicates the same pinned gold documents "
            "are easier to retrieve from source-language queries than pt-BR queries. "
            "This is a feature-quality metric, not a chassis metric."
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
