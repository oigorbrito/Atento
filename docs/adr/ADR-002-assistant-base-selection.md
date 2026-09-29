# ADR-002 — Seleção do sistema-base da Nayá Assistente

## Document contract

Esta ADR compara sistemas completos/persistentes candidatos a base da Assistente pessoal.

Frameworks de orquestração, durable runtimes e componentes isolados não entram como se fossem produtos equivalentes.

- **Status:** Proposed
- **Date:** 2026-09-29
- **Decision:** NOT_SELECTED

## Decision question

> Qual sistema funcionando chega à Assistente alvo com menor mudança estrutural, preservando a maior quantidade de capacidade já provada?

Não decidir por:

- quantidade de features isoladamente;
- estrelas;
- preferência arquitetural;
- estética do código.

Classificar gaps como:

```text
LOCALIZED_REPAIR
vs
CROSS_CUTTING_STRUCTURAL_REWRITE
```

E manter:

```text
PERSISTENCE != DURABLE_EXECUTION
FEATURE_RICH != GOOD_CHASSIS
```

## Candidates

### A — OpenMausBot

Source: `SRC-OPENMAUS`

Qualification snapshot:

`947bef311bf5c3f55d3590849abf0eb329408519`

Upstream had advanced to:

`7cd31c2a7f780757dd6933ec175d11e06103fd0f`

during the 2026-09-29 remote audit.

#### Expensive capability already present

Observed in the qualification snapshot:

- persistent bots and conversation/message state;
- routines/scheduling;
- persistent delegation state;
- desktop/Electron and mobile work;
- computer/browser capability;
- connected-app surface;
- model/provider driver registry;
- session model switching;
- memory/journal mechanisms;
- permission broker;
- deterministic eval/verification infrastructure.

Repository inventory at the inspected snapshot showed a large testing/verification surface. File-count signals are maturity evidence only and are not a quality score.

#### Updated security finding

An earlier shared-computer lending/argument-boundary concern was addressed upstream and follow-up PR #2023 had been incorporated when revalidated.

Do not repeat the historical HOLD for that exact issue without checking current source.

#### Material gaps

1. provider/delegation permissions observed as process-local in the inspected design;
2. no general proof found for arbitrary external-effect reconciliation after:
   ```text
   external effect applied
   → process crash
   → local commit missing
   → retry
   ```
3. interrupted active-turn recovery was not demonstrated at the same level later found in OpenClaw;
4. personal/shared memory concepts are not acceptable as therapeutic-memory authority.

#### Current disposition

```text
PRODUCT_MATURITY          = STRONG
PERSISTENT_ASSISTANT_FIT  = STRONG
GENERIC_EFFECT_DURABILITY = NOT_PROVEN
NAYA_AUTHORITY_MODEL      = NEEDS_REINFORCEMENT
STATUS                    = STRONG_BASE_CANDIDATE
```

No winner selected.

---

### B — NaIA

Source: `SRC-NAIA`

Qualified snapshot:

`23e4ca55abfaf399844047792018a22415ed3738`

#### Strong donor properties

Observed:

```text
intent
→ objective
→ plan
→ policy
→ approval
→ execution
→ evidence
→ persisted state/resume
```

Useful donor concepts include:

- fail-closed risk policy;
- explicit approval contracts;
- evidence/audit records;
- sensitive-memory consent;
- provider-neutral ports;
- operation/idempotency concepts;
- durability fault-research harness.

#### Product-base gap

The snapshot contains many useful modules, but the main product server composes only a subset of them.

Compared with product-rich candidates, more work remained to integrate:

- messaging;
- automations;
- personal memory;
- web execution;
- provider/model routing;
- mature end-user surfaces and auth boundary.

#### External-effect caveat

In the inspected messaging flow, the external provider send can occur before the local successful idempotency record is durably written.

Therefore local idempotency metadata does not establish exactly-once external effects.

#### Current disposition

```text
POLICY/AUTHORITY_MODEL    = STRONG
EVIDENCE_MODEL            = STRONG
PRODUCT_INTEGRATION       = LOWER_MATURITY
GENERIC_EFFECT_DURABILITY = NOT_PROVEN
STATUS                    = ARCHITECTURAL_DONOR / BASE_CANDIDATE_WITH_HIGHER_BUILD_COST
```

The upstream NaIA PR #186 contains a harness-repair experiment. It is not the canonical project evidence record; Atento remains canonical.

#### Historical NaIA durability-harness revalidation

A 2026-09-29 rerun of the NaIA chassis harness recorded:

- 392 tests executed;
- 348 passed;
- 44 failed.

The failures were classified as **HARNESS/fixture/provenance failures**, not evidence that Temporal, DBOS or Restate had failed the candidate protocol.

Concrete harness defects identified/repaired in donor PR #186:

- Temporal cleanup returned `liveObservedWorkerPids` from the wrong variable name;
- DBOS had the same cleanup mapping defect;
- the formal single-run fixture omitted A003/A004 already present in the frozen protocol.

Remaining red-state causes included missing adapter lockfile/provenance prerequisites and additional harness qualification issues.

