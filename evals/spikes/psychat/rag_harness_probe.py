#!/usr/bin/env python3
"""Deterministic end-to-end plumbing probe for PsyChat -> AtentoEval RAG traces.

This is not a donor-quality benchmark. It verifies that fixture-driven RAG
routing and retrieved document IDs survive the complete integration seam:

RouteDecision -> Registry -> Executor -> PsyChatRagSystemPort -> donor response
-> state/trace extraction -> AtentoEval scoring.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.atentoeval.metrics import score_turn
from evals.atentoeval.runner import load_cases
from evals.spikes.psychat.adapter.contracts import ExecutionResult, RouteDecision
from evals.spikes.psychat.adapter.executor import PsyChatExecutorAdapter
from evals.spikes.psychat.adapter.psychat_bridge import PsyChatRagSystemPort
from evals.spikes.psychat.adapter.registry import CapabilityRegistry
from evals.spikes.psychat.adapter.runtime import PsyChatSpikeRuntime
from evals.spikes.psychat.adapter.session import InMemorySessionStore
from evals.spikes.psychat.atentoeval_adapter import to_turn_result


class FixturePatchedRagSystem:
    def __init__(self, *, retrieved_ids: list[str]) -> None:
        self.retrieved_ids = list(retrieved_ids)
        self.conversation_history = []
        self.no_rag_counter = 0
        self.last_retrieval_docs = []
        self.force_flags = []

    def generate_response(self, message: str, force_retrieval: bool = False):
        self.force_flags.append(bool(force_retrieval))
        if not force_retrieval:
            raise AssertionError("knowledge.rag reached donor without force_retrieval")

        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append(
            {"role": "assistant", "content": "fixture-response"}
        )
        self.last_retrieval_docs = [
            {
                "id": doc_id,
                "metadata": {"qa_id": doc_id, "source": f"{doc_id}.fixture"},
            }
            for doc_id in self.retrieved_ids
        ]
        return {
            "success": True,
            "response": "fixture-response",
            "sources": [
                {"qa_id": doc_id, "source": f"{doc_id}.fixture"}
                for doc_id in self.retrieved_ids
            ],
            "used_rag": bool(self.last_retrieval_docs),
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

    created = []

    def donor_factory():
        donor = FixturePatchedRagSystem(retrieved_ids=retrieved_ids)
        created.append(donor)
        return donor

    registry = CapabilityRegistry()
    registry.register(
        PsyChatExecutorAdapter(
            PsyChatRagSystemPort(donor_factory)
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

    if attempted:
        if len(created) != 1:
            raise AssertionError(f"{case.id}: expected one PsyChat runtime")
        if created[0].force_flags != [True]:
            raise AssertionError(
                f"{case.id}: RAG authority was not propagated through bridge: "
                f"{created[0].force_flags}"
            )
    elif created:
        raise AssertionError(f"{case.id}: non-RAG case instantiated PsyChat donor")

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
                f"{case.id}: expected {metric}=1.0 in plumbing probe, "
                f"got {scores.get(metric)}"
            )

    return {
        "case_id": case.id,
        "selected_capability": selected_route.capability,
        "selected_executor": selected_route.executor,
        "bridge_exercised": attempted,
        "force_retrieval_propagated": attempted,
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
    attempted_rows = [row for row in rows if row["bridge_exercised"]]
    empty_attempts = [
        row
        for row in attempted_rows
        if row["trace"]["attempted"] and not row["trace"]["retrieved_ids"]
    ]
    if not empty_attempts:
        raise AssertionError(
            "RAG suite must contain at least one attempted retrieval with zero evidence"
        )

    report = {
        "probe": "rag_harness_end_to_end_plumbing",
        "quality_claim": False,
        "case_count": len(rows),
        "bridge_case_count": len(attempted_rows),
        "forced_empty_retrieval_case_count": len(empty_attempts),
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
