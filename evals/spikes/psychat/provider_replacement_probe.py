#!/usr/bin/env python3
"""Dynamic replacement/lifecycle probe for the patched PsyChat RAG donor.

Run after minimal_fork_patch.py. It loads the real patched donor modules with
stubs for unrelated dependencies and proves that:
- model and embedding providers can be replaced by composition only;
- the same long-lived vector resource can be reused by distinct RAG runtimes;
- mutable conversation state remains isolated per runtime.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import types
from pathlib import Path


class StubCollection:
    def count(self):
        return 0


class StubPersistentClient:
    def __init__(self, *args, **kwargs):
        pass

    def get_or_create_collection(self, *args, **kwargs):
        return StubCollection()


class StubSettings:
    def __init__(self, *args, **kwargs):
        pass


class StubDataProcessor:
    pass


class StubTTSService:
    pass


class RecordingModelGateway:
    def __init__(self, label: str):
        self.label = label
        self.calls = []

    def complete(self, *, purpose, messages, timeout_s):
        self.calls.append(
            {"purpose": purpose, "messages": list(messages), "timeout_s": timeout_s}
        )
        return f"{self.label}:{purpose}"


class RecordingEmbeddingGateway:
    def __init__(self, vector):
        self.vector = list(vector)
        self.calls = []

    def embed(self, *, text):
        self.calls.append(text)
        return list(self.vector)


def install_stubs(donor_root: Path) -> None:
    sys.path.insert(0, str(donor_root))

    chromadb = types.ModuleType("chromadb")
    chromadb.__path__ = []
    chromadb.PersistentClient = StubPersistentClient
    sys.modules["chromadb"] = chromadb

    chromadb_config = types.ModuleType("chromadb.config")
    chromadb_config.Settings = StubSettings
    sys.modules["chromadb.config"] = chromadb_config

    data_pkg = types.ModuleType("data")
    data_pkg.__path__ = []
    sys.modules["data"] = data_pkg
    processor = types.ModuleType("data.processor")
    processor.DataProcessor = StubDataProcessor
    sys.modules["data.processor"] = processor

    tts = types.ModuleType("core.tts_service")
    tts.TTSService = StubTTSService
    sys.modules["core.tts_service"] = tts


def contains_content(history, value: str) -> bool:
    return any(item.get("content") == value for item in history)


def run(donor_root: Path) -> dict:
    install_stubs(donor_root)
    vector_module = importlib.import_module("core.vector_store")
    agent_module = importlib.import_module("agent.psychology_agent")
    rag_module = importlib.import_module("core.rag_system")

    embedding_a = RecordingEmbeddingGateway([1.0, 2.0])
    embedding_b = RecordingEmbeddingGateway([9.0, 8.0])
    vector_a = vector_module.VectorStore(embedding_gateway=embedding_a)
    vector_b = vector_module.VectorStore(embedding_gateway=embedding_b)

    if vector_a.get_embedding("alpha") != [1.0, 2.0]:
        raise AssertionError("embedding gateway A was not used")
    if vector_b.get_embedding("beta") != [9.0, 8.0]:
        raise AssertionError("embedding gateway B was not used")

    model_a = RecordingModelGateway("A")
    model_b = RecordingModelGateway("B")
    agent_a = agent_module.PsychologyAgent(model_gateway=model_a)
    agent_b = agent_module.PsychologyAgent(model_gateway=model_b)

    if agent_a._call_llm("one") != "A:psychat.rag.agent":
        raise AssertionError("model gateway A was not used by PsychologyAgent")
    if agent_b._call_llm("two") != "B:psychat.rag.agent":
        raise AssertionError("model gateway B was not used by PsychologyAgent")

    rag_a = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubDataProcessor(),
        vector_store=vector_a,
        psychology_agent=agent_a,
        tts_service=None,
    )
    rag_b = rag_module.RAGSystem(
        model_gateway=model_b,
        embedding_gateway=embedding_b,
        data_processor=StubDataProcessor(),
        vector_store=vector_b,
        psychology_agent=agent_b,
        tts_service=None,
    )

    response_a = rag_a._generate_response("system", "user", include_history=False)
    response_b = rag_b._generate_response("system", "user", include_history=False)
    if response_a != "A:psychat.rag.response":
        raise AssertionError("RAGSystem did not use model gateway A")
    if response_b != "B:psychat.rag.response":
        raise AssertionError("RAGSystem did not use model gateway B")

    # Lifecycle probe: reuse the long-lived vector resource while keeping
    # conversation state on separate per-session RAGSystem instances.
    session_a = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubDataProcessor(),
        vector_store=vector_a,
        psychology_agent=agent_module.PsychologyAgent(model_gateway=model_a),
        tts_service=None,
    )
    session_b = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubDataProcessor(),
        vector_store=vector_a,
        psychology_agent=agent_module.PsychologyAgent(model_gateway=model_a),
        tts_service=None,
    )

    if session_a.vector_store is not vector_a or session_b.vector_store is not vector_a:
        raise AssertionError("shared long-lived vector resource was not reused")
    if session_a is session_b:
        raise AssertionError("session runtimes must remain distinct")

    result_a = session_a.generate_response("session-a-marker")
    result_b = session_b.generate_response("session-b-marker")
    if not result_a.get("success") or not result_b.get("success"):
        raise AssertionError("patched session runtimes did not execute")

    if not contains_content(session_a.conversation_history, "session-a-marker"):
        raise AssertionError("session A did not retain its own state")
    if contains_content(session_b.conversation_history, "session-a-marker"):
        raise AssertionError("session A state leaked into session B")

    return {
        "metric_version": "psychat-provider-replacement-v0.2",
        "model_provider_swap_pass": True,
        "embedding_provider_swap_pass": True,
        "rag_model_gateway_swap_pass": True,
        "donor_source_edit_required_for_swap": False,
        "files_touched_to_swap_provider_after_boundary": 0,
        "shared_vector_resource_reused": True,
        "distinct_session_runtimes": True,
        "session_state_isolated": True,
        "model_a_call_count": len(model_a.calls),
        "model_b_call_count": len(model_b.calls),
        "embedding_a_call_count": len(embedding_a.calls),
        "embedding_b_call_count": len(embedding_b.calls),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run(args.donor_root)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
