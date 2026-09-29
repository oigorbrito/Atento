import unittest

from evals.spikes.psychat.adapter.contracts import RouteDecision
from evals.spikes.psychat.adapter.executor import PsyChatExecutorAdapter
from evals.spikes.psychat.adapter.registry import CapabilityRegistry
from evals.spikes.psychat.adapter.runtime import PsyChatSpikeRuntime
from evals.spikes.psychat.adapter.session import InMemorySessionStore
from evals.spikes.psychat.adapter.psychat_bridge import PsyChatRagSystemPort


class FakePsyChatDonor:
    def respond(self, *, message, session_state):
        count = int(session_state.get("turns", 0)) + 1
        return f"{message}:{count}", {"turns": count}


class FakeUpstreamRagSystem:
    def __init__(self):
        self.conversation_history = []
        self.no_rag_counter = 0
        self.last_retrieval_docs = []

    def generate_response(self, message):
        self.no_rag_counter += 1
        self.conversation_history.append({"role": "user", "content": message})
        self.conversation_history.append({"role": "assistant", "content": "ok"})
        return {
            "success": True,
            "response": f"upstream:{message}:{self.no_rag_counter}",
            "sources": [],
        }


class AlternateRagExecutor:
    capability = "knowledge.rag"
    executor_id = "alternate"

    def execute(self, request):
        from evals.spikes.psychat.adapter.contracts import ExecutionResult
        return ExecutionResult(
            response="alternate",
            executor=self.executor_id,
            capability=self.capability,
            metadata={"next_state": dict(request.state)},
        )


def route(executor="psychat"):
    return RouteDecision(
        capability="knowledge.rag",
        executor=executor,
        reason_code="knowledge_needed",
        confidence=0.9,
    )


class RecordingTraceSink:
    def __init__(self):
        self.events = []

    def emit(self, event):
        self.events.append(dict(event))


class PsyChatAdapterTest(unittest.TestCase):
    def make_runtime(self):
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(FakePsyChatDonor()))
        return PsyChatSpikeRuntime(
            registry=registry,
            sessions=InMemorySessionStore(),
        ), registry

    def test_sessions_are_isolated_outside_donor(self):
        runtime, _ = self.make_runtime()
        self.assertEqual(runtime.execute(session_id="a", message="x", route=route()).response, "x:1")
        self.assertEqual(runtime.execute(session_id="a", message="x", route=route()).response, "x:2")
        self.assertEqual(runtime.execute(session_id="b", message="x", route=route()).response, "x:1")

    def test_real_bridge_shape_restores_and_extracts_donor_state(self):
        port = PsyChatRagSystemPort(FakeUpstreamRagSystem)
        response, state = port.respond(
            message="hello",
            session_state={"conversation_history": [], "no_rag_counter": 4},
        )
        self.assertEqual(response, "upstream:hello:5")
        self.assertEqual(state["no_rag_counter"], 5)
        self.assertEqual(len(state["conversation_history"]), 2)

    def test_bridge_factory_prevents_state_reuse_between_calls(self):
        port = PsyChatRagSystemPort(FakeUpstreamRagSystem)
        _, first = port.respond(message="a", session_state={})
        _, second = port.respond(message="b", session_state={})
        self.assertEqual(first["no_rag_counter"], 1)
        self.assertEqual(second["no_rag_counter"], 1)

    def test_executor_can_be_swapped_by_registration(self):
        runtime, registry = self.make_runtime()
        registry.register(AlternateRagExecutor())
        result = runtime.execute(session_id="a", message="x", route=route("alternate"))
        self.assertEqual(result.response, "alternate")
        self.assertEqual(result.executor, "alternate")

    def test_unknown_executor_fails_closed(self):
        runtime, _ = self.make_runtime()
        with self.assertRaises(LookupError):
            runtime.execute(session_id="a", message="x", route=route("missing"))

    def test_invalid_route_is_rejected_before_donor(self):
        runtime, _ = self.make_runtime()
        bad = RouteDecision(
            capability="knowledge.rag",
            executor="psychat",
            reason_code="knowledge_needed",
            confidence=2.0,
        )
        with self.assertRaises(ValueError):
            runtime.execute(session_id="a", message="x", route=bad)

    def test_trace_records_executor_choice(self):
        sink = RecordingTraceSink()
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(FakePsyChatDonor()))
        runtime = PsyChatSpikeRuntime(
            registry=registry,
            sessions=InMemorySessionStore(),
            trace_sink=sink,
        )
        result = runtime.execute(session_id="a", message="x", route=route())
        self.assertEqual(result.trace[-1]["event"], "executor.completed")
        self.assertEqual(result.trace[-1]["executor"], "psychat")
        self.assertEqual(sink.events[-1]["executor"], "psychat")


if __name__ == "__main__":
    unittest.main()
