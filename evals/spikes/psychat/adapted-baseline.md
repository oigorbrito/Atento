# PsyChat — Adapted Chassis Contract Probe

## Scope

This experiment tests whether PsyChat can be enclosed by an Atento chassis without rewriting the donor's core RAG logic.

It does **not** claim that the full donor runtime has executed successfully yet. GitHub Actions still has no runner allocation, and the local execution environment cannot clone GitHub directly.

## Adapter boundary

The probe introduces:

- structured route/execution/result contracts;
- `CapabilityRegistry`;
- `PsyChatExecutor`;
- provider interception for the three known donor seams:
  - `PsychologyAgent._call_llm`;
  - `RAGSystem._generate_response`;
  - `VectorStore.get_embedding`;
- external session-state storage;
- output normalization/validation;
- retry + timeout propagation through Model Gateway;
- independent Safety Gate;
- event tracing;
- TTS removed from the core execution path.

The donor-facing method names were verified against pinned PsyChat source commit
`5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`.

## Dynamic contract tests

Executed locally with Python 3.13.5 using a donor-shaped fake runtime that exposes the same integration surface used by the pinned donor.

```text
Ran 6 tests in 0.001s
OK
```

Passing tests:

1. known LLM/embedding provider paths are intercepted by the gateway;
2. session state is externalized and isolated by session ID;
3. retry and timeout boundary is exercised;
4. executor is registered without a central switch statement;
5. malformed donor output is rejected by the validator;
6. independent Safety Gate can block a candidate response.

## Chassis interpretation

| Fitness function | Upstream | Adapter probe |
|---|---|---|
| routing_boundary | PASS | PASS |
| executor_abstraction | FAIL | PASS |
| capability_registry | FAIL | PASS |
| structured_contracts | FAIL | PASS |
| output_validation | FAIL | PASS |
| provider_boundary | FAIL | PARTIAL |
| state_externalization | FAIL | PASS |
| observability_hooks | FAIL | PASS |
| resilience_boundary | FAIL | PASS |
| independent_safety_boundary | FAIL | PASS |

### Provisional adapted CFS

Using the conservative rule that `provider_boundary` remains FAIL until direct donor provider paths are structurally unreachable by construction:

> **Provisional adapted Chassis Fitness: 90/100**

This is a **contract-level result**, not yet a full donor runtime result.

## Evidence significance

The experiment supports the hypothesis that PsyChat's RAG capability can be retained behind an Atento chassis with a thin boundary.

It does **not** yet prove:

- actual PsyChat dependencies install cleanly;
- the real donor runs through these bindings;
- quality is preserved;
- latency/cost are acceptable;
- the full AtentoEval seed set passes.

## Next acceptance test

Run the real pinned donor through this adapter, then compare upstream vs adapted with the same seed cases.

The fork remains a candidate; it is not accepted yet.
