#!/usr/bin/env python3
"""Deterministic plumbing probe for PsyChat -> AtentoEval RAG traces.

This is not a donor-quality benchmark. It verifies that fixture-driven RAG
decisions and retrieved document IDs survive the PsyChat adapter and are scored
correctly by AtentoEval.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.metrics import score_turn
from evals.atentoeval.runner import load_cases
from evals.spikes.psychat.adapter.contracts import ExecutionResult, RouteDecision
from evals.spikes.psychat.adapter.executor import PsyChatExecutorAdapter
from evals.spikes.psychat.adapter.registry import CapabilityRegistry
from evals.spikes.psychat.adapter.runtime import PsyChatSpikeRuntime
from evals.spikes.psychat.adapter.session import InMemorySessionStore
from evals.spikes.psychat.atentoeval_adapter import to_turn_result


class FixtureDonor:
    def __init__(self, *, attempted: bool, retrieved_ids: list[str]) -> None:
        self.attempted = attempted
        self.retrieved_ids = list(retrieved_ids)

    def respond(self, *, message: str, session_state: dict, force_retrieval: bool = False):
        if not self.attempted:
            raise AssertionError("non-RAG case was incorrectly routed to PsyChat")
        if not force_retrieval:
            raise AssertionError("RAG route reached PsyChat without force_retrieval")
        docs = [{"id": doc_id} for doc_id in self.retrieved_ids]
        return "fixture-response", {
            **dict(session_state),
            "last_retrieval_docs": docs,
            "_atento_turn": {
                "rag_attempted": self.attempted,
                "used_rag": bool(docs),
                "sources": [],
            },
        }


class DirectConversationExecutor:
    capability = "conversation.direct"
    executor_id = "direct"

    def execute(self, request):
        return ExecutionResult(
            response="fixture-direct-response",
            executor=self.executor_id,
            capability=self.capability,
            metadata={"next_state": dict(request.state)},
        )


def run_case(case) -> dict:
    step = case.steps[0]
    fixture = step.fixtures
    attempted = bool(fixture["rag_attempted"])
    retrieved_ids = [str(x) for x in fixture.get("retrieval_fixture", [])]

    registry = CapabilityRegistry()
    registry.register(
        PsyChatExecutorAdapter(
            FixtureDonor(
                attempted=attempted,
                retrieved_ids=retrieved_ids,
            )
        )
    )
    registry.register(DirectConversationExecutor())
    runtime = PsyChatSpikeRuntime(
        registry=registry,
        sessions=InMemorySessionStore(),
    )
    selected_route = (
        RouteDecision(
            capability="knowledge.rag",
            executor="psychat",
            reason_code="rag_required",
            confidence=1.0,
        )
        if attempted
        else RouteDecision(
            capability="conversation.direct",
            executor="direct",
            reason_code="rag_not_required",
            confidence=1.0,
        )
    )
    result = runtime.execute(
        session_id=case.id,
        message=step.user,
        route=selected_route,
    )
    turn = to_turn_result(
        case_id=case.id,
        step_index=0,
        result=result,
    )
    scores = score_turn(step.expected, turn)

    for metric in (
        "rag_route_hit",
        "rag_retrieval_precision",
        "rag_retrieval_recall",
        "rag_retrieval_f1",
    ):
        if scores.get(metric) != 1.0:
            raise AssertionError(
                f"{case.id}: expected {metric}=1.0 in plumbing probe, got {scores.get(metric)}"
            )

    return {
        "case_id": case.id,
        "selected_capability": selected_route.capability,
        "selected_executor": selected_route.executor,
        "trace": turn.trace["rag"],
        "scores": {
            key: value for key, value in scores.items() if key.startswith("rag_")
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    cases = load_cases(args.cases)
    rag_cases = [case for case in cases.values() if case.suite == "rag"]
    if not rag_cases:
        raise AssertionError("no RAG cases found")

    rows = [run_case(case) for case in rag_cases]
    report = {
        "probe": "rag_harness_plumbing",
        "quality_claim": False,
        "case_count": len(rows),
        "all_deterministic_rag_metrics_pass": True,
        "rows": rows,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
