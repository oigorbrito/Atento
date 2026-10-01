# NAIA chassis-first selection policy — 2026-09-30

## Status

This document is the **operational screening method** for the NAIA base/chassis. It operates under `ADR-003 — Evidence-first engineering decision policy` and does not override its property-first requirement.

`ARCHITECTURE_FIRST` does **not** mean architectural aesthetics or a preferred framework. It means that the first elimination gate examines high-replacement-cost structural properties and whether the candidate can enforce the required Atento properties without a cross-cutting rewrite.

It does not select a candidate, create a final shortlist, or promote any runtime.

Current authority:

- NAIA_BASE = NOT_SELECTED
- NAIA_SHORTLIST = NOT_SELECTED

## 1. Core decision principle

### First selection parameter: lowest total maintenance cost

The first selection parameter is **the candidate chassis with the lowest defensible total cost of adaptation and ongoing maintenance for Atento's required properties**. The target is not a perfect chassis. No candidate is presumed to satisfy every requirement out of the box, and “most complete” or “most elegant” is not the objective.

Compare the work needed to adapt and keep each candidate operating: cross-cutting changes, integration and dependency burden, replacement boundaries, operational complexity, and expected maintenance. Use observed evidence where available; mark unmeasured cost as an estimate or unknown rather than treating it as fact. A small core or attractive architecture alone does not prove lower total cost.

This parameter governs the first candidate-selection gap. Structural properties matter because failures there can create expensive maintenance and reconstruction, not because architecture is an end in itself. Benchmarks and other evidence remain inputs where they measure relevant behavior or cost under a comparable workload; they do not substitute for the total maintenance-cost comparison or prove unmeasured properties.

The Atento candidate-selection problem is not equivalent to choosing the candidate with the highest feature count or the highest behavioral benchmark score.

The primary question is: **which existing system provides the required structural properties with the lowest expected cross-cutting reconstruction cost?**

The automotive analogy is useful as a cost-of-change model: chassis defects propagate across the system, while many peripheral components can be replaced through stable interfaces. The analogy is not a claim that architecture is intrinsically superior to measured behavior.

Therefore the screening order is:

1. Chassis / architecture
2. Authority / isolation
3. Persistent runtime
4. Empirical evidence
5. Capabilities / integrations
6. UI / peripheral details

This is a **replacement-cost and reversibility principle**, not an architectural-aesthetics preference.

## 2. What is expensive versus repairable

### High-cost / architectural properties

These receive priority because changing them later can require cross-cutting reconstruction:

- process/runtime topology;
- agent identity model;
- state ownership model;
- memory ownership and namespace model;
- tool authority model;
- credential authority model;
- scheduler/background authority model;
- inter-agent communication topology;
- approval/control-plane architecture;
- persistence/recovery architecture;
- sandbox/container boundary;
- provider/runtime abstraction;
- extension/plugin architecture;
- deployment topology;
- coupling between control plane and execution plane.

A candidate that requires replacing several of these should be treated as a high-build-cost donor, even if it has excellent individual features.

### Lower-cost / replaceable properties

These are normally considered after the chassis survives:

- individual channels;
- UI details;
- individual browser integration;
- individual connectors;
- model/provider substitutions where the provider abstraction is sound;
- individual skills/tools;
- peripheral integrations;
- formatting and presentation;
- non-structural convenience features.

These remain important, but they have a different replacement cost.

## 3. Architecture-first gate

Before expensive execution or broad benchmarking, each candidate receives a bounded architectural screen.

Minimum questions:

### A. Runtime topology

Can the system naturally represent NAIA, Anna and Apollo as separate authority domains rather than merely different prompts/personas?

### B. State ownership

Can each role own memory, conversation/session state, credentials, configuration, tool grants, scheduled jobs and external-action authority?

### C. Cross-role boundary

Can the architecture enforce:

- NAIA -> Anna memory = DENY
- Anna -> NAIA memory = DENY
- NAIA -> Anna credentials = DENY
- Anna -> NAIA credentials = DENY
- NAIA -> Anna tools = DENY
- Anna -> NAIA tools = DENY

while permitting an explicit brokered handoff?

### D. Background authority

Does scheduled/heartbeat/recovery execution inherit the same or narrower authority than interactive execution?

### E. Recovery

Can restart/recovery preserve state without silently recreating stale or broader authority?

### F. Extension boundary

Can capabilities be added or replaced without rewriting the core execution architecture?

### G. Deployment boundary

Can the security boundary be expressed by the runtime/deployment topology rather than only by application-level prompt or convention?

A candidate that cannot technically represent or enforce a required invariant should be eliminated before expensive runtime benchmarking. A candidate is not eliminated merely because its architecture differs from a preferred pattern.

## 4. Benchmark role

Benchmarks remain important, but their position changes.

Benchmark signal is not chassis quality, local proof, authority proof or isolation proof.

A benchmark can answer questions such as task completion, memory retrieval, computer-use performance, coding performance, latency, token efficiency, cost and reliability under a defined workload.

It cannot, by itself, establish NAIA/Anna isolation, credential boundaries, broker-only handoff, stale-authority rejection, deployment security, adaptation cost or structural suitability of the chassis.

Therefore benchmark results are used after architectural viability has been established, primarily to differentiate viable candidates and identify useful component donors. A benchmark result cannot rescue a hard failure of a required property.

## 5. Candidate screening sequence

The screening sequence is:

26 candidates
-> architectural / chassis screen
-> authority / isolation screen
-> persistent-runtime screen
-> external benchmark / test evidence
-> targeted Atento delta
-> deep empirical qualification

