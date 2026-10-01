import unittest

from evals.atentoeval.gate2_composition import (
    AssertionRecord,
    HARNESS_VERSION,
    build_summary,
    evaluate_assertions,
    validate_manifest,
)


def manifest():
    return {
        "agent_scope": "NAIA",
        "candidate": "fixture",
        "upstream_repo": "example/fixture",
        "upstream_sha": "a" * 40,
        "composition_profile_hash": "profile-hash",
        "policy_hash": "policy-hash",
        "harness_version": HARNESS_VERSION,
    }


def records(state="PASS", repair_class=""):
    return [
        AssertionRecord(f"ISO-{i}", state, repair_class=repair_class)
        for i in range(1, 7)
    ]


class Gate2CompositionTest(unittest.TestCase):
    def test_all_common_assertions_pass(self):
        report = evaluate_assertions(records())
        self.assertEqual(report["state"], "PASS_WITH_SCOPE")

    def test_missing_common_assertion_is_invalid(self):
        report = evaluate_assertions(records()[:-1])
        self.assertEqual(report["state"], "INVALID_EVIDENCE")
        self.assertEqual(report["missing"], ["ISO-6"])

    def test_blocked_is_not_candidate_failure(self):
        rows = records()
        rows[2] = AssertionRecord("ISO-3", "BLOCKED", "runner unavailable")
        report = evaluate_assertions(rows)
        self.assertEqual(report["state"], "BLOCKED_ENVIRONMENT")
        self.assertEqual(report["blocked"], ["ISO-3"])

    def test_local_failure_stays_local(self):
        rows = records()
        rows[3] = AssertionRecord("ISO-4", "FAIL", repair_class="LOCALIZED_REPAIR")
        report = evaluate_assertions(rows)
        self.assertEqual(report["state"], "FAIL_LOCALIZED")

    def test_cross_cutting_failure_is_structural(self):
        rows = records()
        rows[4] = AssertionRecord(
            "ISO-5",
            "FAIL",
            repair_class="CROSS_CUTTING_STRUCTURAL_REWRITE",
        )
        report = evaluate_assertions(rows)
        self.assertEqual(report["state"], "FAIL_STRUCTURAL")

    def test_manifest_requires_full_sha(self):
        bad = manifest()
        bad["upstream_sha"] = "deadbeef"
        with self.assertRaisesRegex(ValueError, "full 40-character"):
            validate_manifest(bad)

    def test_summary_preserves_exact_identity(self):
        m = manifest()
        summary = build_summary(m, records())
        self.assertEqual(summary["candidate"], "fixture")
        self.assertEqual(summary["upstream_sha"], "a" * 40)
        self.assertEqual(summary["result"]["state"], "PASS_WITH_SCOPE")


if __name__ == "__main__":
    unittest.main()