Therefore:

```text
DURABLE_RUNTIME_WINNER = NOT_SELECTED
HARNESS_RED != CANDIDATE_FAIL
```

Atento should reuse those fault contracts as regression/qualification evidence, not restart broad durable-runtime testing unless a material candidate delta requires it.

---

### C — OpenClaw

Source: `SRC-OPENCLAW`

Qualification-start snapshot:

`df97da27f07f6655d5678bdbf1f6f9e460678013`

Upstream had advanced to:

`17cb0b6bf797d2d350f7268c00464b00aff7729a`

during the same-day audit.

Therefore the next qualification run must re-pin before relying on "latest" behavior.

#### Product surface

Observed:

- local Gateway/control plane;
- UI/CLI/TUI;
- many messaging channels;
- native/companion platform support;
- voice/device functions;
- tools/skills/plugins;
- local and hosted model providers;
- swappable model/agent harnesses.

#### Restart/recovery evidence

The inspected documentation/source showed persistent/recoverable state for:

- conversation history;
- accepted inputs;
- interrupted main-session turns;
- subagent state;
- queued outbound deliveries;
- scheduled jobs;
- restart continuation.

This is stronger interrupted-turn recovery evidence than was established for OpenMausBot.

#### Stale-authority evidence

Observed recovery contracts include checks around:

- requester session;
- run/turn identity;
- connection identity;
- parent/child lineage;
- generation;
- cancellation/replacement.

Later lineage is not automatically allowed to recreate missing historical authority.

#### Approval evidence

Observed exec approvals:

- persistent SQLite-backed state;
- layered tool policy + allowlist + approval;
- cancellation invalidates pending authority;
- late approval cannot restart cancelled work;
- standing/durable grant concepts.

#### Durable outbound evidence

Observed channel-message lifecycle includes concepts equivalent to:

```text
queued
platform-send-started
delivered
failed
unknown
```

with persisted queue/recovery, delivery intent and idempotency/receipt machinery.

This is strong evidence for message delivery.

It does **not yet prove** a generalized exactly-once contract for arbitrary SaaS/tool side effects.

#### Unresolved qualification questions

1. Do arbitrary tool writes receive a general operation/effect reconciliation protocol, or are strongest guarantees channel-specific?
2. How does default trust/exec policy compare with Nayá's intended least-privilege posture?
3. Can personal memory be scoped appropriately while Therapy remains completely outside its authority?
4. What code/change surface is required to impose Nayá-specific policy?
5. Which current security assumptions require modification?
6. Which local tests remain after using upstream evidence?

#### Current disposition

```text
PRODUCT_MATURITY               = STRONG
PERSISTENT_ASSISTANT_FIT       = STRONG
RESTART_RECOVERY               = STRONG_EVIDENCE
STALE_AUTHORITY_DEFENSE        = STRONG_EVIDENCE
OUTBOUND_DELIVERY_DURABILITY   = STRONG_EVIDENCE
GENERIC_TOOL_EFFECT_DURABILITY = NOT_YET_QUALIFIED
NAYA_POLICY_FIT                = NOT_YET_QUALIFIED
STATUS                         = STRONG_CANDIDATE / QUALIFICATION_IN_PROGRESS
```

---

## Current comparison

| Property | OpenMausBot | NaIA | OpenClaw |
|---|---|---|---|
| Complete assistant product | strong | partial | strong |
| Persistent state | strong | present, less integrated | strong |
| Interrupted-turn recovery | not proven at OpenClaw level | contracts/research, less product integration | strong evidence |
| Background/routines | strong | modules present | strong |
| Multi-provider | strong | strong contract | strong |
| Explicit policy/approval | needs reinforcement | strong | strong, different trust model |
| Stale execution defense | present | explicit research/contracts | strong evidence |
| Durable outbound messaging | partial evidence | ambiguity remains | strong evidence |
| Generic external-effect durability | not proven | not proven | not yet qualified |
| Final selection | no | no | no |

## Local-test rule

Do not run generic benchmarks already answered by upstream evidence.

Retain local tests only for material Atento/Nayá deltas:

- required authority policy;
- crash ambiguity for arbitrary external actions;
- sensitive-memory isolation;
- Assistant ↔ Therapist isolation;
- Portuguese/user-facing behavior when relevant;
- integration invasiveness.

## Decision

```yaml
decision: TBD
winner: NOT_SELECTED
openmausbot: strong-base-candidate
naia: architectural-donor-and-higher-build-cost-base-candidate
openclaw: qualification-in-progress
next_required_block: finish-openclaw-qualification
```

## Acceptance criteria

Before this ADR can be accepted:

- [ ] OpenClaw qualification completed at a newly pinned revision
- [ ] generic external-effect semantics compared across candidates
- [ ] policy/approval fit compared
- [ ] memory/privacy boundaries compared
- [ ] change surface / invasiveness measured
- [ ] current security assumptions reviewed
- [ ] license/provenance constraints confirmed
- [ ] same decision protocol applied to all finalists
