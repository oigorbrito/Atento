from __future__ import annotations

from .interfaces import Executor


class CapabilityRegistry:
    def __init__(self) -> None:
        self._executors: dict[tuple[str, str], Executor] = {}

    def register(self, executor: Executor) -> None:
        key = (executor.capability, executor.executor_id)
        if key in self._executors:
            raise ValueError(f"executor already registered: {key}")
        self._executors[key] = executor

    def resolve(self, capability: str, executor_id: str) -> Executor:
        try:
            return self._executors[(capability, executor_id)]
        except KeyError as exc:
            raise LookupError(f"no executor for {capability}:{executor_id}") from exc
