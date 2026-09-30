# NAIA external evidence preflight — 2026-09-29

## Purpose

Make the evidence order explicit before any new local benchmark or NCP runtime probe.

Canonical rule:

```text
EXTERNAL_EVIDENCE
  ↓
TRANSFER / RELEVANCE CHECK
  ↓
REUSE PROVEN MECHANISM
  ↓
TEST ONLY MATERIAL LOCAL DELTAS
  ↓
LOCAL ACCEPTANCE
```

This record applies that rule to the expanded persistent-agent universe.

It does not rank candidates.


Expanded same-protocol upstream matrix:

`docs/evaluation/naia-expanded-upstream-evidence-matrix-2026-09-29.md`

## 1. Evidence classes

### PRODUCT_REFERENCE

Closed or externally operated product evidence that sharpens the product target but cannot prove source/runtime properties for an Atento base.

Examples:

- Grok Bot;
- Meta Muse.

### UPSTREAM_EXECUTABLE_TESTS

Source-owned tests that directly exercise a relevant contract.

Possible transfer state:

`UPSTREAM_PROVEN` or `TRANSFERABLE_WITH_CONSTRAINTS`.

### UPSTREAM_EVAL

A reproducible upstream behavioral/product eval with a declared scenario/protocol.

It answers only the axes it measures.

### INDEPENDENT_EXTERNAL_RUN

A third-party reproducible run on a named revision/environment.

Useful signal, but:

```text
INDEPENDENT_EXTERNAL_RUN != CURRENT_PIN_PROOF
```

### DOC_ONLY

Documentation/product claim without execution evidence.

Useful for discovery, not a runtime pass.

## 2. High-value upstream evidence already visible

### Rakazo

Exact discovery pin:
`f4583525d632fcd8643fd6e24c7f51e3e04cb990`

Repository test surface visibly includes:

- unit/property tests;
- Postgres/worker integration journeys;
- Playwright E2E;
- routine execution/failure flows;
- approval/resume and consequential-approval flows;
- screen/computer isolation;
- browser/computer conformance;
- topology/recovery tests;
- real E2B/Daytona/Box provider variants;
- explicit real vision-model + desktop computer acceptance path;
- performance documentation.

Preflight:

```text
UPSTREAM_EVIDENCE_DENSITY = HIGH
FIRST_ACTION = MAP_TESTS_TO_NAIA_CONTRACTS
LOCAL_BENCHMARK = NOT_YET_JUSTIFIED
```

### Gobii

Exact discovery pin:
`c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb`

Canonical `api/evals` scenarios cover material NAIA questions:

- scheduled work cycles;
- secure credential delegation;
- responsibility boundaries;
- computer integration;
- structured peer handoffs;
- capability routing;
- outreach safety;
- notification terminality;
- webhook behavior;
- message quality and follow-up behavior.

Developer documentation distinguishes unit tests, simulated evals and live evals.

Preflight:

```text
UPSTREAM_EVAL_SURFACE = HIGH_VALUE
FIRST_ACTION = INSPECT_PROTOCOL + AVAILABLE_RUN_ARTIFACTS
LOCAL_BENCHMARK = NOT_YET_JUSTIFIED
```

### Kortix / Suna

Exact discovery pin:
`270c4a57c8ae5ffb85eff6d5b9700c5713612f28`

Upstream documents:

- deterministic local stack;
- browser test lanes;
- package/unit lanes;
- exact deployed-SHA verification;
- target smoke/full staging tests;
- production release gate that rejects SHA mismatch or failed configured journey;
- emitted timing/benchmark artifacts.

Preflight:

```text
UPSTREAM_RELEASE_GATE_EVIDENCE = MATERIAL
FIRST_ACTION = MAP RELEASE JOURNEYS TO NAIA PROFILE
LOCAL_BENCHMARK = NOT_YET_JUSTIFIED
```

### PersonalJarvis

Exact discovery pin:
`1be33c457739ca7e161ee6fbaf298ec10d4dad3b`

Upstream docs/source expose explicit contract tests and platform evidence for:

- routine hooks;
- durable task inbox;
- archive reopening / conversation continuity;
- memory correction/compaction;
- routine ownership/permissions;
- browser installation/runtime;
- Windows computer-use paths;
- OS-specific gaps marked as unverified rather than generalized.

Preflight:

```text
UPSTREAM_PLATFORM_EVIDENCE = MATERIAL
FIRST_ACTION = TRANSFERABILITY_MAP_BY_TARGET_OS
LOCAL_DESKTOP_TEST = ONLY_FOR_UNPROVEN_TARGET_OS_DELTA
```

### Letta Code

Exact discovery pin:
`21daa38a8cdd74f2d03b634c8312253080bacfc1`

Visible test surface includes:

- approval execution/recovery;
- headless pending approval recovery;
- interrupt recovery;
- turn recovery policy;
- cron scheduler/run logs;
- memory confinement and conflict repair;
- memory filesystem integration;
- cross-agent guard tests;
- sandbox transfer;
- channel contracts;
- scheduled/proactive invocation mechanisms.

