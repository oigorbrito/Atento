#!/usr/bin/env python3
"""Verify PsyChat vector-distance semantics before/after the BLOCO I patch."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path


class StubCollection:
    pass


class RecordingClient:
    last_metadata = None
    last_name = None

    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, *, name, metadata=None, **kwargs):
        type(self).last_name = str(name)
        type(self).last_metadata = dict(metadata or {})
        return StubCollection()


class StubSettings:
    def __init__(self, *args, **kwargs):
        pass


class StubEmbeddingGateway:
    def embed(self, *, text):
        return [1.0, 0.0]


def install_stubs() -> None:
    chromadb = types.ModuleType("chromadb")
    chromadb.__path__ = []
    chromadb.PersistentClient = RecordingClient
    sys.modules["chromadb"] = chromadb

    config_mod = types.ModuleType("chromadb.config")
    config_mod.Settings = StubSettings
    sys.modules["chromadb.config"] = config_mod

    requests = types.ModuleType("requests")
    requests.post = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("network forbidden in vector metric probe")
    )
    sys.modules["requests"] = requests

    config = types.ModuleType("config")
    config.ALIBABA_API_KEY = ""
    config.EMBEDDING_MODEL = "text-embedding-v4"
    config.CHROMA_DB_PATH = "/tmp/atento-vector-metric-probe"
    config.COLLECTION_NAME = "psychology_knowledge"
    config.TOP_K_RESULTS = 6
    config.SIMILARITY_THRESHOLD = 0.15
    sys.modules["config"] = config


def load_vector_store(donor_root: Path):
    install_stubs()
    source = donor_root / "core" / "vector_store.py"
    spec = importlib.util.spec_from_file_location("_psychat_vector_metric_probe", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load donor VectorStore")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.VectorStore


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--expect", choices=("upstream", "patched"), required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cls = load_vector_store(args.donor_root)
    if args.expect == "patched":
        cls(embedding_gateway=StubEmbeddingGateway())
    else:
        cls()

    metadata = dict(RecordingClient.last_metadata or {})
    collection_name = RecordingClient.last_name
    explicit_space = metadata.get("hnsw:space")
    index_schema = metadata.get("atento:index_schema")

    if args.expect == "upstream":
        if explicit_space is not None:
            raise AssertionError(
                f"upstream unexpectedly sets hnsw:space={explicit_space!r}"
            )
        if collection_name != "psychology_knowledge":
            raise AssertionError(
                f"unexpected upstream collection name: {collection_name!r}"
            )
        if index_schema is not None:
            raise AssertionError("upstream unexpectedly sets Atento index schema")
        semantic_status = "IMPLICIT_CHROMA_DEFAULT"
    else:
        if explicit_space != "cosine":
            raise AssertionError(
                f"patched donor must set hnsw:space=cosine, got {explicit_space!r}"
            )
        if index_schema != "rag-cosine-v1":
            raise AssertionError(
                f"patched donor must stamp index schema, got {index_schema!r}"
            )
        if collection_name != "psychology_knowledge__rag-cosine-v1":
            raise AssertionError(
                f"patched donor must use a versioned collection name, got {collection_name!r}"
            )
        semantic_status = "EXPLICIT_COSINE_VERSIONED_INDEX"

    report = {
        "metric_version": "psychat-vector-metric-v0.2",
        "runtime_shape": args.expect,
        "collection_name": collection_name,
        "collection_metadata": metadata,
        "index_schema": index_schema,
        "explicit_hnsw_space": explicit_space,
        "similarity_transform_in_donor": "1 - distance",
        "semantic_status": semantic_status,
        "threshold": 0.15,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
