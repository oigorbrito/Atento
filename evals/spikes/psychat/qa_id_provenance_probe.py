#!/usr/bin/env python3
"""Measure QA-ID provenance through the pinned PsyChat DataProcessor.

The probe dynamically loads the donor's real data/processor.py while stubbing
only tiktoken/config dependencies that are irrelevant to
split_psychology_qa_pairs(). It can run both before and after the BLOCO I patch.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import types
from collections import Counter
from pathlib import Path

PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"
GOLD_IDS = {"328", "350", "1864", "1882"}
ID_RE = re.compile(r"(?m)^ID:\s*(\d+)\s*$")


def install_stubs(knowledge_dir: Path) -> None:
    tiktoken = types.ModuleType("tiktoken")
    tiktoken.get_encoding = lambda name: object()
    sys.modules["tiktoken"] = tiktoken

    config = types.ModuleType("config")
    config.KNOWLEDGE_DIR = str(knowledge_dir)
    sys.modules["config"] = config


def load_processor(donor_root: Path):
    knowledge_dir = donor_root / "resources" / "knowledge"
    install_stubs(knowledge_dir)
    source = donor_root / "data" / "processor.py"
    spec = importlib.util.spec_from_file_location("_psychat_processor_probe", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load donor DataProcessor")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.DataProcessor


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument(
        "--expect",
        choices=("broken", "preserved", "any"),
        default="any",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    knowledge_dir = args.donor_root / "resources" / "knowledge"
    processor_cls = load_processor(args.donor_root)
    processor = processor_cls.__new__(processor_cls)

    rows = []
    raw_ids = set()
    chunk_ids = []
    unknown_chunks = 0
    total_chunks = 0

    for path in sorted(knowledge_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_raw_ids = set(ID_RE.findall(text))
        raw_ids.update(file_raw_ids)

        chunks = processor.split_psychology_qa_pairs(text, path.name)
        file_chunk_ids = [str(chunk.get("qa_id", "unknown")) for chunk in chunks]
        file_unknown = sum(doc_id == "unknown" for doc_id in file_chunk_ids)
        total_chunks += len(file_chunk_ids)
        unknown_chunks += file_unknown
        chunk_ids.extend(file_chunk_ids)

        rows.append(
            {
                "file": path.name,
                "raw_record_id_count": len(file_raw_ids),
                "chunk_count": len(file_chunk_ids),
                "unknown_chunk_count": file_unknown,
                "known_chunk_count": len(file_chunk_ids) - file_unknown,
            }
        )

    known_ids = {doc_id for doc_id in chunk_ids if doc_id != "unknown"}
    gold_survival = {doc_id: doc_id in known_ids for doc_id in sorted(GOLD_IDS)}
    missing_raw_ids = sorted(raw_ids - known_ids)
    unknown_ratio = unknown_chunks / total_chunks if total_chunks else 0.0

    if args.expect == "broken":
        if unknown_chunks != total_chunks:
            raise AssertionError(
                f"expected all chunks to lose QA ID upstream, got "
                f"{unknown_chunks}/{total_chunks} unknown"
            )
    elif args.expect == "preserved":
        if unknown_chunks:
            raise AssertionError(
                f"patched parser still emitted {unknown_chunks} unknown chunks"
            )
        if missing_raw_ids:
            raise AssertionError(
                f"patched parser did not preserve raw IDs: {missing_raw_ids[:20]}"
            )
        if not all(gold_survival.values()):
            raise AssertionError(f"patched parser lost gold IDs: {gold_survival}")

    report = {
        "metric_version": "psychat-qa-id-provenance-v0.1",
        "pinned_commit": PINNED_COMMIT,
        "expectation": args.expect,
        "knowledge_file_count": len(rows),
        "raw_record_id_count": len(raw_ids),
        "chunk_count": total_chunks,
        "unknown_chunk_count": unknown_chunks,
        "unknown_chunk_ratio": unknown_ratio,
        "known_unique_qa_id_count": len(known_ids),
        "missing_raw_id_count": len(missing_raw_ids),
        "gold_id_survival": gold_survival,
        "files": rows,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
