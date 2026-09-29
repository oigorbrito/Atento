import json
import tempfile
import unittest
from pathlib import Path

from evals.atentoeval.candidates import (
    CandidateResult,
    EvidenceStatus,
    github_matrix,
    load_registry,
    write_empirical_result,
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
        self.assertEqual(
            by_id["openclaw_upstream"].upstream_sha,
            "e9571d77e76bd6d35996273d9e8398ad539b26e1",
        )
        self.assertEqual(
            by_id["openclaw_upstream"].ci_profile,
            "openclaw_naya_local_delta",
        )

    def test_ci_matrix_contains_only_enabled_supported_candidates(self):
        matrix = github_matrix(REGISTRY)
        ids = [item["candidate_id"] for item in matrix["include"]]
        self.assertEqual(ids, ["psychat_upstream", "openclaw_upstream"])
        static = github_matrix(REGISTRY, profile="python_static_chassis")
        self.assertEqual(
            [item["candidate_id"] for item in static["include"]],
            ["psychat_upstream"],
        )
        openclaw = github_matrix(REGISTRY, profile="openclaw_naya_local_delta")
        self.assertEqual(
            [item["candidate_id"] for item in openclaw["include"]],
            ["openclaw_upstream"],
        )

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
            self.assertEqual(saved["chassis"]["chassis_fitness_score"], 10)

    def test_empirical_result_preserves_architecture_risk(self):
        with tempfile.TemporaryDirectory() as tmp:
            probe = Path(tmp) / "probe.json"
            output = Path(tmp) / "result.json"
            probe.write_text(
                json.dumps(
                    {
                        "protocol": "openclaw_naya_local_delta_v1",
                        "evaluation_kind": "openclaw_naya_local_delta",
                        "evidence_status": "ARCH_RISK",
                        "cases": {
                            "OC-NAYA-001": {"status": "PASS_EMPIRICAL"},
                            "OC-NAYA-002": {"status": "ARCH_RISK"},
                        },
                        "git_surface": {"donor_internal_files_modified": 0},
                        "blockers": [
                            {
                                "code": "GENERIC_EFFECT_DURABILITY_NOT_PROVEN",
                                "kind": "architecture",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = write_empirical_result(
                registry=REGISTRY,
                candidate_id="openclaw_upstream",
                probe=probe,
                atento_sha="b" * 40,
                output=output,
            )
            self.assertEqual(result.evidence_status, EvidenceStatus.ARCH_RISK.value)
            self.assertEqual(result.evaluation_kind, "openclaw_naya_local_delta")
            self.assertEqual(result.git_surface["donor_internal_files_modified"], 0)
            saved = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(saved["benchmark"]["cases"]["OC-NAYA-002"]["status"], "ARCH_RISK")

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
