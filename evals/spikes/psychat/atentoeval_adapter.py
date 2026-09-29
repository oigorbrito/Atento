from __future__ import annotations

from typing import Any

from evals.atentoeval.schema import TurnResult

from .adapter.contracts import ExecutionResult


def execution_trace_to_atentoeval(result: ExecutionResult) -> dict[str, Any]:
    rag: dict[str, Any] = {}
    executive = {
        "capability": result.capability,
        "executor": result.executor,
    }

    for event in result.trace:
        if event.get("event") == "rag.completed":
            rag = {
                "attempted": bool(event.get("attempted", False)),
                "used": bool(event.get("used", False)),
                "retrieved_count": int(event.get("retrieved_count", 0)),
                "retrieved_ids": [str(x) for x in event.get("retrieved_ids", [])],
            }
        elif event.get("event") == "executor.completed":
            executive.update(
                {
                    "reason_code": event.get("reason_code"),
                    "capability": event.get("capability", result.capability),
                    "executor": event.get("executor", result.executor),
                }
            )

    return {
        "executive": executive,
        "rag": rag,
    }


def to_turn_result(
    *,
    case_id: str,
    step_index: int,
    result: ExecutionResult,
    latency_ms: float | None = None,
    usage: dict[str, Any] | None = None,
) -> TurnResult:
    return TurnResult(
        case_id=case_id,
        step_index=step_index,
        response=result.response,
        trace=execution_trace_to_atentoeval(result),
        latency_ms=latency_ms,
        usage=dict(usage or {}),
    )
