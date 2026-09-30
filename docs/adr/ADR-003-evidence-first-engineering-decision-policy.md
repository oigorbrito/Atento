# ADR-003 — Evidence-first engineering decision policy

- **Status:** Accepted
- **Date:** 2026-09-30
- **Scope:** Engineering research, architecture selection, qualification, and promotion decisions in Atento

## Context

Atento evaluates persistent-assistant systems, authority models, runtime topologies, adapters, providers, and supporting infrastructure under uncertainty.

The project must not promote a design because it is preferred by the user, by the evaluator, or because it appears architecturally elegant.

The controlling principle is:

> When reliable technical evidence contradicts a preference, the preference does not control the engineering decision.

This does not mean that software engineering always has one scientifically unique answer. Many decisions are underdetermined and require tradeoffs. In those cases, preferences may choose among options that remain compatible with the evidence. They may not override demonstrated safety, correctness, reliability, isolation, durability, or cost properties.

## Decision

Atento adopts an evidence-first decision policy.

```text
USER_PREFERENCE != TECHNICAL_EVIDENCE
EVALUATOR_PREFERENCE != TECHNICAL_EVIDENCE
ARCHITECTURAL_ELEGANCE != PROPERTY_PROOF
POPULAR_PRACTICE != LOCAL_PROOF
DOCUMENTATION_CLAIM != EXECUTED_EVIDENCE
BENCHMARK_SIGNAL != LOCAL_PROOF
```

When sources conflict, prefer evidence that is more direct, current, reproducible, property-specific, and representative of the actual Atento composition.

A practical hierarchy is:

```text
REPRODUCIBLE_DIRECT_EVIDENCE
  > CURRENT_PIN_EXECUTED_EVIDENCE
  > CURRENT_PIN_IMPLEMENTATION + RELEVANT_TEST CONTRACT
  > TRANSFERABLE_UPSTREAM EVIDENCE WITH EXPLICIT CONSTRAINTS
  > HISTORICAL EXECUTION SIGNAL
  > DOCUMENTATION CLAIM
  > REPUTATION / POPULARITY / AESTHETIC PREFERENCE
```

This hierarchy is not mechanical. Evidence quality, scope, population, environment, threat model, and transferability must be checked before one source is treated as stronger than another.

## Property-first requirement

Atento selects required properties, not preferred implementations.

For example, the NAIA authority model requires properties such as:

```text
DENIED_ACTION = DENIED_TECHNICALLY
ALLOWED_ACTION = BOUND_TO_EXPECTED_AUTHORITY
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
DELEGATION_AUTHORITY <= CALLER_AUTHORITY
CREDENTIAL_BOUNDARY = TECHNICALLY_ENFORCED
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
NAIA_ANNA_AUTHORITY = ISOLATED
CONSEQUENTIAL_EFFECT_AUTHORITY = ENFORCEABLE
```

These properties do **not** imply that one specific mechanism is mandatory.

Therefore Atento must not assume in advance that the correct implementation is necessarily:

- an external policy service;
- a capability-token system;
- a particular approval broker;
- a specific sandbox model;
- a particular process topology;
- a specific framework or runtime.

If a different architecture demonstrates the required properties with stronger evidence and lower total adaptation/maintenance cost, that architecture remains valid.

## Preference rule

Preferences are admissible only after evidence constraints are satisfied.

Valid use of preference:

```text
Option A and Option B both satisfy the required properties with comparable evidence.
A has a simpler UI preferred by the product owner.
=> preference may decide.
```

Invalid use of preference:

```text
Option A is preferred aesthetically.
Option B has stronger demonstrated isolation and A fails the required isolation property.
=> preference cannot promote A.
```

Likewise:

```text
USER_DESIRE cannot convert FAIL into PASS
USER_DESIRE cannot convert UNPROVEN into VERIFIED
EVALUATOR_DESIRE cannot convert STATIC_SOURCE into RUNTIME_PASS
ARCHITECTURAL_PREFERENCE cannot convert AVAILABLE into QUALIFIED
```

