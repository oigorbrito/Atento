# Handoff — Atento product reset and remote reconciliation

Date: 2026-09-29

## Purpose

This handoff captures the restored product intent used for the repository-wide reconciliation.

> **Reconciliation completed in draft PR #19.** Repository-wide audit record: `docs/reconciliation-2026-09-29.md`.

It is intentionally self-contained. A future session should be able to resume from this file without relying on chat history.

## Canonical repository

```text
oigorbrito/Atento
```

Atento is the canonical repository for product decisions, evidence, evaluation infrastructure and implementation work.

## Canonical product model

Atento is an ecosystem with three distinct agents.

### 1. NAIA

**NAIA = Nova Assistente Inteligente Artificial.**

Role:

```text
persistent personal assistant / secretary
```

The historical NAIA implementation is an **idea/product reference**, not a mandatory codebase or architecture.

The strategic shift was:

```text
do not rebuild the persistent assistant from the historical NAIA by default

instead:
start from a mature working persistent-agent chassis
+ absorb NAIA differentiators
+ absorb useful features from other donors
```

OpenMausBot was the first known anchor candidate that motivated this strategy.

It is not selected.

The candidate universe must be re-enumerated. OpenClaw or any other project remains only if it can be justified under the same comparison protocol.

Target capability coverage includes the relevant functionality of references such as Grok Bot, Zapia and comparable mature persistent assistants, subject to practical cost constraints.

### 2. Anna

Role:

```text
emotional / therapeutic assistant
```

Anna is a separate agent, not a mode/persona of NAIA.

Her base is not selected.

Existing therapeutic research must be reclassified before selection:

```text
THERAPEUTIC_BASE_CANDIDATE
MECHANISM_DONOR
MODEL_OR_CHECKPOINT
BENCHMARK_OR_EVAL_SOURCE
UNCLASSIFIED_PENDING_AUDIT
```

Existing measurements for PsychAgent, TherapyMind, PsyChat, TheraMind and related benchmarks must be preserved.

No historical label such as `FULL_DONOR_CANDIDATE`, `adoption HOLD`, preferred/non-preferred or previous block assignment currently grants shortlist status.

### 3. Apollo

Role:

```text
nutrition / fitness / personal trainer assistant
```

Apollo is currently deferred.

Repository audit found no Apollo-specific candidate set or measurements documented before this reset.

State:

```text
APOLLO_STATUS = DEFERRED
APOLLO_SHORTLIST = NOT_SELECTED
APOLLO_RESEARCH = NOT_STARTED
```

## Canonical responsibility split

Use this split when resuming work:

```text
NAIA
= primary personal executive assistant / secretary
= general operational side-effect executor
= calendar + communications + research + shopping + browser/computer + apps + routines + automation

Anna
= emotional / therapeutic domain authority
= therapeutic conversation + longitudinal therapeutic memory + strategy/interventions + safety + multi-session follow-up
= delegates general operational tasks to NAIA through explicit minimal handoff

Apollo
= nutrition / fitness / personal-trainer domain authority
= goals + training + nutrition scope + progress/adherence + domain metrics/wearables + longitudinal plan adaptation
= delegates general operational tasks to NAIA through explicit minimal handoff
```

Important:

```text
NAIA_IS_PRIMARY_ASSISTANT
!=
NAIA_IS_SUPERUSER_OF_ANNA_OR_APOLLO

SHARED_INFRASTRUCTURE
!=
SHARED_PRIVATE_MEMORY

HANDOFF
!=
TRANSFER_OF_FULL_CONTEXT
```

Anna and Apollo own decisions inside their domains. NAIA owns general personal logistics and external operational execution unless a future domain-specific contract explicitly authorizes otherwise.

## Cross-agent boundaries

NAIA, Anna and Apollo are separate bounded agents.

Default invariants:

- no silent cross-agent chat access;
- no silent cross-agent memory access;
- no inherited tool authority across domains;
- no silent fallback from one agent into another role;
- handoffs, if later adopted, must be explicit, minimal and auditable;
- sensitive payloads cross boundaries only under an explicit contract and, where required, user consent.

Example:

```text
user is talking to Anna
→ asks for iPhone price
→ Anna does not become NAIA and does not perform shopping research
→ Anna remains inside the therapeutic/emotional domain
```

