#!/usr/bin/env python3
"""Verify PsyChat vector-distance semantics before/after the BLOCO I patch."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import tempfile
import types
from pathlib import Path


class StubCollection:
    def __init__(self, metadata=None):
        self.metadata = dict(metadata or {})
        self.upsert_calls = []
        self.ids = set()

    def upsert(self, **kwargs):
        self.upsert_calls.append(dict(kwargs))
        self.ids.update(str(item) for item in kwargs.get("ids", []))

    def count(self):
        return len(self.ids)


class RecordingClient:
    collections = {}
    last_metadata = None
    last_name = None
    last_deleted_name = None
    last_created_name = None
    last_created_metadata = None
    last_collection = None

    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, *, name, metadata=None, **kwargs):
        type(self).last_name = str(name)
        if name not in type(self).collections:
            type(self).collections[name] = StubCollection(metadata)
        collection = type(self).collections[name]
        type(self).last_metadata = dict(collection.metadata or {})
        type(self).last_collection = collection
        return collection

    def get_collection(self, *, name, **kwargs):
        if name not in type(self).collections:
            raise KeyError(name)
        collection = type(self).collections[name]
        type(self).last_name = str(name)
        type(self).last_metadata = dict(collection.metadata or {})
        type(self).last_collection = collection
        return collection

    def delete_collection(self, name):
        type(self).last_deleted_name = str(name)
        type(self).collections.pop(name, None)

    def create_collection(self, *, name, metadata=None, **kwargs):
        if name in type(self).collections:
            raise ValueError(f"collection already exists: {name}")
        type(self).last_created_name = str(name)
        type(self).last_created_metadata = dict(metadata or {})
        collection = StubCollection(metadata)
        type(self).collections[name] = collection
        type(self).last_collection = collection
        return collection


class StubSettings:
    def __init__(self, *args, **kwargs):
        pass


class StubEmbeddingGateway:
    index_identity = "stub:text-embedding-v4:v1"

    def embed(self, *, text):
        return [1.0, 0.0]


class PartialFailureEmbeddingGateway:
    index_identity = StubEmbeddingGateway.index_identity

    def embed(self, *, text):
        if text == "bad":
            return []
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
    config.CHROMA_DB_PATH = tempfile.mkdtemp(prefix="atento-vector-metric-probe-")
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
    corpus_identity = metadata.get("atento:corpus_identity")

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
        expected_corpus = "psychat@5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"
        if corpus_identity != expected_corpus:
            raise AssertionError(
                f"patched donor must persist corpus identity, got {corpus_identity!r}"
            )

        alternate = cls(
            embedding_gateway=StubEmbeddingGateway(),
            corpus_identity="psychat@alternate-corpus",
        )
        if alternate.collection_name == collection_name:
            raise AssertionError(
                "different corpus identities must not reuse the same persisted collection"
            )

        initial_collection = store.collection
        sample_doc = {
            "content": "sample",
            "source": "sample.txt",
            "size": 6,
            "type": "psychology_qa",
            "topic": "情绪",
            "qa_id": "sample-1",
        }
        if not store.add_documents([sample_doc]):
            raise AssertionError("first patched index build failed")
        if not store.add_documents([sample_doc]):
            raise AssertionError("same-identity rebuild failed")
        if len(initial_collection.upsert_calls) != 2:
            raise AssertionError(
                "same-identity rebuild must use upsert on both builds, got "
                f"{len(initial_collection.upsert_calls)} calls"
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
        if recreated.get("atento:corpus_identity") != corpus_identity:
            raise AssertionError(
                f"recreated collection lost corpus identity: {recreated!r}"
            )

        info = store.get_collection_info()

        original_corpus_metadata = store.collection.metadata["atento:corpus_identity"]
        store.collection.metadata["atento:corpus_identity"] = "tampered-corpus"
        try:
            store.get_collection_info()
        except RuntimeError as exc:
            if "metadata mismatch" not in str(exc):
                raise
        else:
            raise AssertionError(
                "persisted collection metadata mismatch was not rejected"
            )
        finally:
            store.collection.metadata["atento:corpus_identity"] = original_corpus_metadata

        active_before_atomic = store.collection_name
        if not store.rebuild_documents([sample_doc]):
            raise AssertionError("atomic staging rebuild did not promote healthy generation")
        promoted_name = store.collection_name
        if promoted_name == active_before_atomic:
            raise AssertionError("healthy staging rebuild did not switch generations")
        if not store.pointer_path.exists():
            raise AssertionError("atomic staging rebuild did not write active pointer")
        promoted_pointer = json.loads(
            store.pointer_path.read_text(encoding="utf-8")
        )["active_collection"]
        if promoted_pointer != promoted_name:
            raise AssertionError("active pointer does not match promoted generation")

        reopened = cls(embedding_gateway=StubEmbeddingGateway())
        if reopened.collection_name != promoted_name:
            raise AssertionError(
                "new VectorStore instance did not reopen promoted generation"
            )
        if reopened.collection is not store.collection:
            raise AssertionError(
                "new VectorStore instance resolved a different active collection"
            )

        pointer_backup = store.pointer_path.read_text(encoding="utf-8")
        store.pointer_path.write_text("{not-json", encoding="utf-8")
        try:
            cls(embedding_gateway=StubEmbeddingGateway())
        except RuntimeError as exc:
            if "invalid vector index pointer" not in str(exc):
                raise
        else:
            raise AssertionError("corrupt active pointer did not fail closed")
        finally:
            store.pointer_path.write_text(pointer_backup, encoding="utf-8")

        healthy_gateway = store.embedding_gateway
        store.embedding_gateway = PartialFailureEmbeddingGateway()
        partial_docs = [
            sample_doc,
            {
                "content": "bad",
                "source": "bad.txt",
                "size": 3,
                "type": "psychology_qa",
                "topic": "情绪",
                "qa_id": "bad-1",
            },
        ]
        if store.rebuild_documents(partial_docs):
            raise AssertionError("partial staging rebuild must not be promoted")
        store.embedding_gateway = healthy_gateway
        pointer_after_failure = json.loads(
            store.pointer_path.read_text(encoding="utf-8")
        )["active_collection"]
        if pointer_after_failure != promoted_name:
            raise AssertionError(
                "failed staging rebuild changed active generation pointer"
            )
        if store.collection_name != promoted_name:
            raise AssertionError(
                "failed staging rebuild replaced in-memory active generation"
            )

        expected_info = {
            "name": collection_name,
            "index_schema": "rag-cosine-v1",
            "embedding_identity": StubEmbeddingGateway.index_identity,
            "corpus_identity": corpus_identity,
        }
        for key, expected in expected_info.items():
            if info.get(key) != expected:
                raise AssertionError(
                    f"collection info missing observable {key}: {info!r}"
                )

    report = {
        "metric_version": "psychat-vector-metric-v0.10",
        "runtime_shape": args.expect,
        "collection_name": collection_name,
        "collection_metadata": metadata,
        "index_schema": index_schema,
        "embedding_identity": embedding_identity,
        "corpus_identity": corpus_identity,
        "corpus_identity_isolated": (
            args.expect != "patched"
            or alternate.collection_name != collection_name
        ),
        "same_identity_rebuild_uses_upsert": (
            args.expect != "patched"
            or len(initial_collection.upsert_calls) == 2
        ),
        "collection_info_exposes_index_identity": (
            args.expect != "patched"
            or all(
                store.get_collection_info().get(key)
                for key in (
                    "name",
                    "index_schema",
                    "embedding_identity",
                    "corpus_identity",
                )
            )
        ),
        "persisted_collection_metadata_validation_pass": (
            args.expect != "patched" or True
        ),
        "collection_contract_mismatch_fails_closed": (
            args.expect != "patched" or True
        ),
        "atomic_generation_promotion_pass": (
            args.expect != "patched" or promoted_pointer == promoted_name
        ),
        "partial_staging_never_promoted": (
            args.expect != "patched" or pointer_after_failure == promoted_name
        ),
        "promoted_generation_survives_restart": (
            args.expect != "patched" or reopened.collection_name == promoted_name
        ),
        "corrupt_pointer_fails_closed": (
            args.expect != "patched" or True
        ),
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
                and (RecordingClient.last_created_metadata or {}).get("atento:corpus_identity") == corpus_identity
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
