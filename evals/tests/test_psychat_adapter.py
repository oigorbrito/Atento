import unittest

from evals.spikes.psychat.adapter.contracts import RouteDecision
from evals.spikes.psychat.adapter.executor import PsyChatExecutorAdapter
from evals.spikes.psychat.adapter.registry import CapabilityRegistry
from evals.spikes.psychat.adapter.runtime import PsyChatSpikeRuntime
from evals.spikes.psychat.adapter.session import InMemorySessionStore
from evals.spikes.psychat.adapter.psychat_bridge import PsyChatRagSystemPort, build_patched_factory


class CountingDonor:
    def __init__(self):
        self.calls = 0

    def respond(self, *, message, session_state):
        self.calls += 1
        return "counted", {"turns": int(session_state.get("turns", 0)) + 1}


class BlockingPreSafety:
    def precheck(self, request):
        raise PermissionError("blocked before donor")

    def postcheck(self, result):
        raise AssertionError("postcheck must not run")


class BlockingPostSafety:
    def precheck(self, request):
        request.validate()

    def postcheck(self, result):
        raise PermissionError("blocked after donor")


class FakePsyChatDonor:
    def respond(self, *, message, session_state):
        count = int(session_state.get("turns", 0)) + 1
        return f"{message}:{count}", {"turns": count}


class FakeRetrievalDonor:
    def respond(self, *, message, session_state):
        return "grounded", {
            **dict(session_state),
            "last_retrieval_docs": [
                {"metadata": {"qa_id": "qa-001", "source": "a.md"}},
                {"id": "doc-002", "metadata": {"source": "b.md"}},
            ],
        }


class FakeAttemptedEmptyRagDonor:
    def respond(self, *, message, session_state):
        return "no evidence", {
            **dict(session_state),
            "last_retrieval_docs": [],
            "_atento_turn": {
                "rag_attempted": True,
                "used_rag": False,
                "sources": [],
            },
        }


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


class FakeForcedRouteRagSystem(FakeUpstreamRagSystem):
    def __init__(self):
        super().__init__()
        self.force_flags = []

    def generate_response(self, message, force_retrieval=False):
        self.force_flags.append(bool(force_retrieval))
        return super().generate_response(message)


class FakeRetrievalStateRagSystem(FakeUpstreamRagSystem):
    def generate_response(self, message):
        result = super().generate_response(message)
        self.last_retrieval_docs.append({"content": message})
        return result


class FakeFailedUpstreamRagSystem(FakeUpstreamRagSystem):
    def generate_response(self, message):
        return {"success": False, "response": "failed", "reason": "donor error"}


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


