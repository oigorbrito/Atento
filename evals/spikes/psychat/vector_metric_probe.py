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
    last_deleted_name = None
    last_created_name = None
    last_created_metadata = None

    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, *, name, metadata=None, **kwargs):
        type(self).last_name = str(name)
        type(self).last_metadata = dict(metadata or {})
        return StubCollection()

    def delete_collection(self, name):
        type(self).last_deleted_name = str(name)

    def create_collection(self, *, name, metadata=None, **kwargs):
        type(self).last_created_name = str(name)
        type(self).last_created_metadata = dict(metadata or {})
        return StubCollection()


class StubSettings:
    def __init__(self, *args, **kwargs):
        pass


class StubEmbeddingGateway:
    index_identity = "stub:text-embedding-v4:v1"

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
        store = cls(embedding_gateway=StubEmbeddingGateway())
    else:
        store = cls()

    metadata = dict(RecordingClient.last_metadata or {})
    collection_name = RecordingClient.last_name
    explicit_space = metadata.get("hnsw:space")
    index_schema = metadata.get("atento:index_schema")
    embedding_identity = metadata.get("atento:embedding_identity")

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
        expected_prefix = "psychology_knowledge__rag-cosine-v1__"
        if not collection_name.startswith(expected_prefix):
            raise AssertionError(
                "patched donor must namespace the versioned collection by "
                f"embedding identity, got {collection_name!r}"
            )
        if embedding_identity != StubEmbeddingGateway.index_identity:
            raise AssertionError(
                "patched donor must persist embedding identity metadata, got "
                f"{embedding_identity!r}"
            )
        semantic_status = "EXPLICIT_COSINE_VERSIONED_INDEX"

        if not store.clear_collection():
            raise AssertionError("patched clear_collection failed")
        if RecordingClient.last_deleted_name != collection_name:
            raise AssertionError(
                "patched clear_collection deleted the wrong collection: "
                f"{RecordingClient.last_deleted_name!r}"
            )
        if RecordingClient.last_created_name != collection_name:
            raise AssertionError(
                "patched clear_collection recreated the wrong collection: "
                f"{RecordingClient.last_created_name!r}"
            )
        recreated = dict(RecordingClient.last_created_metadata or {})
        if recreated.get("hnsw:space") != "cosine":
            raise AssertionError(
                f"recreated collection lost cosine metric: {recreated!r}"
            )
        if recreated.get("atento:index_schema") != "rag-cosine-v1":
            raise AssertionError(
                f"recreated collection lost index schema: {recreated!r}"
            )
        if recreated.get("atento:embedding_identity") != StubEmbeddingGateway.index_identity:
            raise AssertionError(
                f"recreated collection lost embedding identity: {recreated!r}"
            )

    report = {
        "metric_version": "psychat-vector-metric-v0.4",
        "runtime_shape": args.expect,
        "collection_name": collection_name,
        "collection_metadata": metadata,
        "index_schema": index_schema,
        "embedding_identity": embedding_identity,
        "explicit_hnsw_space": explicit_space,
        "similarity_transform_in_donor": "1 - distance",
        "semantic_status": semantic_status,
        "clear_collection_contract_preserved": (
            args.expect != "patched"
            or (
                RecordingClient.last_deleted_name == collection_name
                and RecordingClient.last_created_name == collection_name
                and (RecordingClient.last_created_metadata or {}).get("hnsw:space") == "cosine"
                and (RecordingClient.last_created_metadata or {}).get("atento:index_schema") == "rag-cosine-v1"
                and (RecordingClient.last_created_metadata or {}).get("atento:embedding_identity") == StubEmbeddingGateway.index_identity
            )
        ),
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
