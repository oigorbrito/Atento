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

Current persistent-agent discovery expansion:

`docs/evaluation/naia-persistent-agent-discovery-2026-09-29.md`

Current external/upstream evidence preflight:

Expanded upstream-evidence matrix:

Transfer audit for Suna / Letta Code / PersonalJarvis:

Transfer audit for Rakazo / Gobii:

`docs/evaluation/naia-transfer-audit-rakazo-gobii-2026-09-29.md`


`docs/evaluation/naia-transfer-audit-suna-letta-jarvis-2026-09-29.md`


`docs/evaluation/naia-expanded-upstream-evidence-matrix-2026-09-29.md`


`docs/evaluation/naia-external-evidence-preflight-2026-09-29.md`

The registered discovery pools have now been bounded and frozen as the V1 decision snapshot. The secondary admission and transfer records are:

- `docs/evaluation/naia-secondary-pool-admission-screen-2026-09-30.md`
- `docs/evaluation/naia-transfer-audit-automate-agentos-openagentd-2026-09-30.md`
- `docs/evaluation/naia-transfer-audit-hubos-rustfox-2026-09-30.md`
- `docs/evaluation/naia-transfer-audit-engram-holt-2026-09-30.md`

First bounded residual execution evidence:

`docs/evaluation/naia-engram-browser-authority-probe-2026-09-30.md`

The full residual-only execution map is:

`docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md`

Grok Bot and Meta Muse remain reference products rather than comparable base candidates. Open Intern remains deferred at its exact screened pin because required NAIA product surfaces were explicitly not shipped there.

For technical discovery, license remains separate from technical evidence and no candidate receives qualification, shortlist or selection from static/transfer evidence alone.

```text
FROZEN_CANDIDATE_UNIVERSE_V1 = COMPLETE
EXPANDED_EXTERNAL_EVIDENCE_GATE = COMPLETE_V1
RESIDUAL_ONLY_PROBE_LEDGER = COMPLETE_V1
LOCAL_RESIDUAL_PROBE_EXECUTION = STARTED_BOUNDED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```


`docs/evaluation/naia-candidate-completeness-audit-2026-09-29.md`

This audit establishes comparability/missing evidence only. It does not create a shortlist or alter `NOT_SELECTED`.

## Chassis-first selection policy

The selection screen is now explicitly architecture-first. The canonical method is:

`docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md`

The governing principle is replacement cost: first evaluate the expensive-to-replace chassis/architecture, then authority/isolation, then persistent runtime, and only afterward spend expensive benchmark/runtime effort on capabilities and integrations.

The candidate universe must therefore not receive identical empirical budgets. Candidates that require cross-cutting structural rewrites are screened out before deep testing unless there is strong evidence that the required change is already supported by clean extension boundaries.

This is a method change, not a selection decision:

- `SELECTION_METHOD = ARCHITECTURE_FIRST`
- `CHASSIS_GATE = PRIMARY`
- `AUTHORITY_ISOLATION_GATE = SECONDARY`
- `BENCHMARK_GATE = LATER`
- `NAIA_SHORTLIST = NOT_SELECTED`
- `NAIA_BASE = NOT_SELECTED`

## Decision-method policy

Candidate comparison and promotion are governed by:

`docs/adr/ADR-003-evidence-first-engineering-decision-policy.md`

In particular, user/evaluator preference and architectural aesthetics cannot override stronger property-specific evidence. Preferences may operate only among evidence-compatible options.

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

## Current QwenPaw contract evidence

`docs/evaluation/qwenpaw-contract-audit-2026-09-29.md`

QwenPaw is a comparable persistent-assistant product with strong memory/governance/computer-use primitives. The current pin still requires an Atento hardening probe because sandbox fallback and scheduled-task defaults can broaden authority relative to NAIA's fail-closed contract. This does not create shortlist status.

## Current AI Butler contract evidence

`docs/evaluation/aibutler-contract-audit-2026-09-29.md`

AI Butler is a comparable persistent-assistant product with strong static evidence for memory isolation, fail-closed shell authority, credential gating, scheduler persistence and long-horizon mission state. Current qualification remains pending because channel/provider maturity is mixed and Windows computer-use still lacks real interactive validation. This does not create shortlist status.

## Current NanoClaw adaptation evidence

`docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md`