class LookupExecutor:
    capability = "knowledge.lookup"
    executor_id = "lookup"

    def execute(self, request):
        from evals.spikes.psychat.adapter.contracts import ExecutionResult
        return ExecutionResult(
            response="lookup",
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

    def test_pre_safety_blocks_before_donor_execution(self):
        donor = CountingDonor()
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(donor))
        sessions = InMemorySessionStore()
        runtime = PsyChatSpikeRuntime(
            registry=registry,
            sessions=sessions,
            safety=BlockingPreSafety(),
        )

        with self.assertRaisesRegex(PermissionError, "blocked before donor"):
            runtime.execute(
                session_id="a",
                message="x",
                route=route(),
            )

        self.assertEqual(donor.calls, 0)
        self.assertEqual(dict(sessions.load("a")), {})

    def test_post_safety_blocks_before_state_persistence(self):
        donor = CountingDonor()
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(donor))
        sessions = InMemorySessionStore()
        runtime = PsyChatSpikeRuntime(
            registry=registry,
            sessions=sessions,
            safety=BlockingPostSafety(),
        )

        with self.assertRaisesRegex(PermissionError, "blocked after donor"):
            runtime.execute(
                session_id="a",
                message="x",
                route=route(),
            )

        self.assertEqual(donor.calls, 1)
        self.assertEqual(dict(sessions.load("a")), {})

    def test_sessions_are_isolated_outside_donor(self):
        runtime, _ = self.make_runtime()
        self.assertEqual(runtime.execute(session_id="a", message="x", route=route()).response, "x:1")
        self.assertEqual(runtime.execute(session_id="a", message="x", route=route()).response, "x:2")
        self.assertEqual(runtime.execute(session_id="b", message="x", route=route()).response, "x:1")

    def test_executor_emits_deterministic_rag_trace(self):
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(FakeRetrievalDonor()))
        runtime = PsyChatSpikeRuntime(
            registry=registry,
            sessions=InMemorySessionStore(),
        )

        result = runtime.execute(
            session_id="a",
            message="knowledge question",
            route=route(),
        )

        self.assertEqual(result.trace[0]["event"], "rag.completed")
        self.assertTrue(result.trace[0]["used"])
        self.assertEqual(
            result.trace[0]["retrieved_ids"],
            ["qa-001", "doc-002"],
        )
        self.assertEqual(result.trace[-1]["event"], "executor.completed")

    def test_rag_attempt_without_evidence_is_traced_but_not_persisted(self):
        sessions = InMemorySessionStore()
        registry = CapabilityRegistry()
        registry.register(PsyChatExecutorAdapter(FakeAttemptedEmptyRagDonor()))
        runtime = PsyChatSpikeRuntime(
            registry=registry,
            sessions=sessions,
        )

        result = runtime.execute(
            session_id="a",
            message="question with no evidence",
            route=route(),
        )

        self.assertTrue(result.trace[0]["attempted"])
        self.assertFalse(result.trace[0]["used"])
        self.assertEqual(result.trace[0]["retrieved_ids"], [])
        self.assertNotIn("_atento_turn", sessions.load("a"))

    def test_real_bridge_shape_restores_and_extracts_donor_state(self):
        port = PsyChatRagSystemPort(FakeUpstreamRagSystem)
        response, state = port.respond(
            message="hello",
            session_state={"conversation_history": [], "no_rag_counter": 4},
        )
        self.assertEqual(response, "upstream:hello:5")
        self.assertEqual(state["no_rag_counter"], 5)
        self.assertEqual(len(state["conversation_history"]), 2)

    def test_bridge_can_enforce_atento_rag_route_on_patched_donor(self):
        created = []

        def factory():
            donor = FakeForcedRouteRagSystem()
            created.append(donor)
            return donor

        port = PsyChatRagSystemPort(
            factory,
            force_retrieval=True,
        )
        response, _ = port.respond(
            message="must retrieve",
            session_state={},
        )

        self.assertEqual(response, "upstream:must retrieve:1")
        self.assertEqual(len(created), 1)
        self.assertEqual(created[0].force_flags, [True])

    def test_bridge_restores_retrieval_state(self):
        port = PsyChatRagSystemPort(FakeRetrievalStateRagSystem)
        response, state = port.respond(
            message="hello",
            session_state={
                "conversation_history": [],
                "no_rag_counter": 4,
                "last_retrieval_docs": [{"content": "prior"}],
            },
        )
        self.assertEqual(response, "upstream:hello:5")
        self.assertEqual(
            state["last_retrieval_docs"],
            [{"content": "prior"}, {"content": "hello"}],
        )

    def test_bridge_fails_closed_on_donor_failure_mapping(self):
        port = PsyChatRagSystemPort(FakeFailedUpstreamRagSystem)
        with self.assertRaisesRegex(RuntimeError, "donor error"):
            port.respond(message="hello", session_state={})

    def test_bridge_factory_prevents_state_reuse_between_calls(self):
        port = PsyChatRagSystemPort(FakeUpstreamRagSystem)
        _, first = port.respond(message="a", session_state={})
        _, second = port.respond(message="b", session_state={})
        self.assertEqual(first["no_rag_counter"], 1)
        self.assertEqual(second["no_rag_counter"], 1)

    def test_patched_factory_reuses_long_lived_resources_but_not_session_runtime(self):
        import sys
        import types

        created = []
        rag_module = types.ModuleType("core.rag_system")

        class FakePatchedRagSystem(FakeUpstreamRagSystem):
            def __init__(self, **kwargs):
                super().__init__()
                self.resources = kwargs
                created.append(self)

        core = types.ModuleType("core")
        core.__path__ = []
        rag_module.RAGSystem = FakePatchedRagSystem
        previous_core = sys.modules.get("core")
        previous_rag = sys.modules.get("core.rag_system")
        sys.modules["core"] = core
        sys.modules["core.rag_system"] = rag_module
        try:
            shared_model = object()
            shared_embedding = object()
            shared_data = object()
            shared_vector = object()
            agents = []

            def agent_factory():
                agent = object()
                agents.append(agent)
                return agent

            factory = build_patched_factory(
                model_gateway=shared_model,
                embedding_gateway=shared_embedding,
                data_processor=shared_data,
                vector_store=shared_vector,
                psychology_agent_factory=agent_factory,
            )
            port = PsyChatRagSystemPort(factory)
            port.respond(message="a", session_state={})
            port.respond(message="b", session_state={})
        finally:
            if previous_core is None:
                sys.modules.pop("core", None)
            else:
                sys.modules["core"] = previous_core
            if previous_rag is None:
                sys.modules.pop("core.rag_system", None)
            else:
                sys.modules["core.rag_system"] = previous_rag

        self.assertEqual(len(created), 2)
        self.assertIsNot(created[0], created[1])
        self.assertIs(created[0].resources["model_gateway"], shared_model)
        self.assertIs(created[1].resources["model_gateway"], shared_model)
        self.assertIs(created[0].resources["vector_store"], shared_vector)
        self.assertIs(created[1].resources["vector_store"], shared_vector)
        self.assertIsNot(agents[0], agents[1])

    def test_executor_can_be_swapped_by_registration(self):
        runtime, registry = self.make_runtime()
        registry.register(AlternateRagExecutor())
        result = runtime.execute(session_id="a", message="x", route=route("alternate"))
        self.assertEqual(result.response, "alternate")
        self.assertEqual(result.executor, "alternate")

    def test_executor_route_can_roll_back_without_registry_mutation(self):
        runtime, registry = self.make_runtime()
        registry.register(AlternateRagExecutor())

        switched = runtime.execute(
            session_id="a", message="x", route=route("alternate")
        )
        rolled_back = runtime.execute(
            session_id="a", message="x", route=route("psychat")
        )

        self.assertEqual(switched.executor, "alternate")
        self.assertEqual(rolled_back.executor, "psychat")
        self.assertEqual(rolled_back.response, "x:1")

    def test_new_capability_registers_without_chassis_change(self):
        runtime, registry = self.make_runtime()
        registry.register(LookupExecutor())
        result = runtime.execute(
            session_id="a",
            message="x",
            route=RouteDecision(
                capability="knowledge.lookup",
                executor="lookup",
                reason_code="lookup_needed",
                confidence=0.9,
            ),
        )
        self.assertEqual(result.response, "lookup")
        self.assertEqual(result.capability, "knowledge.lookup")

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
