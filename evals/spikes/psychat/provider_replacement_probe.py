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

from evals.spikes.psychat.adapter.psychat_bridge import build_patched_factory


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


class RecordingRouteAgent:
    def __init__(self):
        self.force_flags = []

    def analyze_user_input(
        self,
        user_message,
        conversation_history,
        vector_store,
        force_retrieval=False,
    ):
        self.force_flags.append(bool(force_retrieval))
        return {
            "need_rag": bool(force_retrieval),
            "topics": ["情绪"] if force_retrieval else [],
            "topic": "情绪" if force_retrieval else None,
            "search_queries": ["forced-query"] if force_retrieval else [],
            "search_query": "forced-query" if force_retrieval else None,
            "original_message": user_message,
            "forced": bool(force_retrieval),
        }


class RecordingRetrievalStore:
    def __init__(self):
        self.calls = []

    def search(self, query, *, topics=None, threshold=None, **kwargs):
        self.calls.append(
            {
                "query": query,
                "topics": list(topics or []),
                "threshold": threshold,
            }
        )
        return [
            {
                "content": "forced retrieval evidence",
                "similarity": 0.9,
                "metadata": {
                    "source": "forced.txt",
                    "topic": "情绪",
                    "qa_id": "forced-doc",
                },
            }
        ]


class StubBuildProcessor:
    def process_documents(self, *args, **kwargs):
        return [{
            "content": "build-doc",
            "source": "build.txt",
            "size": 9,
            "type": "psychology_qa",
        }]


class RecordingBuildStore:
    def __init__(self, *, clear_ok=True):
        self.clear_ok = bool(clear_ok)
        self.clear_calls = 0
        self.add_calls = 0

    def clear_collection(self):
        self.clear_calls += 1
        return self.clear_ok

    def add_documents(self, documents):
        self.add_calls += 1
        return True

    def get_collection_info(self):
        return {
            "name": "build-index",
            "document_count": 1,
            "index_schema": "rag-cosine-v1",
            "embedding_identity": "build:model:v1",
            "corpus_identity": "psychat@pinned",
        }


class RecordingEmbeddingGateway:
    def __init__(self, vector, identity):
        self.vector = list(vector)
        self.index_identity = str(identity)
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

    embedding_a = RecordingEmbeddingGateway([1.0, 2.0], "provider-a:model-a:v1")
    embedding_b = RecordingEmbeddingGateway([9.0, 8.0], "provider-b:model-b:v1")
    vector_a = vector_module.VectorStore(embedding_gateway=embedding_a)
    vector_b = vector_module.VectorStore(embedding_gateway=embedding_b)

    if vector_a.get_embedding("alpha") != [1.0, 2.0]:
        raise AssertionError("embedding gateway A was not used")
    if vector_b.get_embedding("beta") != [9.0, 8.0]:
        raise AssertionError("embedding gateway B was not used")
    if vector_a.collection_name == vector_b.collection_name:
        raise AssertionError(
            "different embedding identities must not reuse the same persisted collection"
        )
    if vector_a.embedding_identity != embedding_a.index_identity:
        raise AssertionError("vector A lost embedding identity")
    if vector_b.embedding_identity != embedding_b.index_identity:
        raise AssertionError("vector B lost embedding identity")

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

    embedding_mismatch_factory = build_patched_factory(
        model_gateway=model_a,
        embedding_gateway=embedding_b,
        data_processor=StubDataProcessor(),
        vector_store=vector_a,
        psychology_agent_factory=lambda: agent_a,
        tts_service=None,
    )
    try:
        embedding_mismatch_factory()
    except ValueError as exc:
        if "embedding gateway" not in str(exc):
            raise
    else:
        raise AssertionError(
            "composition root accepted a vector store bound to another embedding gateway"
        )

    model_mismatch_factory = build_patched_factory(
        model_gateway=model_b,
        embedding_gateway=embedding_a,
        data_processor=StubDataProcessor(),
        vector_store=vector_a,
        psychology_agent_factory=lambda: agent_a,
        tts_service=None,
    )
    try:
        model_mismatch_factory()
    except ValueError as exc:
        if "model gateway" not in str(exc):
            raise
    else:
        raise AssertionError(
            "composition root accepted a psychology agent bound to another model gateway"
        )

    build_store = RecordingBuildStore(clear_ok=True)
    build_runtime = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubBuildProcessor(),
        vector_store=build_store,
        psychology_agent=agent_a,
        tts_service=None,
    )
    if not build_runtime.build_knowledge_base():
        raise AssertionError("default replacement rebuild failed")
    if build_store.clear_calls != 1 or build_store.add_calls != 1:
        raise AssertionError(
            "default rebuild must clear exactly once before adding documents"
        )

    failing_build_store = RecordingBuildStore(clear_ok=False)
    failing_build_runtime = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubBuildProcessor(),
        vector_store=failing_build_store,
        psychology_agent=agent_a,
        tts_service=None,
    )
    if failing_build_runtime.build_knowledge_base():
        raise AssertionError("rebuild must fail when collection clear fails")
    if failing_build_store.clear_calls != 1 or failing_build_store.add_calls != 0:
        raise AssertionError(
            "failed clear must prevent document writes during rebuild"
        )

    # Routing-authority probe: once Atento has selected knowledge.rag, the
    # patched donor must accept force_retrieval from the outer Router instead
    # of re-deciding that no retrieval is needed.
    route_agent = RecordingRouteAgent()
    route_store = RecordingRetrievalStore()
    routed = rag_module.RAGSystem(
        model_gateway=model_a,
        embedding_gateway=embedding_a,
        data_processor=StubDataProcessor(),
        vector_store=route_store,
        psychology_agent=route_agent,
        tts_service=None,
    )
    routed_result = routed.generate_response(
        "router-selected-rag",
        force_retrieval=True,
    )
    if route_agent.force_flags != [True]:
        raise AssertionError(
            f"outer force_retrieval did not reach donor agent: {route_agent.force_flags}"
        )
    if not route_store.calls:
        raise AssertionError("outer RAG route did not trigger donor retrieval")
    if not routed_result.get("used_rag"):
        raise AssertionError(
            f"forced donor route did not report RAG usage: {routed_result}"
        )

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
        "metric_version": "psychat-provider-replacement-v0.6",
        "model_provider_swap_pass": True,
        "embedding_provider_swap_pass": True,
        "embedding_index_identity_isolated": True,
        "composition_provider_consistency_pass": True,
        "knowledge_base_rebuild_replace_default_pass": True,
        "knowledge_base_rebuild_clear_fail_closed_pass": True,
        "embedding_a_collection_name": vector_a.collection_name,
        "embedding_b_collection_name": vector_b.collection_name,
        "rag_model_gateway_swap_pass": True,
        "external_rag_route_enforcement_pass": True,
        "external_rag_route_vector_calls": len(route_store.calls),
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
