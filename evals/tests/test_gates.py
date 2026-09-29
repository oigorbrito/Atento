import unittest

from evals.atentoeval.gates import evaluate_gates


class GatesTest(unittest.TestCase):
    def test_hard_gate_passes(self):
        config = {
            "gates": [
                {
                    "id": "critical",
                    "metric": "overall.critical_failure_count",
                    "max": 0,
                    "enabled": True,
                }
            ]
        }
        summary = {"overall": {"critical_failure_count": 0}}
        report = evaluate_gates(summary, config)
        self.assertTrue(report["passed"])

    def test_hard_gate_fails(self):
        config = {
            "gates": [
                {
                    "id": "critical",
                    "metric": "overall.critical_failure_count",
                    "max": 0,
                    "enabled": True,
                }
            ]
        }
        summary = {"overall": {"critical_failure_count": 1}}
        report = evaluate_gates(summary, config)
        self.assertFalse(report["passed"])


if __name__ == "__main__":
    unittest.main()
