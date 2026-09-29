#!/usr/bin/env python3
"""Dynamic provider-swap probe for the minimally patched PsyChat RAG donor.

Run only after minimal_fork_patch.py has modified the pinned donor worktree.
External provider/network dependencies are replaced with deterministic fakes.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path


class FakeModelGateway:
    def __init__(self, value: str) -> None:
        self.value = value
        self.calls = []

    def complete(self, *, purpose, messages, timeout_s):
        self.calls.append(
            {
                "purpose": purpose,
                "messages": messages,
                "timeout_s": timeout_s,
            }
        )
        return self.value


class FakeEmbeddingGateway:
    def __init__(self, vector):
        self.vector = list(vector)
        self.calls = []

    def embed(self, *, text):
        self.calls.append(text)
        return list(self.vector)


class FakeCollection:
    pass


class FakeClient:
    def get_or_create_collection(self, **kwargs):
        return FakeCollection()


def install_vector_store_stubs() -> None:
    chromadb = types.ModuleType("chromadb")
    chromadb.PersistentClient = lambda **kwargs: FakeClient()
    sys.modules["chromadb"] = chromadb

    chromadb_config = types.ModuleType("chromadb.config")

    class Settings:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

    chromadb_config.Settings = Settings
    sys.modules["chromadb.config"] = chromadb_config

    config = types.ModuleType("config")
    config.CHROMA_DB_PATH = "/tmp/atento-psychat-probe"
    config.COLLECTION_NAME = "probe"
    config.TOP_K_RESULTS = 6
    config.SIMILARITY_THRESHOLD = 0.15
    sys.modules["config"] = config


def install_agent_config_stub() -> None:
    config = types.ModuleType("config")
    sys.modules["config"] = config


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    agent_path = args.donor_root / "agent" / "psychology_agent.py"
    vector_path = args.donor_root / "core" / "vector_store.py"

    install_agent_config_stub()
    agent_module = load_module("_psychat_patched_agent", agent_path)
    model_a = FakeModelGateway("model-a")
    model_b = FakeModelGateway("model-b")
    agent_a = agent_module.PsychologyAgent(model_gateway=model_a)
    agent_b = agent_module.PsychologyAgent(model_gateway=model_b)
    result_a = agent_a._call_llm("probe")
    result_b = agent_b._call_llm("probe")
    if result_a != "model-a" or result_b != "model-b":
        raise AssertionError(
            f"model provider swap failed: {result_a!r}, {result_b!r}"
        )

    install_vector_store_stubs()
    vector_module = load_module("_psychat_patched_vector_store", vector_path)
    embedding_a = FakeEmbeddingGateway([1.0, 2.0])
    embedding_b = FakeEmbeddingGateway([3.0, 4.0])
    vector_a = vector_module.VectorStore(embedding_gateway=embedding_a)
    vector_b = vector_module.VectorStore(embedding_gateway=embedding_b)
    emb_a = vector_a.get_embedding("probe")
    emb_b = vector_b.get_embedding("probe")
    if emb_a != [1.0, 2.0] or emb_b != [3.0, 4.0]:
        raise AssertionError(
            f"embedding provider swap failed: {emb_a!r}, {emb_b!r}"
        )

    report = {
        "probe": "psychat_patched_provider_swap",
        "model_provider_swap_pass": True,
        "embedding_provider_swap_pass": True,
        "donor_source_edits_during_swap": 0,
        "model_gateway_calls": len(model_a.calls) + len(model_b.calls),
        "embedding_gateway_calls": len(embedding_a.calls) + len(embedding_b.calls),
        "network_calls_required": False,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
