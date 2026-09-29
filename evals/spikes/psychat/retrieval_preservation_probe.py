#!/usr/bin/env python3
"""Compare upstream vs minimally patched PsyChat retrieval mechanics."""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=Path, required=True)
    parser.add_argument("--patched", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    upstream = load(args.upstream)
    patched = load(args.patched)

    if upstream.get("runtime_shape") != "upstream":
        raise AssertionError("upstream report did not execute upstream runtime shape")
    if patched.get("runtime_shape") != "patched":
        raise AssertionError("patched report did not execute patched runtime shape")

    comparisons = {}
    for key in ("multi_query", "forced_rag"):
        same = upstream.get(key) == patched.get(key)
        comparisons[key] = same
        if not same:
            raise AssertionError(
                f"retrieval mechanics changed after minimal fork patch for {key}: "
                f"upstream={upstream.get(key)!r} patched={patched.get(key)!r}"
            )

    report = {
        "probe": "psychat_retrieval_preservation",
        "pinned_commit": upstream.get("pinned_commit"),
        "donor_replacement_test_pass": True,
        "retrieval_mechanics_preserved": all(comparisons.values()),
        "comparisons": comparisons,
        "scope": (
            "deterministic retrieval mechanics only: multi-query search, "
            "dedup/ranking, forced-RAG cache merge and state transitions"
        ),
        "quality_claim": False,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
