from __future__ import annotations

import types
from typing import Any, Callable, Dict, List

from .contracts import ExecutionRequest, ExecutionResult
from .runtime import (
    EmbeddingGateway,
    EventTracer,
    ResilientModelGateway,
    SafetyGate,
    SessionStore,
)
from .validator import normalize_psychat_result


class PsyChatExecutor:
    executor_id = "psychat_adapted"
    capability = "rag.respond"

    def __init__(
        self,
        runtime_factory: Callable[[], Any],
        model_gateway: ResilientModelGateway,
        embedding_gateway: EmbeddingGateway,
        session_store: SessionStore,
        safety_gate: SafetyGate,
        tracer: EventTracer,
        *,
        embedding_timeout_s: float = 15.0,
    ) -> None:
        self.runtime_factory = runtime_factory
        self.model_gateway = model_gateway
        self.embedding_gateway = embedding_gateway
        self.session_store = session_store
        self.safety_gate = safety_gate
        self.tracer = tracer
        self.embedding_timeout_s = embedding_timeout_s

    def _bind_provider_boundaries(self, runtime: Any) -> None:
        if not hasattr(runtime, "psychology_agent"):
            raise TypeError("PsyChat runtime missing psychology_agent")
        if not hasattr(runtime, "vector_store"):
            raise TypeError("PsyChat runtime missing vector_store")

        def agent_call_llm(agent_self: Any, prompt: str, max_tokens: int = 1000) -> str:
            return self.model_gateway.generate(
                [{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.3,
                top_p=0.8,
            )

        def rag_generate(
            rag_self: Any,
            system_prompt: str,
            user_query: str,
            include_history: bool = True,
        ) -> str:
            messages: List[Dict[str, str]] = [
                {"role": "system", "content": system_prompt}
            ]
            if include_history:
                messages.extend(
                    list(getattr(rag_self, "conversation_history", []))[-12:]
                )
            messages.append({"role": "user", "content": user_query})
            return self.model_gateway.generate(
                messages,
                max_tokens=1000,
                temperature=0.6,
                top_p=0.9,
            )

        def get_embedding(vector_self: Any, text: str) -> List[float]:
            return self.embedding_gateway.embed(
                text,
                timeout_s=self.embedding_timeout_s,
            )

        runtime.psychology_agent._call_llm = types.MethodType(
            agent_call_llm,
            runtime.psychology_agent,
        )
        runtime._generate_response = types.MethodType(rag_generate, runtime)
        runtime.vector_store.get_embedding = types.MethodType(
            get_embedding,
            runtime.vector_store,
        )

        if hasattr(runtime, "tts_service"):
            runtime.tts_service = None

    def _restore_state(self, runtime: Any, state: Dict[str, Any]) -> None:
        runtime.conversation_history = list(state.get("conversation_history", []))
        runtime.no_rag_counter = int(state.get("no_rag_counter", 0))
        runtime.last_retrieval_docs = list(state.get("last_retrieval_docs", []))
        runtime._style_cache = dict(
            state.get("style_cache", {"topic": None, "analysis": ""})
        )

    def _snapshot_state(self, runtime: Any) -> Dict[str, Any]:
        return {
            "conversation_history": list(
                getattr(runtime, "conversation_history", [])
            ),
            "no_rag_counter": int(getattr(runtime, "no_rag_counter", 0)),
            "last_retrieval_docs": list(
                getattr(runtime, "last_retrieval_docs", [])
            ),
            "style_cache": dict(
                getattr(runtime, "_style_cache", {"topic": None, "analysis": ""})
            ),
        }

    def _clear_state(self, runtime: Any) -> None:
        runtime.conversation_history = []
        runtime.no_rag_counter = 0
        runtime.last_retrieval_docs = []
        runtime._style_cache = {"topic": None, "analysis": ""}

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        if request.route.capability != self.capability:
            raise ValueError(f"unsupported capability: {request.route.capability}")
        if request.route.executor_id != self.executor_id:
            raise ValueError(f"wrong executor: {request.route.executor_id}")

        runtime = self.runtime_factory()
        self._bind_provider_boundaries(runtime)
        self._restore_state(
            runtime,
            self.session_store.load(request.session_id),
        )
        self.tracer.emit(
            "executor.started",
            executor=self.executor_id,
            session_id=request.session_id,
        )

        try:
            raw = runtime.generate_response(request.user_message)
            normalized = normalize_psychat_result(raw)
            self.session_store.save(
                request.session_id,
                self._snapshot_state(runtime),
            )

            decision = self.safety_gate.validate(
                request.user_message,
                normalized["response"],
            )

            self.tracer.emit(
                "executor.completed",
                executor=self.executor_id,
                session_id=request.session_id,
                used_rag=normalized["used_rag"],
                safety_reason=decision.reason_code,
            )

            return ExecutionResult(
                status="ok" if decision.allowed else "blocked",
                response=decision.response,
                executor_id=self.executor_id,
                capability=self.capability,
                used_rag=normalized["used_rag"],
                sources=normalized["sources"],
                trace={
                    "topic": normalized["topic"],
                    "reason": normalized["reason"],
                    "safety": decision.reason_code,
                },
            )
        finally:
            self._clear_state(runtime)
