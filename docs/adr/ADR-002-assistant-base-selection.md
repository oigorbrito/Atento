# ADR-002 — Seleção do sistema-base da NAIA

> **DECISION RESET — 2026-09-29:** preservar todos os pins, achados estáticos, testes upstream, gaps e medições abaixo. Não preservar como decisão a shortlist, a ordem de execução, a prioridade de OpenClaw ou qualquer caracterização de candidato como finalista até a categoria de agentes persistentes ser reenumerada.

## Document contract

Esta ADR compara sistemas completos/persistentes candidatos a base da Assistente pessoal.

Frameworks de orquestração, durable runtimes e componentes isolados não entram como se fossem produtos equivalentes.

- **Status:** Reopened — `DECISION_RESET`
- **Date:** 2026-09-29
- **Decision:** NOT_SELECTED / shortlist reset

## Current candidate-universe evidence

Post-reset re-enumeration is recorded in:

`docs/evaluation/candidate-reenumeration-2026-09-29.md`

This record expands/classifies the candidate universe but does not alter this ADR's `NOT_SELECTED` state or create a shortlist.



Current same-protocol completeness evidence:

`docs/evaluation/naia-candidate-completeness-audit-2026-09-29.md`

This audit establishes comparability/missing evidence only. It does not create a shortlist or alter `NOT_SELECTED`.

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

## Historical candidates — evidence preserved, shortlist reset

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

#### Historical audit characterization — non-decisional

```text
PRODUCT_MATURITY          = STRONG
PERSISTENT_ASSISTANT_FIT  = STRONG
GENERIC_EFFECT_DURABILITY = NOT_PROVEN
NAIA_AUTHORITY_MODEL      = NEEDS_REINFORCEMENT
HISTORICAL_AUDIT_CLASSIFICATION = STRONG_BASE_CANDIDATE
```

No winner selected.

---

### B — historical NaIa implementation/donor

Source: `SRC-NAIA`

> This section refers to the historical `oigorbrito/NaIa` repository, not to the current NAIA product identity.

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

#### Historical audit characterization — non-decisional

