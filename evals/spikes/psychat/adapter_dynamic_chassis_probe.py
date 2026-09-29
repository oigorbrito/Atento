#!/usr/bin/env python3
"""Dynamic chassis evidence for the PsyChat adapter boundary.

No external donor/provider is required. This probe measures enforcement seams
that static CFS cannot prove by source inspection alone.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from evals.spikes.psychat.adapter.contracts import (
    ExecutionRequest,
    ExecutionResult,
    RouteDecision,
)
from evals.spikes.psychat.adapter.executor import PsyChatExecutorAdapter
from evals.spikes.psychat.adapter.registry import CapabilityRegistry
from evals.spikes.psychat.adapter.resilience import retry_with_timeout_boundary
from evals.spikes.psychat.adapter.runtime import PsyChatSpikeRuntime
from evals.spikes.psychat.adapter.session import InMemorySessionStore
from evals.spikes.psychat.adapter.validator import ResultValidator


def route(executor: str = "psychat") -> RouteDecision:
    return RouteDecision(
        capability="knowledge.rag",
        executor=executor,
        reason_code="knowledge_needed",
        confidence=0.9,
    )


class StatefulDonor:
    def __init__(self):
        self.calls = 0
        self.force_flags = []

    def respond(self, *, message, session_state, force_retrieval=False):
        self.calls += 1
        self.force_flags.append(bool(force_retrieval))
        if not force_retrieval:
            raise AssertionError("knowledge.rag executor must force donor retrieval")
        count = int(session_state.get("turns", 0)) + 1
        return "ok", {
            "turns": count,
            "last_retrieval_docs": [{"id": "doc-1"}],
            "_atento_turn": {
                "rag_attempted": True,
                "used_rag": True,
                "sources": [],
            },
        }


class RecordingTraceSink:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(dict(event))


class AlternateExecutor:
    capability = "knowledge.rag"
    executor_id = "alternate"

    def execute(self, request):
        return ExecutionResult(
            response="alternate",
            executor=self.executor_id,
            capability=self.capability,
            metadata={"next_state": dict(request.state)},
        )


class BlockingPreSafety:
    def precheck(self, request):
        raise PermissionError("pre-block")

    def postcheck(self, result):
        raise AssertionError("postcheck must not execute")


class BlockingPostSafety:
    def precheck(self, request):
        request.validate()

    def postcheck(self, result):
        raise PermissionError("post-block")


def assert_raises(exc_type, operation) -> bool:
    try:
        operation()
    except exc_type:
        return True
    return False


def schema_validation_probe() -> dict:
    checks = {}

    checks["invalid_route_confidence"] = assert_raises(
        ValueError,
        lambda: RouteDecision(
            capability="knowledge.rag",
            executor="psychat",
            reason_code="x",
            confidence=2.0,
        ).validate(),
    )

    checks["empty_message"] = assert_raises(
        ValueError,
        lambda: ExecutionRequest(
            session_id="s",
            message=" ",
            route=route(),
        ).validate(),
    )

    validator = ResultValidator()
    checks["wrong_result_type"] = assert_raises(
        TypeError,
        lambda: validator.validate("not-an-execution-result"),
    )
    checks["route_identity_mismatch"] = assert_raises(
        ValueError,
        lambda: validator.validate(
            ExecutionResult(
                response="ok",
                executor="other",
                capability="knowledge.rag",
            ),
            expected_capability="knowledge.rag",
            expected_executor="psychat",
        ),
    )

    checks["empty_output"] = assert_raises(
        ValueError,
        lambda: validator.validate(
            ExecutionResult(
                response=" ",
                executor="psychat",
                capability="knowledge.rag",
            )
        ),
    )

    passed = sum(bool(value) for value in checks.values())
    return {
        "checks": checks,
        "passed": passed,
        "total": len(checks),
        "schema_validation_coverage": passed / len(checks),
    }


def trace_probe() -> dict:
    donor = StatefulDonor()
    registry = CapabilityRegistry()
    registry.register(PsyChatExecutorAdapter(donor))
    sink = RecordingTraceSink()
    runtime = PsyChatSpikeRuntime(
        registry=registry,
        sessions=InMemorySessionStore(),
        trace_sink=sink,
    )
    result = runtime.execute(
        session_id="trace",
        message="knowledge",
        route=route(),
    )
    result_events = [str(event.get("event")) for event in result.trace]
    sink_events = [str(event.get("event")) for event in sink.events]
    required = ["rag.completed", "executor.completed"]
    covered = [event for event in required if event in sink_events]
    if donor.force_flags != [True]:
        raise AssertionError(
            f"RAG executor did not enforce retrieval: {donor.force_flags}"
        )
    return {
        "required_events": required,
        "result_events": result_events,
        "sink_events": sink_events,
        "covered": covered,
        "trace_coverage": len(covered) / len(required),
        "rag_force_retrieval_contract_pass": True,
    }


def rollback_probe() -> dict:
    donor = StatefulDonor()
    registry = CapabilityRegistry()
    registry.register(PsyChatExecutorAdapter(donor))
    registry.register(AlternateExecutor())
    runtime = PsyChatSpikeRuntime(
        registry=registry,
        sessions=InMemorySessionStore(),
    )

    switched = runtime.execute(
        session_id="rollback",
        message="x",
        route=route("alternate"),
    )
    restored = runtime.execute(
        session_id="rollback",
        message="x",
        route=route("psychat"),
    )
    passed = switched.executor == "alternate" and restored.executor == "psychat"
    if not passed:
        raise AssertionError("executor rollback failed")
    return {
        "rollback_test_pass": True,
        "switched_to": switched.executor,
        "restored_to": restored.executor,
    }


def safety_probe() -> dict:
    pre_donor = StatefulDonor()
    pre_registry = CapabilityRegistry()
    pre_registry.register(PsyChatExecutorAdapter(pre_donor))
    pre_sessions = InMemorySessionStore()
    pre_runtime = PsyChatSpikeRuntime(
        registry=pre_registry,
        sessions=pre_sessions,
        safety=BlockingPreSafety(),
    )
    pre_blocked = assert_raises(
        PermissionError,
        lambda: pre_runtime.execute(
            session_id="pre",
            message="x",
            route=route(),
        ),
    )
    if not pre_blocked or pre_donor.calls != 0 or dict(pre_sessions.load("pre")):
        raise AssertionError("pre-safety enforcement failed")

    post_donor = StatefulDonor()
    post_registry = CapabilityRegistry()
    post_registry.register(PsyChatExecutorAdapter(post_donor))
    post_sessions = InMemorySessionStore()
    post_runtime = PsyChatSpikeRuntime(
        registry=post_registry,
        sessions=post_sessions,
        safety=BlockingPostSafety(),
    )
    post_blocked = assert_raises(
        PermissionError,
        lambda: post_runtime.execute(
            session_id="post",
            message="x",
            route=route(),
        ),
    )
    if not post_blocked or post_donor.calls != 1 or dict(post_sessions.load("post")):
        raise AssertionError("post-safety enforcement failed")

    return {
        "pre_safety_blocks_before_donor": True,
        "post_safety_blocks_before_state_persistence": True,
        "independent_safety_enforcement_pass": True,
    }


def resilience_probe() -> dict:
    transient_calls = {"count": 0}

    def transient():
        transient_calls["count"] += 1
        if transient_calls["count"] == 1:
            raise TimeoutError("transient")
        return "ok"

    result = retry_with_timeout_boundary(transient, attempts=2)
    if result != "ok" or transient_calls["count"] != 2:
        raise AssertionError("retry boundary did not recover transient timeout")

    fatal_calls = {"count": 0}

    def fatal():
        fatal_calls["count"] += 1
        raise ValueError("fatal")

    non_retryable_failed_closed = assert_raises(
        ValueError,
        lambda: retry_with_timeout_boundary(fatal, attempts=2),
    )
    if not non_retryable_failed_closed or fatal_calls["count"] != 1:
        raise AssertionError("non-retryable error was retried or swallowed")

    return {
        "timeout_retry_recovered": True,
        "transient_attempts": transient_calls["count"],
        "non_retryable_failed_closed": True,
        "non_retryable_attempts": fatal_calls["count"],
        "resilience_boundary_dynamic_pass": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    schema = schema_validation_probe()
    trace = trace_probe()
    rollback = rollback_probe()
    safety = safety_probe()
    resilience = resilience_probe()

    if schema["schema_validation_coverage"] != 1.0:
        raise AssertionError("schema validation coverage is incomplete")
    if trace["trace_coverage"] != 1.0:
        raise AssertionError("trace coverage is incomplete")

    report = {
        "metric_version": "atento-adapter-dynamic-v0.2",
        "schema_validation": schema,
        "trace": trace,
        "rollback": rollback,
        "safety": safety,
        "resilience": resilience,
    }
    encoded = json.dumps(report, ensure_ascii=False, indent=2)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
