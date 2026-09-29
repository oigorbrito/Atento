import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from evals.atentoeval import runner


class RunnerAgentScopeTest(unittest.TestCase):
    def test_release_gates_reject_mixed_primary_agents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cases = root / "cases.jsonl"
            results = root / "results.jsonl"
            gates = root / "gates.json"

            cases.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "id": "anna",
                                "suite": "core",
                                "source_id": "SRC-ATENTO",
                                "agent_scope": "ANNA",
                                "steps": [{"user": "x", "expected": {}}],
                            }
                        ),
                        json.dumps(
                            {
                                "id": "naia",
                                "suite": "tools",
                                "source_id": "SRC-ATENTO",
                                "agent_scope": "NAIA",
                                "steps": [{"user": "y", "expected": {}}],
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            results.write_text(
                "\n".join(
                    [
                        json.dumps(
                            {
                                "case_id": "anna",
                                "step_index": 0,
                                "response": "ok",
                                "trace": {},
                            }
                        ),
                        json.dumps(
                            {
                                "case_id": "naia",
                                "step_index": 0,
                                "response": "ok",
                                "trace": {},
                            }
                        ),
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            gates.write_text(json.dumps({"gates": []}), encoding="utf-8")

            argv = [
                "runner",
                "--cases",
                str(cases),
                "--results",
                str(results),
                "--gates",
                str(gates),
            ]
            with patch("sys.argv", argv):
                with self.assertRaisesRegex(
                    ValueError, "cannot mix multiple primary agent scopes"
                ):
                    runner.main()


if __name__ == "__main__":
    unittest.main()