The purpose is to avoid spending a full empirical battery on a candidate whose fundamental architecture is already unsuitable.

## 6. Donor versus base

A candidate does not need to be a complete NAIA base to have useful evidence.

Separate three categories:

- BASE CANDIDATE: complete chassis capable of carrying NAIA.
- COMPONENT DONOR: mechanism worth incorporating into another chassis.
- REFERENCE: evidence, method or benchmark useful for comparison.

A component donor should not be rejected merely because it is not a complete product. Conversely, a component donor must not be scored as though it were a complete chassis.

## 7. Architecture-first scoring

When a numerical triage score is useful, it must be architecture-heavy.

| Dimension | Weight |
|---|---:|
| Chassis / architecture quality and suitability | 40% |
| Authority / isolation architecture | 25% |
| Persistent runtime / recovery | 15% |
| External empirical evidence | 10% |
| Adaptability / component replacement cost | 10% |

The score is a triage instrument, not a qualification score or final selection. It must not average away a hard failure of a required property. A candidate that cannot technically enforce required isolation/authority is not rescued by a higher benchmark or architecture score.

A missing benchmark does not automatically mean poor architecture.

A strong benchmark does not compensate for an architecturally unsuitable chassis.

## 8. Replacement-cost test

For every material candidate gap, classify the required change as:

- LOCALIZED_REPAIR
- COMPONENT_REPLACEMENT
- CROSS_CUTTING_STRUCTURAL_REWRITE

Localized repair includes changing a connector, channel, model provider, skill or UI.

Component replacement includes replacing a memory subsystem, browser adapter, credential adapter or model router when the chassis exposes a clean interface.

Cross-cutting structural rewrite includes replacing the agent identity model, converting global memory into isolated role memory, replacing direct peer authority with broker-only handoff, rebuilding scheduler authority, changing process topology for security boundaries, or separating a globally shared control plane that cannot enforce role isolation.

These are high-cost changes. A candidate requiring several such rewrites should be eliminated before deep testing unless there is unusually strong evidence that the rewrite is already supported by clean extension boundaries.

## 9. Evidence rule

For every candidate that survives the architectural screen:

1. Freeze the relevant upstream pin.
2. Inventory existing benchmarks, tests and evals.
3. Distinguish source evidence from executed evidence.
4. Identify which evidence transfers to the Atento topology.
5. Identify only the remaining material Atento delta.
6. Run the smallest targeted empirical test needed to resolve that delta.

Do not repeat upstream tests merely because they exist.

Do not run broad Atento tests when the candidate has already failed a higher-cost architectural gate.

Preserve the existing evidence distinctions:

- UPSTREAM_TEST != ATENTO_PROOF
- IMPLEMENTED != QUALIFIED
- AVAILABLE != QUALIFIED
- EXECUTED != VERIFIED
- VERIFIED != ACCEPTED
- BENCHMARK_GAIN != TRANSFERABLE_GAIN

## 10. Consequence for the 26-candidate universe

The 26 candidates should not receive identical test budgets.

Resource allocation should be:

- architectural evidence: broad / cheap;
- authority-isolation evidence: broad enough to eliminate structural mismatches;
- runtime and benchmark testing: narrow / expensive;
- full Atento qualification: very narrow / most expensive.

The intended result is not 26 full batteries.

The intended funnel is:

26 architectural screens
-> small structurally viable set
-> authority/isolation screening
-> small empirical set
-> deep qualification

## 11. Authority and non-redundancy

The documents have distinct roles:

- `ADR-003` is the **supreme engineering decision policy**: evidence quality, property-first requirements, transferability, and preference limits.
- `ADR-002` is the **NAIA base-selection decision record**: candidate universe, decision state, and selection question.
- This document is the **operational chassis-screen procedure**: replacement-cost classification, architectural gate, screening weights, and test-budget funnel.
- Historical comparison documents remain evidence only when explicitly marked historical/non-authoritative.

If these documents appear to conflict, `ADR-003` controls the evidence/property rule; `ADR-002` controls the NAIA decision state; this document controls only the screening procedure.

## 12. Current decision state

This policy changes the method, not the current decision.

- CANDIDATE_UNIVERSE_V1 = FROZEN
- SELECTION_METHOD = ARCHITECTURE_FIRST
- CHASSIS_GATE = PRIMARY
- AUTHORITY_ISOLATION_GATE = SECONDARY
- BENCHMARK_GATE = LATER
- DEEP_TEST_BUDGET = RESERVED_FOR_SURVIVORS
- NAIA_SHORTLIST = NOT_SELECTED
- NAIA_BASE = NOT_SELECTED

No candidate receives finalist status merely by scoring highly in this screen.

## 13. Relation to existing Atento methodology

This policy operationalizes the existing decision question:

> Qual sistema funcionando chega à Assistente alvo com menor mudança estrutural, preservando a maior quantidade de capacidade já provada?

It also formalizes the existing distinctions:

- LOCALIZED_REPAIR != CROSS_CUTTING_STRUCTURAL_REWRITE
- PERSISTENCE != DURABLE_EXECUTION
- FEATURE_RICH != GOOD_CHASSIS

The selection process should therefore minimize expected structural change while preserving demonstrated capability. A mature, structurally suitable chassis is preferred when it satisfies the required properties with defensible evidence; peripheral capabilities can then be added or replaced through bounded interfaces.

## Final rule

> **Primeiro filtre pelo que é caro de reconstruir: o chassi e as propriedades estruturais. Depois compare o que é mensurável e substituível: componentes, integrações e detalhes.**

This is the governing screening principle for the next NAIA candidate reduction.