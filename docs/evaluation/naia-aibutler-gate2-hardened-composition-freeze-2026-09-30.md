# NAIA Gate-2 AI Butler hardened composition freeze — 2026-09-30

## Purpose

Freeze the AI Butler Gate-2 composition and repair the evidence path so the next executable run cannot claim ISO-6 from a synthetic echo.

Candidate:

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

Frozen profile:

`evals/config/naia_gate2_aibutler_v1.json`

## Reused exact-pin evidence

The upstream exact pin already carries run-backed bank-isolation and scoped scheduled-capability evidence. Gate 2 therefore executes only the Atento composition delta.

## Frozen composition

```text
memory:
  NAIA bank = naia
  Anna bank = anna
  cross-bank access = deny

credentials:
  NAIA vault = independent
  Anna vault = independent
  cross-vault access = deny

tools/channels:
  capability sets = role scoped
  agent.delegate = not granted

cross-role:
  native delegation = absent
  allowed crossing = explicit Atento handoff broker only
```

## ISO-6 evidence correction

The previous injected Go test used an in-process `brokerHandoff` echo. That was intentionally insufficient under the canonical evidence validator:

```text
synthetic broker != runtime_broker
```

The composition now invokes:

`tools/naia_gate2/broker_runtime_adapter.py`

which imports and executes:

`evals.atentoeval.handoff_broker.ExplicitHandoffBroker`

The runtime test verifies:

- a bounded NAIA -> Anna handoff succeeds through the actual Atento broker implementation;
- the returned envelope is unchanged;
- an authority-bearing `credential` field is rejected;
- the forbidden credential value is not emitted by the adapter error surface.

The workflow exports the broker adapter path into the injected exact-pin test rather than copying/reimplementing broker logic in Go.

## Canonical result path

After the candidate assertions pass, the workflow now:

1. builds `evals/results/naia_gate2_aibutler_runtime.json`;
2. recomputes and verifies the frozen topology/policy hashes;
3. validates the result with `evals.atentoeval.composition validate-result`;
4. uploads the validated result as a workflow artifact.

Therefore a future green job must satisfy the same validator that rejects synthetic ISO-6 evidence.

## Evidence identity

```text
composition_profile_hash =
d79deed3c708bbb5b8136c526ff1bc7436a8c5838c5d50025b718d2c32f1f579

policy_hash =
f4697f0db81984e54be06b0b33b91c70ca565155feced3b4762e511504a6be16
```

## Current disposition

```text
AI_BUTLER_COMPOSITION = FROZEN_V1
AI_BUTLER_SYNTHETIC_ISO6 = REMOVED
AI_BUTLER_RUNTIME_BROKER_PATH = WIRED
AI_BUTLER_RESULT_VALIDATION = WIRED
AI_BUTLER_EXECUTION = NOT_YET_OBSERVED_AFTER_HARNESS_REPAIR

AI_BUTLER_GATE2_PASS = NOT_CLAIMED
AI_BUTLER_CANDIDATE_FAIL = NOT_CLAIMED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The prior runner-provisioning failures remain infrastructure evidence only. The first valid Gate-2 execution target remains AI Butler.