NanoClaw is a comparable persistent-assistant product with explicit container/credential boundaries and an unusually explicit skill/update model. The current audit shows that total fork cost is capability-profile dependent: channel/gateway surfaces can be modest, while provider integrations such as OpenCode are multi-point. The pinned Ollama skill also requires rederivation against the current provider-contribution architecture. This does not create shortlist status.

## Current TrustClaw contract evidence

`docs/evaluation/trustclaw-contract-audit-2026-09-29.md`

TrustClaw is a comparable persistent-assistant product with strong local instance-memory and cron contracts. Its broad external-action and remote-sandbox authority is materially delegated to Composio, while the standard deployment/model path is Vercel-oriented. Qualification therefore requires a composed dependency/cost/authority probe. This does not create shortlist status.

## Current Open Assistant contract evidence

docs/evaluation/open-assistant-contract-audit-2026-09-29.md

Open Assistant is a comparable persistent-assistant product with real conversation memory, persisted cron scheduling, skill/tool filtering, browser automation, encrypted credential storage and multi-provider support. The exact-pin audit also finds material NAIA hardening gaps: no independent per-action approval/deny boundary, plan-driven expansion to all enabled skills, global-by-service credential scope, no established strict NAIA/Anna isolation and no desktop computer-use surface. Exact-pin hosted execution was not observed.

License is out of scope for the current technical selection protocol.

~~~text
OPEN_ASSISTANT_STATIC_RESULT = PASS_WITH_SCOPE
OPEN_ASSISTANT_CURRENT_PIN_QUALIFIED = NO
LICENSE = OUT_OF_SCOPE_FOR_TECHNICAL_SELECTION
~~~

This does not create shortlist status.

## Current common empirical profile

docs/evaluation/naia-common-probe-profile-2026-09-29.md

The common NCP profile is retained as a template, but broad discovery and upstream-evidence reconciliation are complete for the frozen V1 snapshot. `docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md` now maps each candidate to only the unresolved microprobe families that could change decision evidence. Only a named `ATENTO_DELTA` or blocking `UNPROVEN` invariant may trigger local execution. This ADR remains NOT_SELECTED.

## Historical candidates — evidence preserved, shortlist reset

### A — OpenMausBot

Source: `SRC-OPENMAUS`

Qualification snapshot:

`947bef311bf5c3f55d3590849abf0eb329408519`

Upstream had advanced to:

`7cd31c2a7f780757dd6933ec175d11e06103fd0f`

during the 2026-09-29 remote audit.


Current-pin delta audit:

`docs/evaluation/openmaus-current-delta-audit-2026-09-29.md`

At current observed head `6005b1bf5883a7ffa639c07e729321f89b9532e1`, the four-commit delta from the last Atento-reviewed comparison pin has been audited statically. Lending-memory and request-auth boundaries are stronger in source, but exact-current-pin runtime execution is still pending. This does not grant shortlist status.

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


Current-pin delta audit:

`docs/evaluation/openclaw-current-delta-audit-2026-09-29.md`

At current observed head `ca8f24d05fc49a224adab0c9426077fd8d93801d`, the 67-commit delta from the qualified pin has been audited statically. Approval/restart/channel-durability evidence remains transferable with scope; memory sanitization, browser ownership and channel/gateway boundaries are stronger in source. Exact-current-pin hosted execution is not observed. This does not grant shortlist status.

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


## Architecture Gate 1 closure — 2026-09-30

Canonical result:

`docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`

The frozen V1 universe has now received the architecture-first screen required by the current selection policy.

```text
ARCHITECTURE_GATE_1 = COMPLETE_V1
ARCHITECTURE_SCREENED = 26_OF_26
ARCHITECTURE_SURVIVORS = 25
COMPLETE_BASE_STOPS = [SelfAgent]

AUTHORITY_ISOLATION_GATE = NEXT
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

SelfAgent is stopped only as a **complete NAIA base candidate at its frozen pin** because existing exact-pin evidence requires cross-cutting repairs across central action authority, background execution and scheduler lifecycle before the required contract can be represented. It remains usable as reference/donor evidence and may be reconsidered after a material upstream change.

Survival of Gate 1 is not qualification. The remaining 25 candidates proceed only to candidate-specific authority/isolation composition under the residual-only protocol.


## Authority/isolation Gate 2 screen — 2026-09-30

Canonical result:

`docs/evaluation/naia-authority-isolation-gate2-screen-2026-09-30.md`

All 25 Gate-1 survivors have now received the authority/isolation static screen.

```text
AUTHORITY_ISOLATION_STATIC_SCREEN = COMPLETE_V1
AUTHORITY_ISOLATION_SCREENED = 25_OF_25
VENDOR_DEFAULT_AUTHORITY_PASS = 0
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
ADDITIONAL_GATE_2_STRUCTURAL_STOPS = 0

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This closes the question of whether any current vendor/default profile can proceed directly: none can. It does not mean all 25 fail. Each still has at least one bounded hardened-composition/dependency path that must be frozen before a candidate-specific proof can close Gate 2.

