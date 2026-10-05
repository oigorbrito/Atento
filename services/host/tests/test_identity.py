from __future__ import annotations

import base64
import json
import unittest

from atento_host.identity import IdentityIssuer, IdentityRejected


class IdentityIssuerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.now = 1_800_000_000
        self.issuer = IdentityIssuer(
            signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
            role_grants={
                "subject-naia": {"NAIA": {"calendar.read", "tasks.write"}},
                "subject-anna": {"ANNA": {"anna.memory.read"}},
            },
            clock=lambda: self.now,
        )

    def issue(self, **overrides: object) -> str:
        claims = {
            "authenticated_principal_id": "subject-naia",
            "role_id": "NAIA",
            "session_id": "session-1",
            "run_id": "run-1",
            "generation": 1,
        }
        claims.update(overrides)
        return self.issuer.issue(**claims)  # type: ignore[arg-type]

    def test_issues_identity_with_host_configured_grants(self) -> None:
        token = self.issue()
        identity = self.issuer.verify(
            token,
            expected_role_id="NAIA",
            expected_session_id="session-1",
            expected_run_id="run-1",
            expected_generation=1,
        )
        self.assertEqual(identity.principal_id, "subject-naia")
        self.assertEqual(identity.granted_capability_set, ("calendar.read", "tasks.write"))
        self.assertEqual(identity.issuer, "atento-host-control-plane")

    def test_caller_cannot_assign_itself_another_role(self) -> None:
        with self.assertRaisesRegex(IdentityRejected, "not authorized for role"):
            self.issue(role_id="ANNA")

    def test_caller_cannot_borrow_another_principals_role(self) -> None:
        with self.assertRaisesRegex(IdentityRejected, "not authorized for role"):
            self.issue(authenticated_principal_id="subject-anna", role_id="NAIA")

    def test_malformed_role_claim_is_rejected_without_type_error(self) -> None:
        with self.assertRaisesRegex(IdentityRejected, "unsupported role"):
            self.issue(role_id=[])  # type: ignore[arg-type]

    def test_generation_and_binding_must_match_expected_run(self) -> None:
        token = self.issue()
        with self.assertRaisesRegex(IdentityRejected, "generation binding mismatch"):
            self.issuer.verify(token, expected_generation=2)
        with self.assertRaisesRegex(IdentityRejected, "run binding mismatch"):
            self.issuer.verify(token, expected_run_id="other-run")

    def test_expired_identity_is_rejected(self) -> None:
        token = self.issue(ttl_seconds=1)
        self.now += 1
        with self.assertRaisesRegex(IdentityRejected, "not currently valid"):
            self.issuer.verify(token)

    def test_expiry_cannot_exceed_configured_ttl(self) -> None:
        with self.assertRaisesRegex(IdentityRejected, "outside host policy"):
            self.issue(ttl_seconds=301)

    def test_modified_payload_is_rejected(self) -> None:
        token = self.issue()
        encoded, signature = token.split(".")
        claims = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)))
        claims["role_id"] = "ANNA"
        changed = base64.urlsafe_b64encode(
            json.dumps(claims, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).rstrip(b"=").decode("ascii")
        with self.assertRaisesRegex(IdentityRejected, "signature is invalid"):
            self.issuer.verify(changed + "." + signature)

    def test_malformed_or_noncanonical_tokens_fail_closed(self) -> None:
        for token in ("", "a", "a.b.c", "!bad.abc", "x" * 9000):
            with self.subTest(token=token[:12]), self.assertRaises(IdentityRejected):
                self.issuer.verify(token)

    def test_short_or_missing_signing_key_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 32 bytes"):
            IdentityIssuer(signing_key=b"short", role_grants={})

    def test_token_cannot_be_replayed_for_another_audience(self) -> None:
        token = self.issue()
        other_audience = IdentityIssuer(
            signing_key=b"test-only-signing-key-which-is-32-bytes-minimum",
            role_grants={"subject-naia": {"NAIA": {"calendar.read", "tasks.write"}}},
            audience="different-runtime",
            clock=lambda: self.now,
        )
        with self.assertRaisesRegex(IdentityRejected, "issuer, audience, or version"):
            other_audience.verify(token)


if __name__ == "__main__":
    unittest.main()
