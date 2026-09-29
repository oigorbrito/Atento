import unittest

from evals.spikes.psychat.adapter.contracts import ExecutionResult
from evals.spikes.psychat.atentoeval_adapter import to_turn_result


class PsyChatAtentoEvalAdapterTest(unittest.TestCase):
    def test_maps_rag_and_executor_trace(self):
        result = ExecutionResult(
            response="ok",
            executor="psychat",
            capability="knowledge.rag",
            trace=(
                {
                    "event": "rag.completed",
                    "attempted": True,
                    "used": True,
                    "retrieved_count": 2,
                    "retrieved_ids": ["d1", "d2"],
                },
                {
                    "event": "executor.completed",
                    "capability": "knowledge.rag",
                    "executor": "psychat",
                    "reason_code": "knowledge_needed",
                },
            ),
        )

        turn = to_turn_result(
            case_id="rag.retrieve.001",
            step_index=0,
            result=result,
        )

        self.assertTrue(turn.trace["rag"]["attempted"])
        self.assertEqual(turn.trace["rag"]["retrieved_ids"], ["d1", "d2"])
        self.assertEqual(turn.trace["executive"]["executor"], "psychat")
        self.assertEqual(
            turn.trace["executive"]["reason_code"],
            "knowledge_needed",
        )


if __name__ == "__main__":
    unittest.main()
