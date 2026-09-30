import json
import tempfile
import unittest
from pathlib import Path

from evals.atentoeval.candidates import (
    AgentScope,
    CandidateClass,
    CandidateResult,
    EvidenceStatus,
    SelectionStatus,
    github_matrix,
    load_registry,
    write_static_result,
)


REGISTRY = Path("evals/config/candidates.json")


class CandidateRegistryTest(unittest.TestCase):
    def test_repository_registry_is_valid_and_pinned(self):
        candidates = load_registry(REGISTRY)
        by_id = {candidate.candidate_id: candidate for candidate in candidates}
        self.assertIn("psychat_upstream", by_id)
        self.assertEqual(
            by_id["psychat_upstream"].upstream_sha,
            "5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4",
        )
        self.assertIsNone(by_id["atento_native_rag"].repository)
        self.assertEqual(by_id["psychat_upstream"].agent_scope, AgentScope.ANNA)
        self.assertEqual(
            by_id["psychat_upstream"].candidate_class,
            CandidateClass.UNCLASSIFIED_PENDING_AUDIT,
        )
        self.assertEqual(
            by_id["psychat_upstream"].selection_status,
            SelectionStatus.NOT_SELECTED,
        )
        self.assertEqual(
            by_id["atento_native_rag"].selection_status,
            SelectionStatus.NOT_APPLICABLE,
        )

    def test_ci_matrix_contains_only_enabled_supported_candidates(self):
        matrix = github_matrix(REGISTRY)
        ids = [item["candidate_id"] for item in matrix["include"]]
        self.assertEqual(ids, ["psychat_upstream"])


    def test_registry_rejects_selected_candidate_during_decision_reset(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidates.json"
            path.write_text(
                json.dumps(
                    {
                        "policy": {
                            "decision_authority": False,
                            "selection_state": "DECISION_RESET",
                            "candidate_universe_complete": False,
                        },
                        "candidates": [
                            {
                                "candidate_id": "selected-too-early",
                                "block": "I",
                                "source_id": "SRC-X",
                                "variant": "UPSTREAM",
                                "adapter_id": "selected-too-early",
                                "repository": "owner/repo",
                                "upstream_sha": "a" * 40,
                                "selection_status": "SELECTED",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "decision_authority is false"):
                load_registry(path)

    def test_external_candidate_without_pin_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidates.json"
            path.write_text(
                json.dumps(
                    {
                        "candidates": [
                            {
                                "candidate_id": "bad",
                                "block": "I",
                                "source_id": "SRC-X",
                                "variant": "UPSTREAM",
                                "adapter_id": "bad",
                                "repository": "owner/repo",
                                "upstream_sha": None,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_registry(path)

    def test_static_result_is_typed_pass_static_not_runtime_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            audit = Path(tmp) / "audit.json"
            output = Path(tmp) / "result.json"
            audit.write_text(
                json.dumps({"chassis_fitness_score": 10, "checks_passed": 1}),
                encoding="utf-8",
            )
            result = write_static_result(
                registry=REGISTRY,
                candidate_id="psychat_upstream",
                audit=audit,
                atento_sha="a" * 40,
                output=output,
            )
            self.assertEqual(result.evidence_status, EvidenceStatus.PASS_STATIC.value)
            saved = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(saved["evaluation_kind"], "static_chassis")
            self.assertEqual(saved["agent_scope"], "ANNA")
            self.assertEqual(saved["selection_status"], "NOT_SELECTED")
            self.assertEqual(saved["chassis"]["chassis_fitness_score"], 10)

    def test_candidate_result_rejects_unknown_status(self):
        result = CandidateResult(
            candidate_id="x",
            block="I",
            source_id="SRC-X",
            variant="NATIVE",
            evidence_status="PASS_RUNTIME_INVENTED",
            evaluation_kind="unit",
            atento_sha="a" * 40,
        )
        with self.assertRaises(ValueError):
            result.validate()


if __name__ == "__main__":
    unittest.main()
