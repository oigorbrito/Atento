#!/usr/bin/env python3
"""Runtime probe for the patched PsyChat BLOCO I donor surface.

Run after minimal_fork_patch.py. The probe loads the real patched donor modules
with deterministic stubs for unrelated external dependencies and verifies:
- model provider calls flow through the injected ModelGateway;
- embeddings flow through the injected EmbeddingGateway;
- RAGSystem accepts reusable long-lived resources;
- mutable conversation state remains on the per-call RAGSystem runtime.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path


class FakeModelGateway:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def complete(self, *, purpose: str, messages: list[dict], timeout_s: float) -> str:
        self.calls.append(
            {
                "purpose": purpose,
                "messages": list(messages),
                "timeout_s": timeout_s,
            }
        )
        if purpose == "psychat.rag.agent":
            return "NO"
        return "gateway-response"


class FakeEmbeddingGateway:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def embed(self, *, text: str) -> list[float]:
        self.calls.append(text)
        return [0.1, 0.2, 0.3]


class FakeDataProcessor:
    pass


class FakeVectorResource:
    def search(self, *args, **kwargs):
        return []

    def get_collection_info(self):
        return {"document_count": 1}


class FakeAgent:
    def analyze_user_input(
        self,
        user_message,
        conversation_history,
        vector_store,
        force_retrieval=False,
    ):
        return {
            "need_rag": False,
            "topics": [],
            "topic": None,
            "search_queries": [],
            "search_query": None,
            "original_message": user_message,
            "forced": force_retrieval,
        }


def install_support_modules() -> None:
    config = types.ModuleType("config")
    config.CHROMA_DB_PATH = "/tmp/unused-chroma"
    config.COLLECTION_NAME = "unused"
    config.TOP_K_RESULTS = 5
    config.SIMILARITY_THRESHOLD = 0.0
    config.MAX_NO_RAG_ROUNDS = 999
    config.TTS_ENABLED = False
    sys.modules["config"] = config

    chromadb = types.ModuleType("chromadb")

    class PersistentClient:
        def __init__(self, *args, **kwargs):
            raise AssertionError("VectorStore __init__ must not run in this probe")

    chromadb.PersistentClient = PersistentClient
    sys.modules["chromadb"] = chromadb

    chromadb_config = types.ModuleType("chromadb.config")

    class Settings:
        def __init__(self, *args, **kwargs):
            pass

    chromadb_config.Settings = Settings
    sys.modules["chromadb.config"] = chromadb_config

    data_pkg = types.ModuleType("data")
    data_pkg.__path__ = []
    sys.modules["data"] = data_pkg
    data_processor = types.ModuleType("data.processor")
    data_processor.DataProcessor = FakeDataProcessor
    sys.modules["data.processor"] = data_processor

    core_pkg = types.ModuleType("core")
    core_pkg.__path__ = []
    sys.modules["core"] = core_pkg

    tts_service = types.ModuleType("core.tts_service")

    class TTSService:
        pass

    tts_service.TTSService = TTSService
    sys.modules["core.tts_service"] = tts_service

    agent_pkg = types.ModuleType("agent")
    agent_pkg.__path__ = []
    sys.modules["agent"] = agent_pkg


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module {name} from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def run_probe(donor_root: Path) -> dict:
    install_support_modules()

    vector_module = load_module(
        "core.vector_store",
        donor_root / "core" / "vector_store.py",
    )
    agent_module = load_module(
        "agent.psychology_agent",
        donor_root / "agent" / "psychology_agent.py",
    )
    rag_module = load_module(
        "psychat_patched_rag_system",
        donor_root / "core" / "rag_system.py",
    )

    model_gateway = FakeModelGateway()
    embedding_gateway = FakeEmbeddingGateway()

    agent = agent_module.PsychologyAgent(model_gateway=model_gateway)
    agent_result = agent._call_llm("route-test", max_tokens=10)
    if agent_result != "NO":
        raise AssertionError("patched PsychologyAgent did not use injected model gateway")

    vector = vector_module.VectorStore.__new__(vector_module.VectorStore)
    vector.embedding_gateway = embedding_gateway
    embedding = vector.get_embedding("embedding-test")
    if embedding != [0.1, 0.2, 0.3]:
        raise AssertionError("patched VectorStore did not use injected embedding gateway")

    shared_vector = FakeVectorResource()
    shared_data = FakeDataProcessor()
    fake_agent = FakeAgent()

    first = rag_module.RAGSystem(
        model_gateway,
        embedding_gateway,
        data_processor=shared_data,
        vector_store=shared_vector,
        psychology_agent=fake_agent,
        tts_service=None,
    )
    second = rag_module.RAGSystem(
        model_gateway,
        embedding_gateway,
        data_processor=shared_data,
        vector_store=shared_vector,
        psychology_agent=fake_agent,
        tts_service=None,
    )

    if first.vector_store is not shared_vector or second.vector_store is not shared_vector:
        raise AssertionError("long-lived vector resource was not reusable across runtimes")
    if first is second:
        raise AssertionError("per-session runtimes must be distinct objects")

    first_response = first.generate_response("hello-a")
    second_response = second.generate_response("hello-b")

    if first_response.get("response") != "gateway-response":
        raise AssertionError("patched RAGSystem did not use injected model gateway")
    if second_response.get("response") != "gateway-response":
        raise AssertionError("second patched runtime did not use injected model gateway")

    first_history = first.conversation_history
    second_history = second.conversation_history
    if not any(item.get("content") == "hello-a" for item in first_history):
        raise AssertionError("first runtime did not retain its own conversation state")
    if any(item.get("content") == "hello-a" for item in second_history):
        raise AssertionError("conversation state leaked between patched runtimes")

    response_calls = [
        call for call in model_gateway.calls
        if call["purpose"] == "psychat.rag.response"
    ]
    agent_calls = [
        call for call in model_gateway.calls
        if call["purpose"] == "psychat.rag.agent"
    ]

    return {
        "model_gateway_agent_call_pass": bool(agent_calls),
        "model_gateway_response_call_count": len(response_calls),
        "embedding_gateway_call_pass": embedding_gateway.calls == ["embedding-test"],
        "shared_vector_resource_reused": True,
        "distinct_session_runtimes": True,
        "session_state_isolated": True,
        "first_runtime_history_items": len(first_history),
        "second_runtime_history_items": len(second_history),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run_probe(args.donor_root)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
