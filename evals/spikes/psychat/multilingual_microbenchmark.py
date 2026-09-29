#!/usr/bin/env python3
"""Small real-evidence multilingual retrieval benchmark for pinned PsyChat.

This benchmark intentionally does NOT rebuild the full PsyChat Chroma index.
Instead it extracts the four pinned gold conversations from the donor corpus,
adds deterministic same-corpus distractors, embeds the resulting microcorpus,
and compares pt-BR vs zh-CN retrieval for the exact same gold IDs.

It measures feature quality of the embedding/retrieval path. It is not a
Chassis Fitness metric.

Required environment:
- ALIBABA_API_KEY

Optional environment:
- PSYCHAT_EMBEDDING_MODEL (default: text-embedding-v4)
- PSYCHAT_EMBEDDING_URL
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Iterable


DEFAULT_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings"
DEFAULT_MODEL = "text-embedding-v4"
RECORD_RE = re.compile(
    r"(?ms)^ID:\s*(\d+)\s*$\s*^##\s*$\s*(.*?)(?=^##\s*$\s*^ID:|\Z)"
)


def load_jsonl(path: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def parse_records(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return {
        match.group(1): match.group(2).strip()
        for match in RECORD_RE.finditer(text)
    }


def stable_distractors(ids: Iterable[str], *, exclude: set[str], limit: int) -> list[str]:
    candidates = [doc_id for doc_id in ids if doc_id not in exclude]
    candidates.sort(
        key=lambda doc_id: hashlib.sha256(doc_id.encode("utf-8")).hexdigest()
    )
    return candidates[:limit]


class DashScopeEmbeddingGateway:
    def __init__(self, *, api_key: str, model: str, url: str) -> None:
        if not api_key.strip():
            raise ValueError("ALIBABA_API_KEY is required")
        self.api_key = api_key
        self.model = model
        self.url = url

    def embed(self, text: str) -> list[float]:
        payload = json.dumps(
            {
                "model": self.model,
                "input": text,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            self.url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                body = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(
                f"embedding provider HTTP {exc.code}: {detail[:500]}"
            ) from exc

        data = body.get("data") or []
        if not data or not isinstance(data[0].get("embedding"), list):
            raise RuntimeError("embedding provider returned no vector")
        return [float(value) for value in data[0]["embedding"]]


def cosine(a: list[float], b: list[float]) -> float:
    if len(a) != len(b) or not a:
        raise ValueError("embedding dimensions must be equal and non-empty")
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    if na == 0.0 or nb == 0.0:
        return 0.0
    return dot / (na * nb)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--distractors", type=int, default=16)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--max-document-chars", type=int, default=1800)
    args = parser.parse_args()

    if args.distractors < 1:
        raise ValueError("--distractors must be >= 1")
    if args.top_k < 1:
        raise ValueError("--top-k must be >= 1")

    manifest = load_jsonl(args.manifest)
    expected_ids = {str(row["expected_id"]) for row in manifest}
    source_files = sorted({str(row["source_file"]) for row in manifest})

    source_records: dict[str, dict[str, str]] = {}
    all_records: dict[str, str] = {}
    source_of: dict[str, str] = {}
    for source in source_files:
        records = parse_records(args.donor_root / source)
        source_records[source] = records
        for doc_id, content in records.items():
            if doc_id not in all_records:
                all_records[doc_id] = content
                source_of[doc_id] = source

    missing = sorted(expected_ids - set(all_records))
    if missing:
        raise AssertionError(f"gold IDs missing from parsed donor corpus: {missing}")

    distractor_ids = stable_distractors(
        all_records.keys(),
        exclude=expected_ids,
        limit=args.distractors,
    )
    corpus_ids = sorted(expected_ids) + distractor_ids

    api_key = os.environ.get("ALIBABA_API_KEY", "")
    model = os.environ.get("PSYCHAT_EMBEDDING_MODEL", DEFAULT_MODEL)
    url = os.environ.get("PSYCHAT_EMBEDDING_URL", DEFAULT_URL)
    gateway = DashScopeEmbeddingGateway(
        api_key=api_key,
        model=model,
        url=url,
    )

    document_vectors = {}
    for doc_id in corpus_ids:
        text = all_records[doc_id][: args.max_document_chars]
        document_vectors[doc_id] = gateway.embed(text)

    rows = []
    hits_by_language: dict[str, list[float]] = defaultdict(list)
    reciprocal_by_language: dict[str, list[float]] = defaultdict(list)

    for item in manifest:
        pair_id = str(item["pair_id"])
        language = str(item["query_language"])
        gold = str(item["expected_id"])
        query = str(item["query"])

        query_vector = gateway.embed(query)
        ranked = sorted(
            (
                (doc_id, cosine(query_vector, vector))
                for doc_id, vector in document_vectors.items()
            ),
            key=lambda pair: pair[1],
            reverse=True,
        )
        ranked_ids = [doc_id for doc_id, _ in ranked]
        rank = ranked_ids.index(gold) + 1 if gold in ranked_ids else None
        hit_at_k = bool(rank and rank <= args.top_k)
        reciprocal_rank = (1.0 / rank) if rank else 0.0

        hits_by_language[language].append(1.0 if hit_at_k else 0.0)
        reciprocal_by_language[language].append(reciprocal_rank)
        rows.append(
            {
                "pair_id": pair_id,
                "query_language": language,
                "expected_id": gold,
                "source_file": source_of[gold],
                "rank": rank,
                "hit_at_k": hit_at_k,
                "top_k": [
                    {"id": doc_id, "similarity": score}
                    for doc_id, score in ranked[: args.top_k]
                ],
                "reciprocal_rank": reciprocal_rank,
            }
        )

    def average(values: list[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    hit_rate = {
        language: average(values)
        for language, values in sorted(hits_by_language.items())
    }
    mrr = {
        language: average(values)
        for language, values in sorted(reciprocal_by_language.items())
    }
    if set(hit_rate) != {"pt-BR", "zh-CN"}:
        raise AssertionError(f"expected pt-BR + zh-CN results, got {hit_rate}")

    report = {
        "metric_version": "psychat-multilingual-microbenchmark-v0.1",
        "quality_claim": True,
        "scope": (
            "four real pinned PsyChat gold conversations plus deterministic "
            "same-corpus distractors; not the full Chroma production index"
        ),
        "embedding_model": model,
        "embedding_url": url,
        "gold_document_count": len(expected_ids),
        "distractor_count": len(distractor_ids),
        "microcorpus_document_count": len(corpus_ids),
        "top_k": args.top_k,
        "hit_rate_by_language": hit_rate,
        "mrr_by_language": mrr,
        "zh_minus_pt_hit_rate_gap": hit_rate["zh-CN"] - hit_rate["pt-BR"],
        "zh_minus_pt_mrr_gap": mrr["zh-CN"] - mrr["pt-BR"],
        "rows": rows,
        "limitations": [
            "Microcorpus benchmark, not full-corpus Chroma retrieval.",
            "Measures embedding semantic separation and multilingual transfer on four pinned golds.",
            "Does not measure PsyChat answer-generation quality.",
        ],
    }

    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
