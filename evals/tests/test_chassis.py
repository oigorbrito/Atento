import tempfile
import unittest
from pathlib import Path

from evals.chassis.donor_static_audit import audit


class ChassisAuditTest(unittest.TestCase):
    def test_decoupled_sample_scores_higher_than_coupled_sample(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "router.py").write_text(
                "def route(x):\n    return {'capability': 'x'}\n", encoding="utf-8"
            )
            (root / "runtime.py").write_text(
                "from dataclasses import dataclass\n"
                "@dataclass\n"
                "class ExecutionResult:\n"
                "    value: str\n"
                "class ExecutorAdapter: pass\n"
                "class CapabilityRegistry: pass\n"
                "class ModelGateway: pass\n"
                "def execute(): pass\n"
                "def validate_result(x): return x\n"
                "def retry_with_timeout(): pass\n"
                "logger = type('L', (), {'info': lambda *a, **k: None})()\n",
                encoding="utf-8",
            )
            (root / "safety.py").write_text(
                "def safety_check(x): return True\n", encoding="utf-8"
            )
            report = audit(root, "TEST")
            self.assertFalse(report["decision_authority"])
            self.assertEqual(report["selection_meaning"], "NONE")
            self.assertGreaterEqual(report["chassis_fitness_score"], 70)

    def test_direct_provider_and_local_session_state_are_visible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "app.py").write_text(
                "import requests\n"
                "class App:\n"
                "    def __init__(self):\n"
                "        self.conversation_history=[]\n"
                "    def generate_response(self):\n"
                "        return requests.post('https://provider.example/v1')\n",
                encoding="utf-8",
            )
            report = audit(root, "TEST")
            self.assertGreater(report["raw_metrics"]["direct_provider_bypass_count"], 0)
            self.assertGreater(report["raw_metrics"]["mutable_session_state_count"], 0)
            self.assertFalse(report["checks"]["provider_boundary"]["pass"])
            self.assertFalse(report["checks"]["state_externalization"]["pass"])


if __name__ == "__main__":
    unittest.main()