Broad vendor-default retesting and a generic 25-candidate runtime battery are therefore not justified.


## First Gate-2 candidate preflight — OpenClaw

Canonical record:

`docs/evaluation/openclaw-gate2-hardening-preflight-2026-09-30.md`

Result:

```text
OPENCLAW_PROFILE_EXPRESSIBILITY = PASS_STATIC_WITH_SCOPE
CORE_PATCH_REQUIRED_TO_EXPRESS_POLICY = NO
EXACT_PIN_CI = PASS
ATENTO_TWO_ROLE_RUNTIME_COMPOSITION = NOT_RUN
OPENCLAW_GATE2 = NOT_CLOSED
```

The next OpenClaw evidence, if executed, is the two-role negative authority/isolation composition test; broad upstream retesting remains unnecessary.


## Technical-funnel update — 2026-09-30

Open Assistant at `32c55d2643f9fe38777f9212588b2eee45392514` is restored to the technical selection funnel. License is not used as an elimination or ranking criterion in the current protocol.

Canonical status record:

`docs/evaluation/open-assistant-adoption-elimination-2026-09-30.md`

Current funnel state:

```text
FROZEN_UNIVERSE = 26
SELFAGENT = ELIMINATED_ARCHITECTURE
OPEN_ASSISTANT = ACTIVE_TECHNICAL_SURVIVOR
CURRENT_TECHNICAL_SURVIVORS = 25
LICENSE = OUT_OF_SCOPE_FOR_TECHNICAL_SELECTION
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

HubOS has also completed the next Gate-2 structural authority preflight. Its fail-open/sessionless guard gaps are real, but the exact pin exposes a single central `ToolGuardMixin._acting` enforcement path; therefore a cross-cutting rewrite is not yet established and HubOS is not eliminated at this stage.

Canonical record:

`docs/evaluation/hubos-gate2-authority-preflight-2026-09-30.md`


## Gate-2 high-hardening structural preflight — 2026-09-30

Canonical result:

`docs/evaluation/naia-gate2-high-hardening-structural-preflight-2026-09-30.md`

The five candidates previously marked as the highest structural-hardening risk have now been source-preflighted:

```text
Open Assistant = BOUNDED_HARDENING_PATH
OpenGrokBot    = BOUNDED_HARDENING_PATH
OpenAgentd     = BOUNDED_HARDENING_PATH
HubOS          = BOUNDED_HARDENING_PATH
RustFox        = BOUNDED_HARDENING_PATH

NEW_STRUCTURAL_ELIMINATIONS = 0
```

No candidate is promoted by this result. It only establishes that the current evidence does not justify structural elimination before a hardened composition test.

Current technical funnel:

```text
FROZEN_UNIVERSE = 26
TECHNICAL_ELIMINATED = [SelfAgent]
TECHNICAL_SURVIVORS = 25
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```


## Gate-2 empirical execution frontier — 2026-09-30

Canonical record:

`docs/evaluation/naia-gate2-empirical-execution-frontier-2026-09-30.md`

Evidence reuse has reduced AI Butler to one Atento-specific Gate-2 residual:

```text
NEXT_EMPIRICAL_COMPOSITION_TARGET = AI_BUTLER
AI_BUTLER_GATE2 = ONE_RESIDUAL_COMPOSITION_TEST_REMAINING
```

This execution ordering is not a shortlist, winner, or base selection. It is justified only by exact-pin executed authority evidence plus the smallest remaining composition delta.

Current environment limitation:

```text
LOCAL_CLONE_NETWORK = BLOCKED_DNS
AI_BUTLER_COMPOSITION_EXECUTION = READY_BUT_NOT_RUN
```

Do not convert the executor/network limitation into candidate evidence.


## Gate-2 transferable-evidence frontier — 2026-09-30

Canonical record:

`docs/evaluation/naia-gate2-transferable-evidence-frontier-2026-09-30.md`

```text
TRANSFERABLE_EVIDENCE_FRONTIER = COMPLETE_V1
FRONTIER = [AI Butler, AgentOS]