The exact runtime/deployment/handoff topology is not selected.

## Engineering selection principle

The project has no ideological preference for greenfield.

Use the "working car" rule:

```text
a working car with a broken shock absorber
may be cheaper to repair
than dismantling the whole car
to move everything onto a theoretically cleaner chassis
```

Therefore selection must compare **total adaptation cost**, not architecture aesthetics alone.

Measure:

- useful upstream capability preserved;
- real defects to repair;
- files/lines changed;
- depth of internal donor edits;
- boundaries that must be introduced;
- provider/executor/storage swap surface;
- safety/privacy/isolation adaptation;
- regressions caused by adaptation;
- upstream sync burden;
- estimated cost of reconstructing equivalent mature capability.

A localized defect does not automatically disqualify a mature base.

## Evidence policy

Preserve:

- pins and upstream SHAs;
- benchmark results;
- static and runtime observations;
- known gaps;
- failures and blockers;
- provenance;
- change-surface measurements;
- Project Points already earned.

Reset:

- shortlist authority;
- winner/finalist status;
- preferred/non-preferred labels as decisions;
- execution priority derived from the confused reconciliation;
- concrete topology treated as selected;
- fork/full-donor/native decision where not independently justified.

Reuse external evidence when it actually transfers.

Do not rerun broad upstream suites merely to obtain another pass number.

Local tests should focus on:

- Atento-specific deltas;
- pt-BR/domain transfer;
- cross-agent authority boundaries;
- actual integrations;
- material unproven gaps;
- regressions caused by adaptation.

## Current decision-state files

- `docs/product-concept-reset.md` — provisional authority for product identity during reconciliation.
- `docs/adr/ADR-002-assistant-base-selection.md` — NAIA base selection, reopened.
- `docs/adr/ADR-ANNA-001-therapeutic-base-selection.md` — Anna base selection, reset.
- `docs/adr/ADR-APOLLO-001-fitness-nutrition-base-selection.md` — Apollo deferred.
- `docs/adr/ADR-001-naya-product-composition.md` — historical composition ADR; isolation evidence preserved, concrete topology reopened.
- `docs/adr/ADR-000-fork-vs-greenfield.md` — historical adoption-strategy evidence; decision authority reset.
- `roadmap.md` — Project Points/evidence ledger; historical architecture is under reconciliation.

## Current high-level state

```text
REPOSITORY = ATENTO

NAIA_BASE = NOT_SELECTED
NAIA_SHORTLIST = NOT_SELECTED

ANNA_BASE = NOT_SELECTED
ANNA_SHORTLIST = NOT_SELECTED

APOLLO_STATUS = DEFERRED
APOLLO_BASE = NOT_SELECTED

CROSS_AGENT_DEFAULT = ISOLATED

PRESERVE_MEASUREMENTS = TRUE
PRESERVE_DECISIONS_FROM_CONFUSED_RECONCILIATION = FALSE
```

## Repository-wide reconciliation task — completed in draft

The draft reconciliation audited the entire remote and reconciled normative/current documents, configs, workflows and evaluation scope against this product model.

Rules:

1. do not rewrite dated research merely because it records historical observations;
2. add a historical/non-authoritative marker when a dated record can be mistaken for a current decision;
3. correct current/normative docs that still use Nayá/Naya as the current product name;
4. distinguish the historical `oigorbrito/NaIa` repository from **NAIA the current product agent**;
5. remove candidate-specific execution priority that survived the decision reset;
6. prevent evaluation registries from implying selection when they only register an executable candidate;
7. separate candidate classes for NAIA and Anna;
8. keep Apollo deferred;
9. keep Project Points/evidence already earned unless the underlying evidence itself is invalid;
10. do not select a winner during reconciliation.

## Immediate next step after reconciliation

After merge/acceptance of the reconciled state:

1. re-enumerate mature persistent-agent chassis for NAIA;
2. re-enumerate mature complete therapeutic-agent chassis for Anna;
3. classify every source into comparable categories;
4. reuse existing measurements;
5. perform only missing material audits/deltas;
6. then make evidence-based adoption decisions.

No winner is selected by this handoff.