```text
POLICY/AUTHORITY_MODEL    = STRONG
EVIDENCE_MODEL            = STRONG
PRODUCT_INTEGRATION       = LOWER_MATURITY
GENERIC_EFFECT_DURABILITY = NOT_PROVEN
HISTORICAL_AUDIT_CLASSIFICATION = ARCHITECTURAL_DONOR / BASE_CANDIDATE_WITH_HIGHER_BUILD_COST
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

Qualification repin on 2026-09-29:

`e9571d77e76bd6d35996273d9e8398ad539b26e1`

The repin was 8 commits ahead of the previously observed `17cb0b6bf797d2d350f7268c00464b00aff7729a`.

Detailed evidence record:

`docs/evaluation/openclaw-qualification-2026-09-29.md`

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

#### Policy/approval result

OpenClaw exposes:

- persistent SQLite-backed approval state;
- `deny`, `allowlist`, `ask`, `auto` and `full` exec modes;
- layered host/config policy;
- executable binding and revalidation;
- plugin tool-policy/approval hooks;
- cancellation and stale-authority defenses.

These primitives are strong, but the documented general-purpose defaults are not the NAIA target.

NAIA requires an explicit fail-closed hardening profile rather than inheriting permissive/trusted-operator assumptions.

#### Durable outbound vs generic tool effects

Channel-message delivery has strong durable semantics:

```text
queued
platform-send-started
delivered
failed
unknown
```

with persisted intent, queue recovery, receipts and optional provider reconciliation for ambiguous sends.

However OpenClaw explicitly does not claim exactly-once external tool/provider effects generally.

Therefore:

```text
OUTBOUND_DELIVERY_DURABILITY   = STRONG_EVIDENCE
GENERIC_TOOL_EFFECT_DURABILITY = NOT_PROVEN
```

A universal generic effect protocol would be cross-cutting; controlled high-risk adapters can instead implement localized idempotency/readback/reconciliation contracts.

#### Memory and Therapist boundary

OpenClaw supports per-agent:

- workspace;
- `agentDir`;
- SQLite session store;
- auth/config state;
- same-agent built-in memory search.

But:

- plugin storage can require explicit per-agent scoping;
- cross-agent session access is not narrow by default;
- workspace alone is not a hard sandbox;
- one Gateway is documented as trusted-operator infrastructure rather than a hostile multi-tenant boundary.

Therefore ADR-001's strict Assistant ↔ Therapist authority boundary should use separate Gateway/runtime boundaries (or an equivalent independent service boundary), connected only through the explicit handoff broker.

#### Change surface / invasiveness

```text
PRODUCT_ADAPTATION                = LOW_TO_MODERATE
NAIA_SECURITY_HARDENING           = MODERATE
STRICT_THERAPY_BOUNDARY           = DEPLOYMENT_TOPOLOGY_CHANGE
UNIVERSAL_GENERIC_EFFECT_PROTOCOL = CROSS_CUTTING_IF_REQUIRED
CRITICAL_TOOL_EFFECT_PROTOCOL     = LOCALIZED_IF_ADAPTER_CONTROLLED
```

The candidate exposes enough config/plugin seams that the ordinary NAIA product and policy adaptation does not currently imply a deep fork.

#### Historical proposed OpenClaw follow-up — inactive pending re-enumeration

Do not repeat upstream persistence/restart/channel/approval-lifecycle tests when the NAIA adaptation does not replace those mechanisms.

Run one OpenClaw-specific pre-selection probe:

- `OC-NAYA-001` — implement the minimal NAIA hardening profile using supported config/plugin seams, validate the effective policy, and record Git/change-surface including whether any OpenClaw core patch is required.

The earlier candidate-local probes are preserved/reclassified as historical evidence. `OC-NAYA-*` identifiers remain unchanged for traceability but are not current product naming:

- former `OC-NAYA-002` (arbitrary external-effect crash ambiguity) → **Block J / external-action adapter contract**. OpenClaw already states that generic exactly-once external effects are not guaranteed; retesting an unmodified generic tool path would only reconfirm a known absence. Test the real Atento-controlled high-risk adapter when it exists.
- former `OC-NAYA-003` (Assistant ↔ Therapist isolation) → **ADR-001 composition/deployment test**. The selected architecture requires separate runtime/Gateway authority boundaries, so the useful test is the brokered composition, not two personas in one OpenClaw Gateway.
- former `OC-NAYA-004` (plugin/global-store isolation) → **per-plugin/per-memory integration test** when a concrete shared-store plugin is selected.
- former `OC-NAYA-005` (touchpoint count) → folded into `OC-NAYA-001`; change-surface is a measurement of the implemented adapter/profile, not an independent runtime test.

#### Historical audit characterization — non-decisional

```text
PRODUCT_MATURITY                = STRONG
PERSISTENT_ASSISTANT_FIT        = STRONG
RESTART_RECOVERY                = STRONG_EVIDENCE
STALE_AUTHORITY_DEFENSE         = STRONG_EVIDENCE
OUTBOUND_DELIVERY_DURABILITY    = STRONG_EVIDENCE
POLICY_PRIMITIVES               = STRONG
NAIA_POLICY_DEFAULT_FIT         = NEEDS_HARDENING
PER_AGENT_CORE_STATE_ISOLATION  = STRONG
STRICT_THERAPY_BOUNDARY         = SEPARATE_RUNTIME_REQUIRED
GENERIC_TOOL_EFFECT_DURABILITY  = NOT_PROVEN
LICENSE                         = MIT
HISTORICAL_AUDIT_CLASSIFICATION = STRONG_CANDIDATE / STATIC_QUALIFICATION_COMPLETE
LOCAL_DELTA_TESTS               = PENDING
```

No winner selected.

---

## Historical comparison — evidence only

| Property | OpenMausBot | NaIA | OpenClaw |
|---|---|---|---|
| Complete assistant product | strong | partial | strong |
| Persistent state | strong | present, less integrated | strong |
| Interrupted-turn recovery | not proven at OpenClaw level | contracts/research, less product integration | strong evidence |
| Background/routines | strong | modules present | strong |
| Multi-provider | strong | strong contract | strong |
| Explicit policy/approval | needs reinforcement | strong | strong primitives; NAIA hardening required |
| Stale execution defense | present | explicit research/contracts | strong evidence |
| Durable outbound messaging | partial evidence | ambiguity remains | strong evidence |
| Generic external-effect durability | not proven | not proven | not proven; explicitly not a general exactly-once claim |
| Memory / bounded-context isolation | needs reinforcement | strong authority concepts, lower product integration | strong per-agent core state; strict Therapy boundary needs separate runtime |
| Adaptation surface | product-rich; authority reinforcement required | higher product integration/build cost | low/moderate product adaptation; moderate hardening; generic effect protocol structural if universal |
| Final selection | no | no | no |

## Evidence-reuse and local-test rule

Do not trust documentation claims blindly, and do not rerun upstream suites mechanically.

For each material property:

1. audit implementation + directly relevant upstream tests at the pinned SHA;
2. verify CI/run evidence when available; absence of observable CI is recorded as a limitation, not converted into pass/fail;
3. decide whether the upstream evidence transfers unchanged to the Atento deployment;
4. create a local test only when the Atento adapter/configuration/topology materially changes the property or the property remains unproven.

Behavioral benchmarks are used only for behavioral questions. Authority, durability, isolation and adaptation cost are primarily contract/fault/runtime/Git questions.

The previous reconciliation treated `OC-NAYA-001` as the only remaining OpenClaw pre-selection delta. That execution priority is now **inactive**. The underlying evidence and probe design remain reusable if OpenClaw re-enters the comparable shortlist.

## Decision reset

```yaml
decision: NOT_SELECTED
status: DECISION_RESET
shortlist: NOT_SELECTED
openmausbot: EVIDENCE_PRESERVED
naia_historical_implementation: IDEA_AND_DONOR_EVIDENCE_PRESERVED
openclaw: EVIDENCE_PRESERVED
next_required_block: REENUMERATE_COMPARABLE_PERSISTENT_ASSISTANT_CHASSIS
```

No candidate receives finalist status from this document until the comparable set is rebuilt.

## Historical acceptance criteria — inactive

These criteria are preserved as a record of the previous decision process. They do not define the next execution order until the candidate set is rebuilt:

- [x] OpenClaw static qualification completed at a newly pinned revision
- [x] generic external-effect semantics characterized for OpenClaw and compared with existing finalist evidence
- [x] policy/approval fit analyzed
- [x] memory/privacy boundaries analyzed
- [x] current security assumptions reviewed
- [x] license/provenance constraints confirmed
- [ ] OC-NAYA-001 minimal hardening/profile probe executed against the pinned candidate
- [ ] empirical change surface / invasiveness recorded as part of OC-NAYA-001
- [x] non-selection tests reclassified to their owning blocks instead of duplicated during base selection
- [ ] same decision protocol applied to all finalists after the material local delta
- [ ] final base decision recorded
