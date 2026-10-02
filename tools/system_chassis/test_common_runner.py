"""Contract tests for the serial common chassis runner (no candidate qualification)."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from common_runner import CASE_EXPECTATIONS, ContractError, evaluate_observations, run_cohort, validate_manifest


def manifest() -> dict:
    path = Path(__file__).parents[2] / "evals" / "config" / "system_chassis_cohort_v1.json"
    return json.loads(path.read_text(encoding="utf-8"))


class CommonRunnerContractTests(unittest.TestCase):
    def test_requires_frozen_eight_assertions_and_eleven_candidates(self) -> None:
        validate_manifest(manifest())
        invalid = manifest()
        invalid["candidates"].pop()
        with self.assertRaises(ContractError):
            validate_manifest(invalid)

    def test_missing_or_malformed_observation_is_blocked(self) -> None:
        outcomes = evaluate_observations({"SYS-CHAT-01": {"own_session_read": {"observed": "ALLOWED"}}})
        self.assertEqual(outcomes["SYS-CHAT-01"], "BLOCKED")
        self.assertEqual(outcomes["SYS-MEM-01"], "BLOCKED")

    def test_reproduced_false_observation_is_scoped_failure(self) -> None:
        observations = {
            assertion: {
                case: {"observed": expected, "evidence_file": "raw.json"}
                for case, expected in cases.items()
            }
            for assertion, cases in CASE_EXPECTATIONS.items()
        }
        expected_rows = CASE_EXPECTATIONS["SYS-MEM-01"]["cross_role_marker_read"]
        observations["SYS-MEM-01"]["cross_role_marker_read"]["observed"] = [
            {**row, "outcome": "FOUND"} if index == 0 else row
            for index, row in enumerate(expected_rows)
        ]
        outcomes = evaluate_observations(observations, {"raw.json"})
        self.assertEqual(outcomes["SYS-MEM-01"], "FAIL_WITH_SCOPE")
        self.assertEqual(outcomes["SYS-CHAT-01"], "PASS_WITH_SCOPE")

    def test_observation_without_hashed_artifact_cannot_pass(self) -> None:
        observations = {
            assertion: {
                case: {"observed": expected, "evidence_file": "missing.json"}
                for case, expected in cases.items()
            }
            for assertion, cases in CASE_EXPECTATIONS.items()
        }
        outcomes = evaluate_observations(observations, set())
        self.assertTrue(all(state == "BLOCKED" for state in outcomes.values()))

    def test_verified_counterexample_is_scoped_failure_even_if_other_cases_are_missing(self) -> None:
        observations = {
            assertion: {
                case: {"observed": expected, "evidence_file": "raw.json"}
                for case, expected in cases.items()
            }
            for assertion, cases in CASE_EXPECTATIONS.items()
        }
        observations["SYS-MEM-01"]["cross_role_marker_read"]["observed"] = [
            {**row, "outcome": "FOUND"} if index == 0 else row
            for index, row in enumerate(CASE_EXPECTATIONS["SYS-MEM-01"]["cross_role_marker_read"])
        ]
        del observations["SYS-MEM-01"]["own_marker_read"]
        outcomes = evaluate_observations(observations, {"raw.json"})
        self.assertEqual(outcomes["SYS-MEM-01"], "FAIL_WITH_SCOPE")
        self.assertEqual(outcomes["SYS-CHAT-01"], "PASS_WITH_SCOPE")

    def test_unregistered_adapters_are_blocked_and_remain_in_order(self) -> None:
        data = manifest()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            result = run_cohort(
                data,
                atento_sha="test-only",
                checkout_root=root / "checkouts",
                adapter_root=root / "adapters",
                artifact_root=root / "artifacts",
            )
        self.assertEqual(result["cohort_size"], 11)
        self.assertEqual(result["candidate_execution_order"], [row["candidate_id"] for row in data["candidates"]])
        self.assertTrue(all(row["status"] == "BLOCKED_ADAPTER" for row in result["results"]))
        self.assertEqual(result["candidate_failures_inferred_from_missing_evidence"], 0)


if __name__ == "__main__":
    unittest.main()