NEXT_EMPIRICAL_COMPOSITION_TARGET = AI Butler
SECOND_READY_COMPOSITION_TARGET = AgentOS

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This frontier is not a shortlist or ranking. It only records that these two candidates currently have enough exact-pin executed Gate-2 evidence to avoid broad retesting and proceed directly to Atento-specific hardened composition.


## Gate-2 transferable-evidence frontier V2 — 2026-09-30

Exact-pin executed evidence now supports a five-candidate composition frontier:

```text
FRONTIER_V2 = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram
]

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This is not a shortlist. It only identifies candidates for which broad upstream retesting is now redundant and only Atento-specific composition residuals remain decision-relevant.


## Gate-2 hosted-execution reconciliation / frontier V3 — 2026-09-30

Canonical reconciliation:

`docs/evaluation/naia-gate2-exact-pin-hosted-execution-reconciliation-2026-09-30.md`

Current transferable-evidence frontier:

```text
FRONTIER_V3 = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox
]

FRONTIER_COUNT = 8
NEW_TECHNICAL_ELIMINATIONS = 0
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Holt and HubOS have exact-pin green automation but not relevant authority test execution. Rakazo, Gobii, PersonalJarvis and OpenGrokBot have exact-pin failed CI, but failure attribution is required before any technical elimination.


## Gate-2 CI-failure attribution / frontier V4 — 2026-09-30

Canonical gate:

`docs/evaluation/naia-gate2-ci-failure-attribution-gate-2026-09-30.md`

```text
FRONTIER_V4 = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox,
  Rakazo
]

FRONTIER_COUNT = 9

Gobii = CURRENT_PIN_PRIVACY_REGRESSION_BLOCK
PersonalJarvis = CURRENT_PIN_POLICY_COVERAGE_BLOCK
OpenGrokBot = BROWSER_EFFECT_GATE_OPEN

NEW_TECHNICAL_ELIMINATIONS = 0
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Rakazo enters only because the failed global workflow is attributable to an unrelated onboarding test while the exact-pin authority/isolation cases relevant to Gate 2 executed successfully with scope.


## Gate-2 frontier V5 — 2026-09-30

Exact-pin hosted evidence now supports twelve candidates for composition-only follow-up:

```text
FRONTIER_V5 = [
  AI Butler,
  AgentOS,
  Octop,
  Rome,
  Engram,
  Suna,
  Letta Code,
  RustFox,
  Rakazo,
  OpenMausBot,
  NanoClaw,
  QwenPaw
]

FRONTIER_COUNT = 12
REMAINING_NON_FRONTIER = 13

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

New admissions:

- OpenMausBot: exact-pin cross-platform CI with request-auth, permission-proxy, CUA isolation, approval-mode, peer-approval, routine delegation/cron/continuity and behavior eval execution.
- NanoClaw: exact-pin CI with 3033 primary tests plus permission, approval, restart, mount-security, task and container-restart contracts.
- QwenPaw: exact-pin contract/integration matrix with 412 contract tests passing; four Python 3.13 PTY failures are runtime-specific and remain scoped rather than being treated as authority failure.

Canonical non-frontier disposition:

`docs/evaluation/naia-gate2-non-frontier-hosted-evidence-disposition-2026-09-30.md`

No candidate is shortlisted or selected by frontier admission.


## Common Gate-2 composition harness frozen — 2026-09-30

Canonical protocol:

`docs/evaluation/naia-gate2-common-composition-harness-v1-2026-09-30.md`

Machine-readable matrix:

`docs/evaluation/naia-gate2-common-composition-matrix-v1-2026-09-30.yaml`

The twelve transferable-evidence candidates now share one black-box Atento composition contract:

```text
ISO-1 cross-memory read
ISO-2 cross-memory mutation
ISO-3 cross-credential use
ISO-4 cross-tool/channel use
ISO-5 silent cross-role invocation
ISO-6 explicit broker positive control
```

