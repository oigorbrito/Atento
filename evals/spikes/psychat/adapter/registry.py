from __future__ import annotations

from typing import Dict, Protocol

from .contracts import ExecutionRequest, ExecutionResult


class Executor(Protocol):
    executor_id: str

    def execute(self, request: ExecutionRequest) -> ExecutionResult:
        ...


class CapabilityRegistry:
    def __init__(self) -> None:
        self._executors: Dict[str, Dict[str, Executor]] = {}

    def register(self, capability: str, executor: Executor) -> None:
        bucket = self._executors.setdefault(capability, {})
        if executor.executor_id in bucket:
            raise ValueError(f"duplicate executor: {capability}/{executor.executor_id}")
        bucket[executor.executor_id] = executor

    def resolve(self, capability: str, executor_id: str) -> Executor:
        try:
            return self._executors[capability][executor_id]
        except KeyError as exc:
            raise KeyError(f"unregistered executor: {capability}/{executor_id}") from exc
