from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class RouteDecision:
    capability: str
    executor: str
    reason_code: str
    confidence: float

    def validate(self) -> None:
        if not self.capability:
            raise ValueError("capability is required")
        if not self.executor:
            raise ValueError("executor is required")
        if not self.reason_code:
            raise ValueError("reason_code is required")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass(frozen=True)
class ExecutionRequest:
    session_id: str
    message: str
    route: RouteDecision
    state: Mapping[str, Any] = field(default_factory=dict)

    def validate(self) -> None:
        if not self.session_id:
            raise ValueError("session_id is required")
        if not self.message.strip():
            raise ValueError("message is required")
        self.route.validate()


@dataclass(frozen=True)
class ExecutionResult:
    response: str
    executor: str
    capability: str
    trace: tuple[Mapping[str, Any], ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)
