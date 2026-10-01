# NAIA Gate-2 AI Butler empirical composition result — 2026-10-01

## Classification

`PASS_WITH_SCOPE` for the frozen AI Butler Gate-2 composition.

This closes the six common Gate-2 isolation assertions for the exact AI Butler pin and the frozen Atento composition. It does **not** select AI Butler as the NAIA base, does not rank it against the remaining candidates, and does not prove later product/performance/lifecycle gates.

Candidate:

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

Harness:

`NAIA-GATE2-COMPOSITION-V1`

Frozen config:

`evals/config/naia_gate2_aibutler_v1.json`

Preserved result:

`evals/results/naia_gate2_aibutler_runtime_2026-10-01.json`

## Execution identity

The prior hosted run was re-executed only to prove that runner provisioning had recovered. That older run succeeded but still belonged to the obsolete synthetic-ISO-6 harness and is **not** the accepted Gate-2 evidence.

Accepted run:

```text
workflow = NAIA Gate2 AI Butler Composition
run_id = 36801793397
job_id = 110177534395
event = pull_request
probe PR = #56
head branch = eval/naia-gate2-aibutler-runtime-20261001
probe branch commit = d15e07a984cadd319a2810c388ebb8df7d063696
candidate pin = c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c
Go = 1.26.5 linux/amd64
job conclusion = success
```

The PR changed only a workflow comment so the repaired workflow could be observed through pull-request run tooling. It made no harness-logic or candidate-source change.

## Observed assertions

The exact-pin injected test executed:

```text
ISO-1 cross-memory read denied            = PASS
ISO-2 cross-memory mutation denied        = PASS
ISO-3 cross-credential use denied         = PASS
ISO-4 cross-tool/channel use denied       = PASS
ISO-5 silent cross-role invocation denied = PASS
ISO-6 explicit Atento broker control      = PASS
```

Observed test runtime:

```text
TestAtentoGate2Composition = PASS
elapsed ~= 0.88s
```

ISO-6 invoked the real Atento broker adapter:

`tools/naia_gate2/broker_runtime_adapter.py`

which imports and executes:

`evals.atentoeval.handoff_broker.ExplicitHandoffBroker`

The positive bounded NAIA -> Anna handoff succeeded. The negative authority-bearing `credential` field was rejected and the forbidden credential value was not emitted.

Therefore:

```text
SYNTHETIC_BROKER = NOT_USED
ISO6_EVIDENCE_KIND = runtime_broker
```

## Canonical validation

The workflow built the canonical result and then executed:

`python3 -m evals.atentoeval.composition validate-result`

Observed validator summary:

```text
state = PASS_WITH_SCOPE
common_passed = 6
```

The validator completed successfully before evidence upload.

## Artifact identity

GitHub Actions artifact:

```text
artifact_id = 11136566058
artifact_name = naia-gate2-aibutler-807184e1b7e7a23387dcf867d6c7e2af6440ab5c
artifact_size = 1090 bytes
artifact_zip_sha256 = a9d13826c34b0e51c847e3a81226a14b57a21943f4362c7d069ed13c1421dae1
```

The uploaded JSON was downloaded and inspected after the run. It records the exact frozen candidate pin, topology hash, policy hash, six PASS assertions and `ISO-6.evidence_kind = runtime_broker`.

## Scope

This pass establishes only the frozen Gate-2 composition:

- bank-scoped role memory;
- independent role vaults;
- role-scoped tool/channel capabilities;
- absence of native silent delegation;
- explicit Atento broker as the only tested cross-role positive path.

It does not establish:

- comparative superiority over another candidate;
- product performance;
- latency/cost advantage;
- full NAIA feature completeness;
- later lifecycle/recovery gates;
- shortlist or base selection.

## Current state

```text
AI_BUTLER_GATE2_COMPOSITION = PASS_WITH_SCOPE
AI_BUTLER_COMMON_ASSERTIONS = 6_OF_6_PASS
AI_BUTLER_ISO6 = PASS_RUNTIME_BROKER
AI_BUTLER_EVIDENCE_VALIDATOR = PASS
AI_BUTLER_ARTIFACT_PRESERVED = YES

GATE2_EMPIRICAL_PASS = 1
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Execution order now advances to OpenMausBot.