## Evidence handling rules

The following project separations remain mandatory:

```text
BENCHMARK_SIGNAL != LOCAL_PROOF
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED

HISTORICAL_EVIDENCE != CURRENT_PIN_PROOF
STATIC_SOURCE != RUNTIME_PASS
SMALL_CORE != LOW_TOTAL_MIGRATION_COST
```

Additional rules:

1. Prefer the smallest decisive test over broad retesting.
2. Reuse sufficient evidence when the relevant boundary has not changed.
3. Do not extrapolate a result from one candidate, adapter, provider, profile, topology, or pin to another.
4. Treat contradictory evidence explicitly; do not average it away.
5. Preserve negative evidence and known absences.
6. Record uncertainty as uncertainty rather than forcing a verdict.
7. Keep legal/adoption constraints separate from technical quality.
8. Measure total adaptation and maintenance cost rather than inferring it from code size or architectural neatness.
9. For authority, isolation, durability, and external effects, prefer technical enforcement and fault/runtime evidence over prompt instructions or UI claims.
10. When no decisive evidence distinguishes two acceptable options, document the tie and allow product preference to operate within that evidence-compatible set.

## Relation to candidate selection

This ADR does not select or rank a NAIA base.

It constrains how future selection must be performed.

The selection question remains evidence-driven:

> Which working system reaches the target assistant with the least structural change while preserving the greatest amount of capability already demonstrated?

A candidate must not be promoted because:

- it matches a preferred architecture;
- it is more popular;
- its repository looks cleaner;
- its design resembles an earlier Atento concept;
- the user or evaluator wants it to win.

A candidate may be promoted only through the project's explicit evidence gates.

## Relation to NAIA / Anna isolation

The fixed product requirement remains:

```text
chat access = isolated
memory authority = isolated
tool authority = isolated
silent role drift = forbidden
```

The implementation mechanism is not predetermined.

A workspace, project, profile, process, container, OS user, service boundary, capability layer, or other mechanism is acceptable only to the extent that the required isolation properties are actually demonstrated.

```text
NAMED_ISOLATION_BOUNDARY != PROVEN_AUTHORITY_ISOLATION
```

## Consequences

Positive consequences:

- candidate selection is less vulnerable to confirmation bias;
- architecture can evolve when better evidence appears;
- tests focus on decision-relevant properties;
- negative results remain useful rather than being worked around;
- user preferences remain meaningful without overriding correctness or safety evidence.

Costs:

- some preferred designs may be rejected;
- some decisions remain unresolved longer because evidence is insufficient;
- exact pins, profiles, topologies, and adapters may need to be frozen before testing;
- evidence provenance and transferability must be maintained carefully.

These costs are accepted.

## Current decision state

This methodological decision does not change any candidate state:

```text
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
ANNA_SHORTLIST = NOT_SELECTED
ANNA_BASE = NOT_SELECTED
APOLLO_STATUS = DEFERRED
CROSS_AGENT_TOPOLOGY = NOT_SELECTED
```

It also does not alter the current Engram residual state or promote Engram:

```text
ENGRAM_HARDENED_COMPOSITION = FROZEN_V1
ENGRAM_BROWSER_EFFECT_AUTHORITY = UNPROVEN
RESIDUAL_BROWSER_AUTHORITY_PROBE = READY_NOT_EXECUTED
```

## Canonical shorthand

```text
EVIDENCE > PREFERENCE
PROPERTY_PROOF > ARCHITECTURAL AESTHETICS
DIRECT_CURRENT_PROOF > INDIRECT_HISTORICAL SIGNAL
OBSERVED_TOTAL_COST > ASSUMED SIMPLICITY
UNCERTAINTY = PRESERVED
NO_PROMOTION_WITHOUT_EVIDENCE
```
