from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping, Protocol

from .contracts import ExecutionRequest, ExecutionResult, RouteDecision
from .registry import CapabilityRegistry
from .safety import SpikeSafetyPolicy
from .session import InMemorySessionStore
from .validator import ResultValidator


class TraceSink(Protocol):
    def emit(self, event: Mapping[str, Any]) -> None: ...


class NullTraceSink:
    def emit(self, event: Mapping[str, Any]) -> None:
        return None


class PsyChatSpikeRuntime:
    def __init__(
        self,
        *,
        registry: CapabilityRegistry,
        sessions: InMemorySessionStore,
        safety: SpikeSafetyPolicy | None = None,
        validator: ResultValidator | None = None,
        trace_sink: TraceSink | None = None,
    ) -> None:
        self._registry = registry
        self._sessions = sessions
        self._safety = safety or SpikeSafetyPolicy()
        self._validator = validator or ResultValidator()
        self._trace_sink = trace_sink or NullTraceSink()

    def execute(self, *, session_id: str, message: str, route: RouteDecision) -> ExecutionResult:
        state = self._sessions.load(session_id)
        request = ExecutionRequest(
            session_id=session_id,
            message=message,
            route=route,
            state=state,
        )
        self._safety.precheck(request)
        executor = self._registry.resolve(route.capability, route.executor)
        result = self._validator.validate(executor.execute(request))
        self._safety.postcheck(result)

        next_state = result.metadata.get("next_state", state)
        if not isinstance(next_state, Mapping):
            raise TypeError("next_state must be a mapping")
        self._sessions.save(session_id, next_state)

        event = {
            "event": "executor.completed",
            "capability": route.capability,
            "executor": route.executor,
            "reason_code": route.reason_code,
        }
        self._trace_sink.emit(event)
        trace = result.trace + (event,)
        return replace(result, trace=trace)
