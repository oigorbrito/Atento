import unittest

from evals.atentoeval.metrics import score_turn, summarize_scores
from evals.atentoeval.schema import Expected, TurnResult


class MetricsTest(unittest.TestCase):
    def test_process_metrics(self):
        expected = Expected(
            accepted_strategies=["validation", "clarification"],
            memory_ids=["m1", "m2"],
            tool_calls=["weather"],
            safety_route="normal",
        )
        result = TurnResult(
            case_id="x",
            step_index=0,
            response="ok",
            trace={
                "plan": {"strategy": "validation"},
                "memory": {"retrieved_ids": ["m1"]},
                "tools": [{"name": "weather"}],
                "safety": {"route": "normal"},
            },
            latency_ms=100,
            usage={"cost_usd": 0.01},
        )
        scores = score_turn(expected, result)
        self.assertEqual(scores["strategy_hit"], 1.0)
        self.assertEqual(scores["memory_precision"], 1.0)
        self.assertEqual(scores["memory_recall"], 0.5)
        self.assertEqual(scores["tool_f1"], 1.0)
        self.assertEqual(scores["safety_route_hit"], 1.0)

    def test_summary_counts_critical_failures(self):
        rows = [
            {"suite": "safety", "scores": {"critical_failure": 1.0}},
            {"suite": "safety", "scores": {"critical_failure": 0.0}},
        ]
        summary = summarize_scores(rows)
        self.assertEqual(summary["overall"]["critical_failure_count"], 1.0)
        self.assertEqual(summary["overall"]["critical_failure_rate"], 0.5)


if __name__ == "__main__":
    unittest.main()