```text
FRONTIER_CANDIDATES = 12
COMMON_ASSERTIONS_PER_CANDIDATE = 6
COMMON_ASSERTIONS_TOTAL = 72

COMMON_COMPOSITION_HARNESS = FROZEN_V1
GATE2_EMPIRICAL_PASS = 0
NEXT_EXECUTION_TARGET = AI Butler
```

Candidate-specific tests are limited to the explicit add-ons in the matrix. Broad upstream retesting remains forbidden as redundant.

Execution order is evidence-minimizing, not a ranking.


## Gate-2 empirical execution attempt / evidence exhaustion — 2026-09-30

Canonical records:

- `docs/evaluation/naia-gate2-empirical-execution-infrastructure-block-2026-09-30.md`
- `docs/evaluation/naia-gate2-evidence-exhaustion-gate-2026-09-30.md`

The first Atento-hosted common-composition execution was attempted against AI Butler.

```text
LOCAL_MATERIALIZATION = BLOCKED_DNS
HOSTED_JOB_CREATED = YES
HOSTED_JOB_STEPS = []
CANDIDATE_CHECKOUT = NOT_RUN

AI_BUTLER_COMPOSITION = BLOCKED_ENVIRONMENT
```

No candidate code or assertion executed, so this is not a candidate failure.

Current Gate-2 state:

```text
TECHNICAL_SURVIVORS = 25
TRANSFERABLE_FRONTIER = 12
NON_FRONTIER = 13

GATE2_EMPIRICAL_PASS = 0
GATE2_STRUCTURAL_FAIL_FROM_EMPIRICAL = 0
GATE2_EXECUTION_INFRA = BLOCKED

STATIC_RESEARCH_LOOP = CLOSED_FOR_CURRENT_PINS
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Further Gate-2 progress requires executable exact-pin composition or materially new upstream executed evidence. Broad static/CI reconciliation is now considered exhausted at the frozen pins.


## Gate-2 composition execution block — 2026-09-30

Canonical evidence:

`docs/evaluation/naia-gate2-composition-execution-block-2026-09-30.md`

The common composition harness is frozen and ready, but this executor cannot acquire exact upstream runtime pins because `github.com` DNS resolution fails and no candidate checkout is preloaded locally.

```text
COMMON_COMPOSITION_EXECUTION = BLOCKED_ENVIRONMENT
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL

AI_BUTLER_COMPOSITION = BLOCKED_ENVIRONMENT
OPENMAUSBOT_COMPOSITION = BLOCKED_ENVIRONMENT
NANOCLAW_COMPOSITION = BLOCKED_ENVIRONMENT

GATE2_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The same infrastructure precondition applies to the rest of the 12-candidate frontier in this executor. Do not convert the shared infrastructure failure into per-candidate negative evidence.


## Gate-2 execution infrastructure + broker contract — 2026-09-30

Two separate common conditions now govern the first empirical Gate-2 PASS.

### Executor condition

Observed local and hosted execution infrastructure is currently unavailable:

```text
LOCAL github.com DNS = BLOCKED
LOCAL exact candidate checkout = ABSENT

GitHub Actions AI Butler run:
  run_id = 36789543149
  job_id = 110138936806
  runner_id = 0
  steps = []
  candidate code executed = NO
```

Therefore:

```text
EXECUTION_INFRA = BLOCKED_ENVIRONMENT
EXECUTION_INFRA != CANDIDATE_FAIL
```

### Explicit broker condition

Canonical broker contract:

`docs/evaluation/naia-gate2-handoff-broker-contract-v1-2026-09-30.md`

Reference harness implementation:

- `evals/atentoeval/handoff_broker.py`
- `evals/tests/test_handoff_broker.py`

Evidence validator:

- `evals/atentoeval/composition.py`
- `evals/config/naia_gate2_composition_v1.json`
- `evals/tests/test_composition.py`

The validator explicitly forbids converting a synthetic broker echo into `ISO-6 PASS`.

```text
BROKER_CONTRACT_FROZEN = YES
BROKER_RUNTIME_INTEGRATION_PROVEN = NO

GATE2_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

A future Gate-2 candidate PASS requires both candidate-specific composition evidence and a real runtime broker path conforming to the frozen contract.
