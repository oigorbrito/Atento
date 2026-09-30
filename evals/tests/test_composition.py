import unittest

from evals.atentoeval.composition import (
    CompositionValidationError,
    HARNESS_VERSION,
    sha256_json,
    validate_result,
)


MATRIX = {
    "version": HARNESS_VERSION,
    "common_assertions_per_candidate": 6,
    "candidates": [
        {
            "name": "AI Butler",
            "repo": "LumabyteCo/aibutler",
            "sha": "c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c",
            "add_ons": [],
        },
        {
            "name": "AgentOS",
            "repo": "use-agent-os/agent-os",
            "sha": "226c906291fc68f3c4517623446bdaec1b48a82d",
            "add_ons": ["browser_effect_policy"],
        },
    ],
}


def base_result(candidate="AI Butler"):
    profile = {"roles": ["NAIA", "Anna"], "stores": "separate"}
    policy = {"cross_role": "broker_only"}
    sha = MATRIX["candidates"][0]["sha"] if candidate == "AI Butler" else MATRIX["candidates"][1]["sha"]
    repo = MATRIX["candidates"][0]["repo"] if candidate == "AI Butler" else MATRIX["candidates"][1]["repo"]
    assertions = []
    for i in range(1, 7):
        item = {
            "id": f"ISO-{i}",
            "state": "PASS",
            "evidence_kind": "runtime_candidate",
        }
        if i == 6:
            item["evidence_kind"] = "runtime_broker"
            item["broker_endpoint_or_adapter"] = "atento-broker-v1"
        assertions.append(item)
    return {
        "candidate": candidate,
        "harness_version": HARNESS_VERSION,
        "upstream_repo": repo,
        "upstream_sha": sha,
        "state": "PASS_WITH_SCOPE",
        "composition_profile": profile,
        "composition_profile_hash": sha256_json(profile),
        "policy": policy,
        "policy_hash": sha256_json(policy),
        "assertions": assertions,
        "add_ons": [],
    }


class CompositionEvidenceTest(unittest.TestCase):
    def test_valid_common_result(self):
        summary = validate_result(MATRIX, base_result())
        self.assertTrue(summary["valid"])
        self.assertEqual(summary["common_passed"], 6)

    def test_wrong_sha_is_rejected(self):
        result = base_result()
        result["upstream_sha"] = "0" * 40
        with self.assertRaises(CompositionValidationError):
            validate_result(MATRIX, result)

    def test_synthetic_broker_cannot_close_iso6(self):
        result = base_result()
        result["assertions"][-1]["evidence_kind"] = "synthetic_fixture"
        result["assertions"][-1].pop("broker_endpoint_or_adapter")
        with self.assertRaises(CompositionValidationError) as ctx:
            validate_result(MATRIX, result)
        codes = {x.code for x in ctx.exception.issues}
        self.assertIn("iso6.synthetic_broker", codes)

    def test_static_source_cannot_be_runtime_pass(self):
        result = base_result()
        result["assertions"][0]["evidence_kind"] = "static_source_only"
        with self.assertRaises(CompositionValidationError):
            validate_result(MATRIX, result)

    def test_addon_is_required_for_frontier_candidate(self):
        result = base_result("AgentOS")
        with self.assertRaises(CompositionValidationError) as ctx:
            validate_result(MATRIX, result)
        self.assertIn("addon.missing", {x.code for x in ctx.exception.issues})

    def test_addon_runtime_pass_closes_candidate(self):
        result = base_result("AgentOS")
        result["add_ons"] = [
            {
                "id": "browser_effect_policy",
                "state": "PASS",
                "evidence_kind": "runtime_candidate",
            }
        ]
        summary = validate_result(MATRIX, result)
        self.assertEqual(summary["required_add_ons"], ["browser_effect_policy"])

    def test_blocked_environment_requires_blocker_id(self):
        result = base_result()
        result["state"] = "BLOCKED_ENVIRONMENT"
        result["assertions"] = []
        with self.assertRaises(CompositionValidationError):
            validate_result(MATRIX, result)
        result["blocker_id"] = "NAIA-G2-EXEC-INFRA-2026-09-30-01"
        summary = validate_result(MATRIX, result)
        self.assertEqual(summary["state"], "BLOCKED_ENVIRONMENT")

    def test_false_pass_with_failed_assertion_is_rejected(self):
        result = base_result()
        result["assertions"][2]["state"] = "FAIL"
        with self.assertRaises(CompositionValidationError) as ctx:
            validate_result(MATRIX, result)
        self.assertIn("result.false_pass", {x.code for x in ctx.exception.issues})


if __name__ == "__main__":
    unittest.main()
