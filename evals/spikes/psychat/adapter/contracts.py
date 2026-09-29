from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


class ContractError(ValueError):
    pass


@dataclass(frozen=True)
class RouteDecision:
    capability: str
    executor_id: str
    args: Dict[str, Any] = field(default_factory=dict)
    reason_code: str = "unspecified"


@dataclass(frozen=True)
class ExecutionRequest:
    session_id: str
    user_message: str
    route: RouteDecision


@dataclass(frozen=True)
class ExecutionResult:
    status: str
    response: str
    executor_id: str
    capability: str
    used_rag: bool
    sources: List[Dict[str, Any]]
    trace: Dict[str, Any]
