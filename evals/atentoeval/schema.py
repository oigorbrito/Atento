from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Expected:
    accepted_strategies: List[str] = field(default_factory=list)
    memory_ids: List[str] = field(default_factory=list)
    tool_calls: List[str] = field(default_factory=list)
    safety_route: Optional[str] = None
    required_behaviors: List[str] = field(default_factory=list)
    forbidden_behaviors: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expected":
        return cls(
            accepted_strategies=list(data.get("accepted_strategies", [])),
            memory_ids=list(data.get("memory_ids", [])),
            tool_calls=list(data.get("tool_calls", [])),
            safety_route=data.get("safety_route"),
            required_behaviors=list(data.get("required_behaviors", [])),
            forbidden_behaviors=list(data.get("forbidden_behaviors", [])),
        )


@dataclass
class EvalStep:
    user: str
    expected: Expected = field(default_factory=Expected)
    fixtures: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvalStep":
        return cls(
            user=data["user"],
            expected=Expected.from_dict(data.get("expected", {})),
            fixtures=dict(data.get("fixtures", {})),
        )


@dataclass
class EvalCase:
    id: str
    suite: str
    source_id: str
    agent_scope: str = "UNSPECIFIED"
    language: str = "pt-BR"
    profile: Dict[str, Any] = field(default_factory=dict)
    context: List[Dict[str, Any]] = field(default_factory=list)
    memory_seed: List[Dict[str, Any]] = field(default_factory=list)
    steps: List[EvalStep] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EvalCase":
        return cls(
            id=data["id"],
            suite=data["suite"],
            source_id=data.get("source_id", "SRC-ATENTO"),
            agent_scope=str(data.get("agent_scope", "UNSPECIFIED")),
            language=data.get("language", "pt-BR"),
            profile=dict(data.get("profile", {})),
            context=list(data.get("context", [])),
            memory_seed=list(data.get("memory_seed", [])),
            steps=[EvalStep.from_dict(x) for x in data.get("steps", [])],
            tags=list(data.get("tags", [])),
            metadata=dict(data.get("metadata", {})),
        )


@dataclass
class TurnResult:
    case_id: str
    step_index: int
    response: str
    trace: Dict[str, Any] = field(default_factory=dict)
    latency_ms: Optional[float] = None
    usage: Dict[str, Any] = field(default_factory=dict)
    judge: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TurnResult":
        return cls(
            case_id=data["case_id"],
            step_index=int(data["step_index"]),
            response=data.get("response", ""),
            trace=dict(data.get("trace", {})),
            latency_ms=data.get("latency_ms"),
            usage=dict(data.get("usage", {})),
            judge=dict(data.get("judge", {})),
        )
