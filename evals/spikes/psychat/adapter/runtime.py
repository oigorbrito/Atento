from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol


class SessionStore(Protocol):
    def load(self, session_id: str) -> Dict[str, Any]: ...
    def save(self, session_id: str, state: Dict[str, Any]) -> None: ...


class InMemorySessionStore:
    def __init__(self) -> None:
        self._data: Dict[str, Dict[str, Any]] = {}

    def load(self, session_id: str) -> Dict[str, Any]:
        raw = self._data.get(session_id, {})
        return {
            "conversation_history": list(raw.get("conversation_history", [])),
            "no_rag_counter": int(raw.get("no_rag_counter", 0)),
            "last_retrieval_docs": list(raw.get("last_retrieval_docs", [])),
            "style_cache": dict(raw.get("style_cache", {"topic": None, "analysis": ""})),
        }

    def save(self, session_id: str, state: Dict[str, Any]) -> None:
        self._data[session_id] = {
            "conversation_history": list(state.get("conversation_history", [])),
            "no_rag_counter": int(state.get("no_rag_counter", 0)),
            "last_retrieval_docs": list(state.get("last_retrieval_docs", [])),
            "style_cache": dict(state.get("style_cache", {"topic": None, "analysis": ""})),
        }


class ModelGateway(Protocol):
    def generate(
        self,
        messages: List[Dict[str, str]],
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
        timeout_s: float,
    ) -> str:
        ...


class EmbeddingGateway(Protocol):
    def embed(self, text: str, *, timeout_s: float) -> List[float]: ...


class SafetyGate(Protocol):
    def validate(self, user_message: str, candidate_response: str) -> "SafetyDecision": ...


@dataclass(frozen=True)
class SafetyDecision:
    allowed: bool
    response: str
    reason_code: str


class EventTracer:
    def __init__(self) -> None:
        self.events: List[Dict[str, Any]] = []

    def emit(self, event: str, **payload: Any) -> None:
        self.events.append({"event": event, **payload})


class ResilientModelGateway:
    def __init__(
        self,
        delegate: ModelGateway,
        *,
        attempts: int = 2,
        timeout_s: float = 15.0,
    ) -> None:
        if attempts < 1:
            raise ValueError("attempts must be >= 1")
        self.delegate = delegate
        self.attempts = attempts
        self.timeout_s = timeout_s

    def generate(
        self,
        messages: List[Dict[str, str]],
        *,
        max_tokens: int,
        temperature: float,
        top_p: float,
    ) -> str:
        last_exc: Exception | None = None
        for _ in range(self.attempts):
            try:
                return self.delegate.generate(
                    messages,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    timeout_s=self.timeout_s,
                )
            except Exception as exc:
                last_exc = exc
        assert last_exc is not None
        raise last_exc
