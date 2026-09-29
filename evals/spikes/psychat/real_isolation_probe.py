#!/usr/bin/env python3
"""Dynamic session-isolation probe against the pinned PsyChat RAGSystem source.

The probe loads the donor's real core/rag_system.py while replacing external
dependencies (provider, vector store, TTS and data processor) with deterministic
stubs. RAGSystem.generate_response itself is kept from the donor source.

This isolates the state-ownership question from network/API dependencies.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import types
from pathlib import Path

from evals.spikes.psychat.adapter.psychat_bridge import PsyChatRagSystemPort


PINNED_COMMIT = "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4"


class StubDataProcessor:
    pass


class StubVectorStore:
    pass


class StubPsychologyAgent:
    def __init__(self) -> None:
        self.histories: list[list[dict]] = []

    def analyze_user_input(
        self,
        user_message,
        conversation_history,
        vector_store,
        force_retrieval=False,
    ):
        self.histories.append([dict(item) for item in conversation_history])
        return {
            "need_rag": False,
            "topics": [],
            "topic": None,
            "search_queries": [],
            "search_query": None,
            "original_message": user_message,
            "forced": force_retrieval,
        }


class StubTTSService:
    pass


def install_stub_modules() -> None:
    requests = types.ModuleType("requests")
    sys.modules["requests"] = requests

    data_pkg = types.ModuleType("data")
    data_pkg.__path__ = []
    sys.modules["data"] = data_pkg
    data_processor = types.ModuleType("data.processor")
    data_processor.DataProcessor = StubDataProcessor
    sys.modules["data.processor"] = data_processor

    core_pkg = types.ModuleType("core")
    core_pkg.__path__ = []
    sys.modules["core"] = core_pkg
    vector_store = types.ModuleType("core.vector_store")
    vector_store.VectorStore = StubVectorStore
    sys.modules["core.vector_store"] = vector_store
    tts_service = types.ModuleType("core.tts_service")
    tts_service.TTSService = StubTTSService
    sys.modules["core.tts_service"] = tts_service

    agent_pkg = types.ModuleType("agent")
    agent_pkg.__path__ = []
    sys.modules["agent"] = agent_pkg
    psychology_agent = types.ModuleType("agent.psychology_agent")
    psychology_agent.PsychologyAgent = StubPsychologyAgent
    sys.modules["agent.psychology_agent"] = psychology_agent

    config = types.ModuleType("config")
    config.DEEPSEEK_API_KEY = "stub"
    config.DEEPSEEK_BASE_URL = "https://invalid.example"
    config.MAX_NO_RAG_ROUNDS = 999
    config.TTS_ENABLED = False
    sys.modules["config"] = config


def load_real_rag_system(donor_root: Path):
    install_stub_modules()
    source = donor_root / "core" / "rag_system.py"
    if not source.exists():
        raise FileNotFoundError(source)

    spec = importlib.util.spec_from_file_location("psychat_pinned_rag_system", source)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load pinned RAGSystem module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.RAGSystem


def make_runtime(rag_system_cls):
    runtime = rag_system_cls()
    runtime._generate_response = lambda *args, **kwargs: "stub-response"
    return runtime


def contains_content(history, value: str) -> bool:
    return any(item.get("content") == value for item in history)


def run_probe(donor_root: Path) -> dict:
    rag_system_cls = load_real_rag_system(donor_root)

    # Upstream web/interface.py owns one process-global RAGSystem. Reproduce
    # that ownership model by sending two conceptual sessions through one
    # donor instance.
    shared = make_runtime(rag_system_cls)
    first = shared.generate_response("session-A-secret")
    second = shared.generate_response("session-B-message")
    if not first.get("success") or not second.get("success"):
        raise AssertionError("stubbed upstream execution did not succeed")

    history_seen_by_second_request = shared.psychology_agent.histories[-1]
    upstream_shared_instance_cross_session_state = contains_content(
        history_seen_by_second_request, "session-A-secret"
    )
    if not upstream_shared_instance_cross_session_state:
        raise AssertionError(
            "expected the shared upstream instance to carry session A history into session B"
        )

    # The Atento bridge creates a donor runtime per invocation and restores
    # only the caller's external state.
    port = PsyChatRagSystemPort(lambda: make_runtime(rag_system_cls))
    response_a, state_a = port.respond(message="session-A-secret", session_state={})
    response_b, state_b = port.respond(message="session-B-message", session_state={})
    response_a_followup, state_a_followup = port.respond(
        message="session-A-followup",
        session_state=state_a,
    )

    if (
        response_a != "stub-response"
        or response_b != "stub-response"
        or response_a_followup != "stub-response"
    ):
        raise AssertionError("bridge did not normalize the real donor response mapping")

    state_a_history = state_a.get("conversation_history", [])
    state_b_history = state_b.get("conversation_history", [])
    state_a_followup_history = state_a_followup.get("conversation_history", [])

    adapted_bridge_isolated = (
        contains_content(state_a_history, "session-A-secret")
        and contains_content(state_b_history, "session-B-message")
        and not contains_content(state_b_history, "session-A-secret")
        and contains_content(state_a_followup_history, "session-A-secret")
        and contains_content(state_a_followup_history, "session-A-followup")
        and not contains_content(state_a_followup_history, "session-B-message")
    )
    if not adapted_bridge_isolated:
        raise AssertionError("adapted bridge failed session isolation or continuity")

    return {
        "pinned_commit": PINNED_COMMIT,
        "upstream_shared_instance_cross_session_state": True,
        "adapted_bridge_isolated": True,
        "adapted_bridge_session_continuity": True,
        "upstream_second_request_history_items": len(history_seen_by_second_request),
        "adapter_session_a_history_items": len(state_a_history),
        "adapter_session_b_history_items": len(state_b_history),
        "adapter_session_a_followup_history_items": len(state_a_followup_history),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--donor-root", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = run_probe(args.donor_root)
    encoded = json.dumps(result, indent=2, ensure_ascii=False)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
