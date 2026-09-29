from __future__ import annotations

from collections.abc import Callable, Mapping
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

        history = list(session_state.get("conversation_history", []))
        no_rag_counter = int(session_state.get("no_rag_counter", 0))

        donor.conversation_history = history
        donor.no_rag_counter = no_rag_counter
        if hasattr(donor, "last_retrieval_docs"):
            donor.last_retrieval_docs = list(session_state.get("last_retrieval_docs", []))

        raw_result = donor.generate_response(message)
        response = self._normalize_response(raw_result)

        next_state = {
            "conversation_history": list(getattr(donor, "conversation_history", [])),
            "no_rag_counter": int(getattr(donor, "no_rag_counter", 0)),
        }
        if hasattr(donor, "last_retrieval_docs"):
            next_state["last_retrieval_docs"] = list(donor.last_retrieval_docs)

        return response, next_state


def upstream_factory():
    """Lazy import keeps the spike testable without donor dependencies."""
    from core.rag_system import RAGSystem

    return RAGSystem()
