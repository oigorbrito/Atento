# NAIA/Anna explicit handoff broker contract v1 — 2026-09-30

## Status

```text
BROKER_CONTRACT = FROZEN_V1
BROKER_IMPLEMENTATION = REFERENCE_HARNESS_COMPONENT
PRODUCTION_DEPLOYMENT = NOT_SELECTED
CANDIDATE_DEPENDENCY = NONE
```

This contract exists because Gate 2 requires a positive cross-role control:

```text
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

The broker is deliberately independent of the NAIA chassis candidate.

## Allowed envelope

Only these fields may cross the NAIA/Anna boundary:

```text
from_role
to_role
kind
body
correlation_id
```

Allowed kinds:

```text
handoff
request
response
```

The payload body is bounded to 4096 characters in the reference contract.

## Explicitly forbidden authority transfer

The broker contract has no authority-bearing transport surface.

It rejects undeclared fields and specifically rejects fields representing:

- memory or memory identifiers;
- credentials, tokens, API keys or secrets;
- capabilities;
- tool handles;
- channel handles;
- session/runtime handles;
- agent handles.

Therefore:

```text
BROKER_MESSAGE_TRANSFER != MEMORY_TRANSFER
BROKER_MESSAGE_TRANSFER != CREDENTIAL_TRANSFER
BROKER_MESSAGE_TRANSFER != TOOL_AUTHORITY_TRANSFER
BROKER_MESSAGE_TRANSFER != SESSION_OR_RUNTIME_TRANSFER
```

## Reference implementation

- `evals/atentoeval/handoff_broker.py`
- `evals/tests/test_handoff_broker.py`

The reference implementation is part of the evaluation harness. It is not yet a claim about the final production transport, service language, IPC mechanism or deployment topology.

## Gate-2 evidence rule

`ISO-6` may pass only when the actual composed candidate is wired to an explicit broker path conforming to this contract.

A local echo helper, mock function or synthetic struct round-trip is insufficient.

The Gate-2 result validator enforces:

```text
ISO-6 PASS
  => evidence_kind = runtime_broker
  => broker_endpoint_or_adapter is identified
```

## Consequence

The common broker contract is no longer ambiguous across candidates, but no candidate receives Gate-2 PASS from this document alone.

```text
BROKER_CONTRACT_FROZEN = YES
BROKER_RUNTIME_INTEGRATION_PROVEN = NO
GATE2_EMPIRICAL_PASS = 0
```
