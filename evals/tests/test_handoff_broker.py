import unittest

from evals.atentoeval.handoff_broker import (
    BrokerContractError,
    ExplicitHandoffBroker,
    validate_envelope,
)


class HandoffBrokerContractTest(unittest.TestCase):
    def setUp(self):
        self.valid = {
            "from_role": "NAIA",
            "to_role": "Anna",
            "kind": "handoff",
            "body": "bounded payload",
            "correlation_id": "case-001",
        }

    def test_valid_bounded_handoff_round_trips(self):
        broker = ExplicitHandoffBroker()
        self.assertEqual(broker.handoff(self.valid), self.valid)

    def test_same_role_is_rejected(self):
        data = dict(self.valid, to_role="NAIA")
        with self.assertRaises(BrokerContractError):
            validate_envelope(data)

    def test_unknown_field_is_rejected(self):
        data = dict(self.valid, debug=True)
        with self.assertRaises(BrokerContractError):
            validate_envelope(data)

    def test_memory_transfer_field_is_rejected(self):
        data = dict(self.valid, memory_ids=["anna-private"])
        with self.assertRaisesRegex(BrokerContractError, "authority-bearing"):
            validate_envelope(data)

    def test_credential_transfer_field_is_rejected(self):
        data = dict(self.valid, credential_value="secret")
        with self.assertRaisesRegex(BrokerContractError, "authority-bearing"):
            validate_envelope(data)

    def test_capability_or_tool_handle_is_rejected(self):
        for field in ("capabilities", "tool_handle", "channel_handle", "agent_handle"):
            with self.subTest(field=field):
                data = dict(self.valid)
                data[field] = "forbidden"
                with self.assertRaisesRegex(BrokerContractError, "authority-bearing"):
                    validate_envelope(data)

    def test_body_is_bounded(self):
        data = dict(self.valid, body="x" * 4097)
        with self.assertRaises(BrokerContractError):
            validate_envelope(data)

    def test_kind_is_allowlisted(self):
        data = dict(self.valid, kind="delegate_authority")
        with self.assertRaises(BrokerContractError):
            validate_envelope(data)


if __name__ == "__main__":
    unittest.main()
