from __future__ import annotations

from dataclasses import replace
from typing import Mapping

from .contracts import ExecutionRequest, ExecutionResult, RouteDecision
from .interfaces import SafetyPolicy, SessionStore, TraceSink
from .registry import CapabilityRegistry
from .safety import SpikeSafetyPolicy
from .validator import ResultValidator


class NullTraceSink:
    def emit(self, event: Mapping[str, Any]) -> None:
        return None


class PsyChatSpikeRuntime:
    def __init__(
        self,
        *,
        registry: CapabilityRegistry,
        sessions: SessionStore,
        safety: SafetyPolicy | None = None,
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
        result = self._validator.validate(
            executor.execute(request),
            expected_capability=route.capability,
            expected_executor=route.executor,
        )
        self._safety.postcheck(result)

        next_state = result.metadata.get("next_state", state)
        if not isinstance(next_state, Mapping):
            raise TypeError("next_state must be a mapping")
        self._sessions.save(session_id, next_state)

        for trace_event in result.trace:
            self._trace_sink.emit(trace_event)

        event = {
            "event": "executor.completed",
            "capability": route.capability,
            "executor": route.executor,
            "reason_code": route.reason_code,
        }
        self._trace_sink.emit(event)
        trace = result.trace + (event,)
        return replace(result, trace=trace)
