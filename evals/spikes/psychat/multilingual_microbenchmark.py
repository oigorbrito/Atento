#!/usr/bin/env python3
"""Chunk-faithful multilingual retrieval microbenchmark for pinned PsyChat.

The benchmark uses real pinned PsyChat conversations and reproduces the donor's
2–3 turn (up to 6 utterance) chunk granularity. It compares pt-BR vs zh-CN
queries against the exact same gold QA IDs.

It does not rebuild the full Chroma index and is not a Chassis Fitness metric.

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


def split_dialogue_like_psychat(content: str) -> list[str]:
    """Mirror DataProcessor._split_dialogue_by_turns() at 6 utterances."""
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    chunks: list[str] = []
    current: list[str] = []
    turn_count = 0

    for line in lines:
        current.append(line)
        if line.startswith("用户:") or line.startswith("助手:"):
            turn_count += 1
            if turn_count >= 6:
                chunks.append("\n".join(current))
                current = []
                turn_count = 0

    if current:
        chunks.append("\n".join(current))
    return chunks


def stable_distractors(
    ids: Iterable[str],
    *,
    exclude: set[str],
    limit: int,
) -> list[str]:
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
    parser.add_argument("--top-k", type=int, default=6)
    parser.add_argument("--max-document-chars", type=int, default=1800)
    args = parser.parse_args()

    if args.distractors < 1:
        raise ValueError("--distractors must be >= 1")
    if args.top_k < 1:
        raise ValueError("--top-k must be >= 1")

    manifest = load_jsonl(args.manifest)
    expected_ids = {str(row["expected_id"]) for row in manifest}
    source_files = sorted({str(row["source_file"]) for row in manifest})

    all_records: dict[str, str] = {}
    source_of: dict[str, str] = {}
    for source in source_files:
        for doc_id, record in parse_records(args.donor_root / source).items():
            if doc_id not in all_records:
                all_records[doc_id] = record
                source_of[doc_id] = source

    missing = sorted(expected_ids - set(all_records))
    if missing:
        raise AssertionError(f"gold IDs missing from parsed donor corpus: {missing}")

    distractor_ids = stable_distractors(
        all_records.keys(),
        exclude=expected_ids,
        limit=args.distractors,
    )
    selected_record_ids = sorted(expected_ids) + distractor_ids

    chunks: list[dict] = []
    for doc_id in selected_record_ids:
        for index, chunk_text in enumerate(
            split_dialogue_like_psychat(all_records[doc_id])
        ):
            chunks.append(
                {
                    "chunk_id": f"{doc_id}:{index}",
                    "qa_id": doc_id,
                    "source_file": source_of[doc_id],
                    "content": chunk_text[: args.max_document_chars],
                }
            )

    gold_chunk_counts = {
        doc_id: sum(chunk["qa_id"] == doc_id for chunk in chunks)
        for doc_id in sorted(expected_ids)
    }
    if any(count == 0 for count in gold_chunk_counts.values()):
        raise AssertionError(f"gold record produced no chunks: {gold_chunk_counts}")

    api_key = os.environ.get("ALIBABA_API_KEY", "")
    model = os.environ.get("PSYCHAT_EMBEDDING_MODEL", DEFAULT_MODEL)
    url = os.environ.get("PSYCHAT_EMBEDDING_URL", DEFAULT_URL)
    gateway = DashScopeEmbeddingGateway(
        api_key=api_key,
        model=model,
        url=url,
    )

    vectors = {
        chunk["chunk_id"]: gateway.embed(chunk["content"])
        for chunk in chunks
    }
    chunk_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}

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
                (chunk_id, cosine(query_vector, vector))
                for chunk_id, vector in vectors.items()
            ),
            key=lambda pair: pair[1],
            reverse=True,
        )

        gold_ranks = [
            index
            for index, (chunk_id, _score) in enumerate(ranked, start=1)
            if chunk_by_id[chunk_id]["qa_id"] == gold
        ]
        rank = min(gold_ranks) if gold_ranks else None
        hit_at_k = bool(rank and rank <= args.top_k)
        reciprocal_rank = (1.0 / rank) if rank else 0.0

        hits_by_language[language].append(1.0 if hit_at_k else 0.0)
        reciprocal_by_language[language].append(reciprocal_rank)
        rows.append(
            {
                "pair_id": pair_id,
                "query_language": language,
                "expected_id": gold,
                "gold_chunk_count": gold_chunk_counts[gold],
                "best_gold_chunk_rank": rank,
                "hit_at_k": hit_at_k,
                "top_k": [
                    {
                        "chunk_id": chunk_id,
                        "qa_id": chunk_by_id[chunk_id]["qa_id"],
                        "source_file": chunk_by_id[chunk_id]["source_file"],
                        "similarity": score,
                    }
                    for chunk_id, score in ranked[: args.top_k]
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
        "metric_version": "psychat-multilingual-microbenchmark-v0.2",
        "quality_claim": True,
        "scope": (
            "real pinned PsyChat records split at donor-equivalent 6-utterance "
            "chunk granularity plus deterministic same-corpus distractor records"
        ),
        "embedding_model": model,
        "embedding_url": url,
        "gold_record_count": len(expected_ids),
        "gold_chunk_counts": gold_chunk_counts,
        "distractor_record_count": len(distractor_ids),
        "microcorpus_chunk_count": len(chunks),
        "top_k": args.top_k,
        "hit_rate_by_language": hit_rate,
        "mrr_by_language": mrr,
        "zh_minus_pt_hit_rate_gap": hit_rate["zh-CN"] - hit_rate["pt-BR"],
        "zh_minus_pt_mrr_gap": mrr["zh-CN"] - mrr["pt-BR"],
        "rows": rows,
        "limitations": [
            "Microcorpus benchmark, not the full Chroma production index.",
            "Uses donor-equivalent chunk granularity but cosine ranking rather than Chroma's configured/default distance implementation.",
            "Measures embedding multilingual retrieval, not answer-generation quality.",
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
