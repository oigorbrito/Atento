from __future__ import annotations

from typing import Any, Mapping, Protocol

from .contracts import ExecutionRequest, ExecutionResult


class ModelGateway(Protocol):
    def complete(self, *, purpose: str, messages: list[Mapping[str, str]], timeout_s: float) -> str: ...


class EmbeddingGateway(Protocol):
    def embed(self, *, text: str) -> list[float]: ...


class SessionStore(Protocol):
    def load(self, session_id: str) -> Mapping[str, Any]: ...
    def save(self, session_id: str, state: Mapping[str, Any]) -> None: ...


class Executor(Protocol):
    capability: str
    executor_id: str

    def execute(self, request: ExecutionRequest) -> ExecutionResult: ...


class SafetyPolicy(Protocol):
    def precheck(self, request: ExecutionRequest) -> None: ...
    def postcheck(self, result: ExecutionResult) -> None: ...


class TraceSink(Protocol):
    def emit(self, event: Mapping[str, Any]) -> None: ...
