#!/usr/bin/env python3
"""Assess whether pinned PsyChat retrieval is reproducible from repository state alone."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.donor_root

    knowledge_dir = root / "resources" / "knowledge"
    knowledge_files = sorted(knowledge_dir.glob("*.txt")) if knowledge_dir.exists() else []
    storage = root / "storage"
    chroma_candidates = [
        storage / "chroma_db",
        root / "chroma_db",
    ]
    index_paths = [str(path.relative_to(root)) for path in chroma_candidates if path.exists()]

    config_path = root / "config.py"
    config_text = config_path.read_text(encoding="utf-8", errors="ignore")
    model_match = re.search(r'^EMBEDDING_MODEL\s*=\s*["\']([^"\']+)["\']', config_text, re.M)
    key_match = re.search(r'^ALIBABA_API_KEY\s*=\s*["\']([^"\']*)["\']', config_text, re.M)

    committed_index_present = bool(index_paths)
    embedding_key_committed_nonempty = bool(key_match and key_match.group(1).strip())

    report = {
        "metric_version": "psychat-retrieval-readiness-v0.1",
        "pinned_commit": PINNED_COMMIT,
        "knowledge_corpus_present": bool(knowledge_files),
        "knowledge_file_count": len(knowledge_files),
        "committed_vector_index_present": committed_index_present,
        "vector_index_paths": index_paths,
        "embedding_model": model_match.group(1) if model_match else None,
        "embedding_key_committed_nonempty": embedding_key_committed_nonempty,
        "index_build_required": not committed_index_present,
        "external_embedding_provider_required_for_rebuild": not committed_index_present,
        "repository_alone_reproduces_semantic_retrieval": (
            bool(knowledge_files) and committed_index_present
        ),
        "interpretation": (
            "The corpus can be source-verified from Git. If no persisted vector "
            "index is committed, semantic retrieval quality requires rebuilding "
            "the index with a configured embedding provider before benchmarking."
        ),
    }

    if not report["knowledge_corpus_present"]:
        raise AssertionError("pinned donor knowledge corpus is missing")

    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