Preflight:

```text
UPSTREAM_CONTRACT_EVIDENCE = HIGH
FIRST_ACTION = MAP PERMISSION/MEMORY/CRON TESTS TO NCP AXES
LOCAL_BENCHMARK = NOT_YET_JUSTIFIED
```

### OpenGrokBot

Exact discovery pin:
`43ba51fc0487b7adbb23861a1062a113390833d9`

Visible source tests cover:

- approvals;
- computer lifecycle;
- memory;
- routines;
- scheduler;
- corresponding UI chips/panels.

Preflight:

```text
UPSTREAM_CONTRACT_EVIDENCE = PRESENT
MATURITY_EVIDENCE = LIMITED
LOCAL_PROBE = DEFER_UNTIL_SOURCE_CONTRACT_AUDIT
```

### Agent Zero

Exact discovery pin:
`e3051fb584b1a36be2b0a0c90606f1c2c2d356ec`

Current product/source surface includes:

- persistent project-scoped memory;
- scheduler APIs;
- browser runtime;
- local/host computer-use;
- project-scoped settings;
- permission surfaces;
- plugin extension paths.

Preflight:

```text
UPSTREAM_PRODUCT_SURFACE = STRONG
EXACT_CONTRACT_TEST_MAP = NOT_YET_COMPLETE
LOCAL_PROBE = DEFER
```

### Octop

Exact discovery pin:
`e473dd3c4a4741618ffde1a42a3492341a189e8e`

Repository contains a substantial tests surface and explicit browser/cron/memory/security modules.

An independent external run has also been reported on an older September revision/environment. That evidence is useful as an operational signal only; it does not transfer as current-pin proof.

Preflight:

```text
UPSTREAM_TEST_SURFACE = PRESENT
INDEPENDENT_EXTERNAL_RUN = SIGNAL_ONLY
FIRST_ACTION = EXACT_PIN_TEST/CI INVENTORY
LOCAL_PROBE = DEFER
```

### Rome

Exact discovery pin:
`ef523c4659149e2711744deb04ec42c3be339907`

Upstream publishes unit checks and a product architecture built around persistent actions/apps/memory/routines.

Preflight:

```text
UPSTREAM_PRODUCT_CONTRACT = MATERIAL
RUNTIME_EXECUTION_EVIDENCE = REQUIRES_INVENTORY
LOCAL_PROBE = DEFER
```

## 3. Existing seven candidates

The previous work remains reusable.

### OpenClaw

Reuse:

- historical Atento runtime qualification where the mechanism is unchanged;
- current-pin static delta audit;
- upstream tests for changed ownership/policy/memory contracts.

Do not rerun generic benchmarks.

### OpenMausBot

Reuse:

- historical Atento evidence;
- current changed-contract E2E/source wiring;
- request-auth/lending-memory tests.

Only changed current-pin contracts may eventually need execution.

### QwenPaw

Reuse upstream/source tests for governance, sandbox fallback and computer-use approval semantics.

The local question is only the hardened NAIA configuration delta.

### AI Butler

Reuse static/source contracts and upstream readiness labels/tests.

Runtime work should be limited to target deployment deltas.

### NanoClaw

Reuse skill/integration tests and current change-surface audit.

Do not benchmark an uncomposed trunk; freeze a capability recipe first.

### TrustClaw

Reuse local source contracts for memory/cron and treat Composio-controlled surfaces as dependency evidence.

Do not convert external service claims into local authority proof.

### Open Assistant

Reuse static contract audit and exact-pin source tests.

For current technical discovery, license is not used to defer or exclude the candidate.

## 4. Gate before any local NCP

A local NCP or benchmark may run only after all five are true:

```text
1. candidate exact pin frozen
2. upstream implementation/contract located
3. upstream tests/evals located
4. available run/CI artifacts checked
5. remaining Atento delta stated in one sentence
```

If item 5 cannot be stated, the local test is not yet justified.

## 5. Expanded transfer-audit progress

The comparable expanded candidates now have bounded transfer audits for:

- Suna / Letta Code / PersonalJarvis;
- Rakazo / Gobii;
- Octop / Agent Zero / Rome / OpenGrokBot.

The newest transfer record is:

docs/evaluation/naia-transfer-audit-octop-agentzero-rome-opengrokbot-2026-09-30.md

No generic local NCP is justified by those four audits. Their remaining questions are configuration/topology deltas, not missing broad product benchmarks.

The next universe-completion block is the provisional admission pass for:

~~~text
SelfAgent
GoClaw
Nebo
~~~

Only after that admission block should the candidate-universe gate be reconsidered.

## 6. Candidate-universe gate

The candidate universe is still open.

The discovery expansion record is:

`docs/evaluation/naia-persistent-agent-discovery-2026-09-29.md`

Until the new comparable candidates receive at least a same-protocol admission/completeness pass:

```text
CANDIDATE_UNIVERSE_COMPLETE = false
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The next work is therefore **external evidence reconciliation and candidate admission**, not local benchmarking.
