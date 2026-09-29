from __future__ import annotations

from collections.abc import Callable, Mapping
import inspect
from typing import Any


class PsyChatRagSystemPort:
    """Bridge to the upstream RAGSystem without changing upstream source.

    A fresh donor runtime is created per call. This deliberately trades
    performance for isolation in the spike. If the donor is adopted, resource
    ownership must be redesigned without reintroducing cross-session state.
    """

    def __init__(self, rag_system_factory: Callable[[], Any]) -> None:
        self._factory = rag_system_factory

    @staticmethod
    def _normalize_result(
        raw_result: Any,
        *,
        force_retrieval: bool = False,
    ) -> tuple[str, dict]:
        if isinstance(raw_result, str):
            return raw_result, {}

        if isinstance(raw_result, Mapping):
            if raw_result.get("success") is False:
                detail = (
                    raw_result.get("reason")
                    or raw_result.get("response")
                    or "PsyChat donor failed"
                )
                raise RuntimeError(str(detail))

            response = raw_result.get("response")
            if not isinstance(response, str) or not response.strip():
                raise ValueError("donor response mapping must contain non-empty response")

            used_rag = bool(raw_result.get("used_rag", False))
            # Upstream sets topic/search_query only on the RAG branch. This lets
            # us distinguish an attempted retrieval with zero results from a
            # simple conversational turn that never entered RAG.
            rag_attempted = (
                force_retrieval
                or used_rag
                or "topic" in raw_result
                or "search_query" in raw_result
            )
            turn_metadata = {
                "rag_attempted": rag_attempted,
                "used_rag": used_rag,
                "sources": list(raw_result.get("sources", [])),
            }
            return response, turn_metadata

        raise TypeError("donor generate_response must return str or mapping")

    def respond(
        self,
        *,
        message: str,
        session_state: dict,
        force_retrieval: bool = False,
    ) -> tuple[str, dict]:
        donor = self._factory()

        history = list(session_state.get("conversation_history", []))
        no_rag_counter = int(session_state.get("no_rag_counter", 0))

        donor.conversation_history = history
        donor.no_rag_counter = no_rag_counter
        if hasattr(donor, "last_retrieval_docs"):
            donor.last_retrieval_docs = list(
                session_state.get("last_retrieval_docs", [])
            )
        if hasattr(donor, "_style_cache"):
            style_cache = session_state.get("_style_cache", {})
            donor._style_cache = (
                dict(style_cache)
                if isinstance(style_cache, Mapping)
                else {"topic": None, "analysis": ""}
            )

        if force_retrieval:
            params = inspect.signature(donor.generate_response).parameters
            if "force_retrieval" not in params:
                raise RuntimeError(
                    "PsyChat donor does not expose external force_retrieval; "
                    "the minimal BLOCO I fork patch is required"
                )
            raw_result = donor.generate_response(
                message,
                force_retrieval=True,
            )
        else:
            raw_result = donor.generate_response(message)
        response, turn_metadata = self._normalize_result(
            raw_result,
            force_retrieval=force_retrieval,
        )

        next_state = {
            "conversation_history": list(
                getattr(donor, "conversation_history", [])
            ),
            "no_rag_counter": int(getattr(donor, "no_rag_counter", 0)),
            "_atento_turn": turn_metadata,
        }
        if hasattr(donor, "last_retrieval_docs"):
            next_state["last_retrieval_docs"] = list(donor.last_retrieval_docs)
        if hasattr(donor, "_style_cache"):
            next_state["_style_cache"] = dict(donor._style_cache)

        return response, next_state


def upstream_factory():
    """Lazy import keeps the spike testable without donor dependencies."""
    from core.rag_system import RAGSystem

    return RAGSystem()


def build_patched_factory(
    *,
    model_gateway: Any,
    embedding_gateway: Any,
    data_processor: Any,
    vector_store: Any,
    psychology_agent_factory: Callable[[], Any],
    tts_service: Any = None,
) -> Callable[[], Any]:
    """Compose patched PsyChat with shared resources and per-session runtime.

    Shared/long-lived:
    - model gateway;
    - embedding gateway;
    - data processor;
    - vector store/index;
    - optional TTS service.

    Per invocation/session runtime:
    - RAGSystem instance;
    - PsychologyAgent instance;
    - mutable conversation/retrieval state restored by PsyChatRagSystemPort.
    """

    def factory():
        from core.rag_system import RAGSystem

        vector_gateway = getattr(vector_store, "embedding_gateway", None)
        if vector_gateway is not None and vector_gateway is not embedding_gateway:
            raise ValueError(
                "vector_store embedding gateway does not match composition gateway"
            )

        psychology_agent = psychology_agent_factory()
        agent_gateway = getattr(psychology_agent, "model_gateway", None)
        if agent_gateway is not None and agent_gateway is not model_gateway:
            raise ValueError(
                "psychology_agent model gateway does not match composition gateway"
            )

        return RAGSystem(
            model_gateway=model_gateway,
            embedding_gateway=embedding_gateway,
            data_processor=data_processor,
            vector_store=vector_store,
            psychology_agent=psychology_agent,
            tts_service=tts_service,
        )

    return factory
