from __future__ import annotations

import unittest

from evals.spikes.psychat.adapter import (
    CapabilityRegistry,
    ContractError,
    EventTracer,
    ExecutionRequest,
    InMemorySessionStore,
    PsyChatExecutor,
    ResilientModelGateway,
    RouteDecision,
    SafetyDecision,
)


class FakeDelegateGateway:
    def __init__(self, fail_first: bool = False):
        self.calls = []
        self.fail_first = fail_first

    def generate(self, messages, *, max_tokens, temperature, top_p, timeout_s):
        self.calls.append({"messages": messages, "timeout_s": timeout_s})
        if self.fail_first and len(self.calls) == 1:
            raise TimeoutError("simulated timeout")
        return "gateway-output"


class FakeEmbeddingGateway:
    def __init__(self):
        self.calls = []

    def embed(self, text, *, timeout_s):
        self.calls.append((text, timeout_s))
        return [0.1, 0.2]


class FakeSafetyGate:
    def validate(self, user_message, candidate_response):
        if "UNSAFE" in candidate_response:
            return SafetyDecision(False, "blocked", "test_block")
        return SafetyDecision(True, candidate_response, "allow")


class FakePsychologyAgent:
    def _call_llm(self, prompt, max_tokens=1000):
        raise AssertionError("direct donor LLM path should be overridden")


class FakeVectorStore:
    def get_embedding(self, text):
        raise AssertionError("direct donor embedding path should be overridden")


class FakePsyChatRuntime:
    def __init__(self, registry):
        self.psychology_agent = FakePsychologyAgent()
        self.vector_store = FakeVectorStore()
        self.tts_service = object()
        self.conversation_history = []
        self.no_rag_counter = 0
        self.last_retrieval_docs = []
        self._style_cache = {"topic": None, "analysis": ""}
        registry.append(self)

    def _generate_response(self, system_prompt, user_query, include_history=True):
        raise AssertionError("direct donor generation path should be overridden")

    def generate_response(self, query):
        route = self.psychology_agent._call_llm("route", max_tokens=30)
        emb = self.vector_store.get_embedding(query)
        answer = self._generate_response("system", query)
        self.conversation_history.append({"role": "user", "content": query})
        self.conversation_history.append({"role": "assistant", "content": answer})
        self.no_rag_counter += 1
        return {
            "success": True,
            "response": answer,
            "sources": [{"source": "fake", "similarity": emb[0]}],
            "used_rag": route == "gateway-output",
            "topic": "test",
        }


class AdapterTest(unittest.TestCase):
    def build(self, fail_first=False):
        runtimes = []
        delegate = FakeDelegateGateway(fail_first=fail_first)
        embedding = FakeEmbeddingGateway()
        store = InMemorySessionStore()
        tracer = EventTracer()
        executor = PsyChatExecutor(
            runtime_factory=lambda: FakePsyChatRuntime(runtimes),
            model_gateway=ResilientModelGateway(
                delegate,
                attempts=2,
                timeout_s=7.0,
            ),
            embedding_gateway=embedding,
            session_store=store,
            safety_gate=FakeSafetyGate(),
            tracer=tracer,
        )
        return executor, delegate, embedding, store, tracer, runtimes

    def test_known_provider_calls_are_intercepted(self):
        executor, delegate, embedding, _, tracer, runtimes = self.build()
        result = executor.execute(
            ExecutionRequest(
                "a",
                "hello",
                RouteDecision("rag.respond", "psychat_adapted"),
            )
        )
        self.assertEqual(result.status, "ok")
        self.assertEqual(len(delegate.calls), 2)
        self.assertEqual(len(embedding.calls), 1)
        self.assertIsNone(runtimes[0].tts_service)
        self.assertEqual(runtimes[0].conversation_history, [])
        self.assertEqual(
            [event["event"] for event in tracer.events],
            ["executor.started", "executor.completed"],
        )

    def test_session_state_is_externalized_and_isolated(self):
        executor, _, _, store, _, _ = self.build()
        route = RouteDecision("rag.respond", "psychat_adapted")
        executor.execute(ExecutionRequest("A", "a1", route))
        executor.execute(ExecutionRequest("B", "b1", route))
        executor.execute(ExecutionRequest("A", "a2", route))
        session_a = store.load("A")["conversation_history"]
        session_b = store.load("B")["conversation_history"]
        self.assertEqual(
            [x["content"] for x in session_a if x["role"] == "user"],
            ["a1", "a2"],
        )
        self.assertEqual(
            [x["content"] for x in session_b if x["role"] == "user"],
            ["b1"],
        )

    def test_gateway_retry_boundary(self):
        executor, delegate, _, _, _, _ = self.build(fail_first=True)
        result = executor.execute(
            ExecutionRequest(
                "A",
                "hello",
                RouteDecision("rag.respond", "psychat_adapted"),
            )
        )
        self.assertEqual(result.status, "ok")
        self.assertGreaterEqual(len(delegate.calls), 3)
        self.assertTrue(all(call["timeout_s"] == 7.0 for call in delegate.calls))

    def test_registry_adds_executor_without_switch(self):
        executor, *_ = self.build()
        registry = CapabilityRegistry()
        registry.register("rag.respond", executor)
        self.assertIs(
            registry.resolve("rag.respond", "psychat_adapted"),
            executor,
        )

    def test_validator_rejects_bad_donor_result(self):
        class BadRuntime(FakePsyChatRuntime):
            def generate_response(self, query):
                return {"success": True, "response": "", "sources": []}

        executor = PsyChatExecutor(
            runtime_factory=lambda: BadRuntime([]),
            model_gateway=ResilientModelGateway(FakeDelegateGateway()),
            embedding_gateway=FakeEmbeddingGateway(),
            session_store=InMemorySessionStore(),
            safety_gate=FakeSafetyGate(),
            tracer=EventTracer(),
        )
        with self.assertRaises(ContractError):
            executor.execute(
                ExecutionRequest(
                    "A",
                    "hello",
                    RouteDecision("rag.respond", "psychat_adapted"),
                )
            )

    def test_independent_safety_gate_can_block(self):
        class UnsafeRuntime(FakePsyChatRuntime):
            def generate_response(self, query):
                self.conversation_history.append({"role": "user", "content": query})
                return {
                    "success": True,
                    "response": "UNSAFE",
                    "sources": [],
                    "used_rag": False,
                }

        executor = PsyChatExecutor(
            runtime_factory=lambda: UnsafeRuntime([]),
            model_gateway=ResilientModelGateway(FakeDelegateGateway()),
            embedding_gateway=FakeEmbeddingGateway(),
            session_store=InMemorySessionStore(),
            safety_gate=FakeSafetyGate(),
            tracer=EventTracer(),
        )
        result = executor.execute(
            ExecutionRequest(
                "A",
                "hello",
                RouteDecision("rag.respond", "psychat_adapted"),
            )
        )
        self.assertEqual(result.status, "blocked")
        self.assertEqual(result.response, "blocked")


if __name__ == "__main__":
    unittest.main()
