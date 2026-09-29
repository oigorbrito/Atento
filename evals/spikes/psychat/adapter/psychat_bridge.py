from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any


class PsyChatRagSystemPort:
    """Bridge to PsyChat with external session state.

    The factory creates a fresh session runtime per call. After the minimal
    fork patch, that runtime may receive shared long-lived resources from its
    composition root, so isolation does not require rebuilding them every turn.
    """

    def __init__(self, rag_system_factory: Callable[[], Any]) -> None:
        self._factory = rag_system_factory

    @staticmethod
    def _normalize_response(raw_result: Any) -> str:
        if isinstance(raw_result, str):
            return raw_result
        if isinstance(raw_result, Mapping):
            if raw_result.get("success") is False:
                detail = raw_result.get("reason") or raw_result.get("response") or "PsyChat donor failed"
                raise RuntimeError(str(detail))
            response = raw_result.get("response")
            if not isinstance(response, str) or not response.strip():
                raise ValueError("donor response mapping must contain non-empty response")
            return response
        raise TypeError("donor generate_response must return str or mapping")

    def respond(self, *, message: str, session_state: dict) -> tuple[str, dict]:
        donor = self._factory()
        donor.conversation_history = list(session_state.get("conversation_history", []))
        donor.no_rag_counter = int(session_state.get("no_rag_counter", 0))
        if hasattr(donor, "last_retrieval_docs"):
            donor.last_retrieval_docs = list(session_state.get("last_retrieval_docs", []))

        response = self._normalize_response(donor.generate_response(message))
        next_state = {
            "conversation_history": list(getattr(donor, "conversation_history", [])),
            "no_rag_counter": int(getattr(donor, "no_rag_counter", 0)),
        }
        if hasattr(donor, "last_retrieval_docs"):
            next_state["last_retrieval_docs"] = list(donor.last_retrieval_docs)
        return response, next_state


def build_patched_factory(
    *,
    model_gateway: Any,
    embedding_gateway: Any,
    data_processor: Any,
    vector_store: Any,
    psychology_agent_factory: Callable[[], Any],
    tts_service: Any = None,
) -> Callable[[], Any]:
    """Build isolated session runtimes over shared long-lived RAG resources."""
    from core.rag_system import RAGSystem

    def factory() -> Any:
        return RAGSystem(
            model_gateway=model_gateway,
            embedding_gateway=embedding_gateway,
            data_processor=data_processor,
            vector_store=vector_store,
            psychology_agent=psychology_agent_factory(),
            tts_service=tts_service,
        )

    return factory


def upstream_factory():
    """Legacy helper for the unpatched donor probe only."""
    from core.rag_system import RAGSystem
    return RAGSystem()
