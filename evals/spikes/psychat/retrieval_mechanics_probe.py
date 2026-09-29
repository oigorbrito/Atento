#!/usr/bin/env python3
"""Dynamic retrieval-mechanics probe against pinned PsyChat RAGSystem source.

This probe executes the donor's real RAG orchestration and retrieval-merging
methods while stubbing only external resources. It measures mechanics, not
semantic/conversational quality.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from copy import deepcopy
from pathlib import Path


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


def doc(doc_id: str, content: str, similarity: float, topic: str = "情绪") -> dict:
    return {
        "id": doc_id,
        "content": content,
        "similarity": similarity,
        "metadata": {
            "source": f"{doc_id}.txt",
            "topic": topic,
            "qa_id": doc_id,
        },
    }


class StubDataProcessor:
    pass


class StubTTSService:
    pass


class ScriptedVectorStore:
    def __init__(self, responses=None):
        self.responses = dict(responses or {})
        self.calls = []

    def search(self, query, *, topics=None, threshold=None, **kwargs):
        self.calls.append(
            {
                "query": query,
                "topics": list(topics or []),
                "threshold": threshold,
            }
        )
        return deepcopy(self.responses.get(query, []))


class MultiQueryAgent:
    def __init__(self):
        self.calls = []

    def analyze_user_input(
        self,
        user_message,
        conversation_history,
        vector_store,
        force_retrieval=False,
    ):
        self.calls.append(
            {
                "message": user_message,
                "force_retrieval": force_retrieval,
                "history": deepcopy(conversation_history),
            }
        )
        return {
            "need_rag": True,
            "topics": ["情绪"],
            "topic": "情绪",
            "search_queries": ["q1", "q2"],
            "search_query": "q1",
            "original_message": user_message,
            "forced": force_retrieval,
        }


class ForcedRagAgent:
    def __init__(self):
        self.calls = []

    def analyze_user_input(
        self,
        user_message,
        conversation_history,
        vector_store,
        force_retrieval=False,
    ):
        self.calls.append(bool(force_retrieval))
        if not force_retrieval:
            return {
                "need_rag": False,
                "topics": [],
                "topic": None,
                "search_queries": [],
                "search_query": None,
                "original_message": user_message,
                "forced": False,
            }
        return {
            "need_rag": True,
            "topics": ["情绪"],
            "topic": "情绪",
            "search_queries": ["forced-q"],
            "search_query": "forced-q",
            "original_message": user_message,
            "forced": True,
        }


def install_stubs() -> None:
    requests = types.ModuleType("requests")
    requests.post = lambda *a, **k: (_ for _ in ()).throw(
        AssertionError("network call is forbidden in retrieval mechanics probe")
    )
    sys.modules["requests"] = requests

    data_pkg = types.ModuleType("data")
    data_pkg.__path__ = []
    sys.modules["data"] = data_pkg
    processor = types.ModuleType("data.processor")
    processor.DataProcessor = StubDataProcessor
    sys.modules["data.processor"] = processor

    core_pkg = types.ModuleType("core")
    core_pkg.__path__ = []
    sys.modules["core"] = core_pkg
    vector = types.ModuleType("core.vector_store")
    vector.VectorStore = ScriptedVectorStore
    sys.modules["core.vector_store"] = vector
    tts = types.ModuleType("core.tts_service")
    tts.TTSService = StubTTSService
    sys.modules["core.tts_service"] = tts

    agent_pkg = types.ModuleType("agent")
    agent_pkg.__path__ = []
    sys.modules["agent"] = agent_pkg
    psychology = types.ModuleType("agent.psychology_agent")
    psychology.PsychologyAgent = MultiQueryAgent
    sys.modules["agent.psychology_agent"] = psychology

    config = types.ModuleType("config")
    config.DEEPSEEK_API_KEY = "stub"
    config.DEEPSEEK_BASE_URL = "https://invalid.example"
    config.DEEPSEEK_MODEL = "stub"
    config.MAX_NO_RAG_ROUNDS = 3
    config.TOP_K_RESULTS = 6
    config.SIMILARITY_THRESHOLD = 0.15
    config.KNOWLEDGE_DIR = "/tmp/atento-unused"
    config.TTS_ENABLED = False
    sys.modules["config"] = config


def load_rag_system(donor_root: Path):
    install_stubs()
    source = donor_root / "core" / "rag_system.py"
    if not source.exists():
        raise FileNotFoundError(source)
    spec = importlib.util.spec_from_file_location("_psychat_retrieval_probe", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned RAGSystem")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RAGSystem


def prepare_runtime(rag_system_cls, *, vector_store, agent):
    runtime = rag_system_cls()
    runtime.vector_store = vector_store
    runtime.psychology_agent = agent
    runtime.tts_service = None
    runtime._expand_context = lambda docs, top_n=2: []
    runtime._analyze_counselor_style = lambda expanded, topic: ""
    runtime._generate_response = (
        lambda system_prompt, user_query, include_history=True: "stub-response"
    )
    return runtime


def run_multi_query(rag_system_cls) -> dict:
    same_content = "duplicate-evidence-" + ("x" * 120)
    first_a = doc("A-low", same_content, 0.60)
    better_a = doc("A-high", same_content, 0.90)
    b = doc("B", "second-evidence-" + ("b" * 120), 0.70)
    c = doc("C", "third-evidence-" + ("c" * 120), 0.80)

    vector = ScriptedVectorStore(
        {
            "q1": [first_a, b],
            "q2": [better_a, c],
        }
    )
    agent = MultiQueryAgent()
    runtime = prepare_runtime(rag_system_cls, vector_store=vector, agent=agent)

    result = runtime.generate_response("multi-query")
    if not result.get("success") or not result.get("used_rag"):
        raise AssertionError(f"multi-query RAG execution failed: {result}")

    ids = [item["metadata"]["qa_id"] for item in runtime.last_retrieval_docs]
    if ids != ["A-high", "C", "B"]:
        raise AssertionError(f"unexpected dedup/ranking order: {ids}")
    if [x["qa_id"] for x in result["sources"]] != ["A-high", "C", "B"]:
        raise AssertionError(f"result sources diverged from retrieval state: {result['sources']}")
    if [x["query"] for x in vector.calls] != ["q1", "q2"]:
        raise AssertionError(f"unexpected vector search calls: {vector.calls}")
    if any(x["threshold"] != 0.15 for x in vector.calls):
        raise AssertionError(f"configured similarity threshold not propagated: {vector.calls}")
    if runtime.no_rag_counter != 0:
        raise AssertionError("successful RAG turn must reset no_rag_counter")
    if not any(x.get("content") == "multi-query" for x in runtime.conversation_history):
        raise AssertionError("conversation history was not updated")

    return {
        "retrieved_ids": ids,
        "vector_queries": [x["query"] for x in vector.calls],
        "dedup_kept_higher_similarity_duplicate": True,
        "sorted_descending_similarity": True,
        "no_rag_counter_reset": True,
    }


def run_forced_rag(rag_system_cls) -> dict:
    cached = doc("cached", "cached-evidence-" + ("z" * 120), 0.95)
    fresh = doc("fresh", "fresh-evidence-" + ("y" * 120), 0.80)
    vector = ScriptedVectorStore({"forced-q": [fresh]})
    agent = ForcedRagAgent()
    runtime = prepare_runtime(rag_system_cls, vector_store=vector, agent=agent)
    runtime.no_rag_counter = 2
    runtime.last_retrieval_docs = [cached]

    result = runtime.generate_response("force-me")
    if not result.get("success") or not result.get("used_rag"):
        raise AssertionError(f"forced RAG execution failed: {result}")
    if agent.calls != [False, True]:
        raise AssertionError(f"force_retrieval control path not exercised: {agent.calls}")

    ids = [item["metadata"]["qa_id"] for item in runtime.last_retrieval_docs]
    if ids != ["cached", "fresh"]:
        raise AssertionError(f"cached/new merge order unexpected: {ids}")
    if runtime.no_rag_counter != 0:
        raise AssertionError("forced RAG turn must reset no_rag_counter")

    return {
        "force_retrieval_call_sequence": agent.calls,
        "merged_retrieved_ids": ids,
        "cached_evidence_retained": True,
        "new_evidence_retained": True,
        "no_rag_counter_reset": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    rag_system_cls = load_rag_system(args.donor_root)
    report = {
        "probe": "psychat_retrieval_mechanics",
        "pinned_commit": PINNED_COMMIT,
        "quality_claim": False,
        "multi_query": run_multi_query(rag_system_cls),
        "forced_rag": run_forced_rag(rag_system_cls),
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
