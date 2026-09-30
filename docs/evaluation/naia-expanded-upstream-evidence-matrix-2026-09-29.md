# NAIA expanded upstream-evidence matrix — 2026-09-29

## Contract

This record maps **external/upstream evidence** for the newly expanded persistent-agent candidate set.

It does not run local benchmarks and does not rank candidates.

```text
TEST_SOURCE_PRESENT != TEST_EXECUTED
UPSTREAM_EVAL_PROTOCOL != LIVE_EVAL_PASS
DOCS_CLAIM != RUNTIME_PASS
INDEPENDENT_RUN_AT_OLDER_PIN != CURRENT_PIN_PROOF
BENCHMARK_SIGNAL != LOCAL_PROOF
```

All exact pins below were checked for observable GitHub workflow runs / combined statuses through the available connector. For the pins inspected here:

```text
workflow_runs = []
combined_statuses = []
```

unless otherwise stated.

Therefore no candidate receives a hosted code/eval PASS or FAIL from CI visibility alone.

## 1. Rakazo

Repository:
`elie222/rakazo`

Pin:
`f4583525d632fcd8643fd6e24c7f51e3e04cb990`

### Upstream evidence present

The repository exposes a broad test hierarchy:

- unit/property tests;
- Postgres/worker integration tests;
- Playwright E2E;
- routine execution and persistence;
- approval pause/resume flows;
- consequential-action confirmation flows;
- browser/computer conformance;
- screen-proxy isolation;
- topology/recovery tests;
- real sandbox-provider variants for E2B/Daytona/Box;
- an explicit real vision-model + computer acceptance path;
- deterministic desktop performance harness.

Material source contracts observed:

- approval envelopes are bound to connector/resource/tool and optional resource revision;
- OAuth/resource revision changes can invalidate stale approval replay;
- duplicate external effects have explicit persisted states;
- an interrupted effect in `executing` becomes `uncertain`;
- uncertain effects are not automatically replayed, avoiding silent duplicate side effects;
- routines have E2E persistence coverage;
- screen proxy capabilities are revocable and isolated from app cookies/storage;
- Team computers share an OS/workspace and are explicitly **not** security boundaries;
- Private computers provide the stronger per-bot computer boundary.

Material default caveat:

The current UI E2E explicitly establishes that consequential actions run automatically by default unless optional action-confirmation rules are configured.

Classification:

```text
UPSTREAM_TEST_DENSITY = HIGH
APPROVAL_BINDING_STATIC = STRONG
EXTERNAL_EFFECT_UNCERTAIN_STATE = PRESENT
AUTO_CONFIRMATION_DEFAULT = PERMISSIVE
PRIVATE_COMPUTER_ISOLATION = AVAILABLE
TEAM_COMPUTER_ISOLATION = NOT_A_SECURITY_BOUNDARY
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, not before transfer mapping
```

## 2. Gobii

Repository:
`gobii-ai/gobii-platform`

Pin:
`c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb`

### Upstream evidence present

Gobii contains a canonical product-eval framework under `api/evals`.

The design explicitly separates:

- stable scenario code;
- asynchronous agent code under test;
- scenario injection through the API/Celery boundary;
- observation through persisted database state;
- fingerprinting of eval scenario code.

Relevant scenarios include:

- `scheduled_work_cycles`;
- `secure_credential_delegation`;
- `responsibility_boundaries`;
- `computer_integration`;
- `structured_peer_handoffs`;
- capability routing;
- outreach safety;
- webhook behavior;
- notification terminality.

Observed protocol details:

- scheduled-work scenarios trigger through the real agent harness;
- empty work cycles are expected to end quietly;
- ready work is expected to dispatch exactly once to the intended peer;
- structured handoff scenarios preserve record boundaries and exact fields;
- handoff scenarios explicitly test leakage of unrelated sensitive context;
- developer docs distinguish unit, simulated and live evals;
- `LOCAL_RUNS.md` contains run instructions, not committed live-result artifacts.

Classification:

```text
UPSTREAM_EVAL_PROTOCOL = HIGH_VALUE
REAL_HARNESS_SCENARIOS = PRESENT
LIVE_RESULT_ARTIFACTS_AT_PIN = NOT_OBSERVED
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, until upstream protocol/result availability is exhausted
```

## 3. Kortix / Suna

Repository:
`kortix-ai/suna`

Pin:
`270c4a57c8ae5ffb85eff6d5b9700c5713612f28`

### Upstream evidence present

The platform documents a deterministic test/release model with:

- root unit/package lanes;
- Playwright browser journeys;
- deterministic local stack;
- exact deployed-SHA verification;
- staging smoke/full target runs;
- production release gating on SHA parity and configured journey pass;
- timing artifacts written by test runs.

Product contracts relevant to NAIA include:

- named agents with explicit governance blocks;
- connector/secret/skill grants per agent;
- cron/webhook/monitor triggers;
- sandbox template selection;
- session strategy for triggered work;
- OpenCode permission/tool configuration beneath the Kortix governance layer.

Classification:

```text
UPSTREAM_RELEASE_GATE_PROTOCOL = STRONG
EXACT_SHA_GATING_DESIGN = PRESENT
PERSISTENT_AGENT_GOVERNANCE = PRESENT
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, before release-journey transfer audit
```

## 4. Letta Code

Repository:
`letta-ai/letta-code`

Pin:
`21daa38a8cdd74f2d03b634c8312253080bacfc1`

### Upstream evidence present

The source tree contains substantial direct tests for:

- approval execution and recovery;
- pending approval recovery in headless mode;
- interrupt/turn recovery;
- cron scheduler and run logs;
- memory confinement;
- memory filesystem integration;
- memory conflict repair;
- cross-agent permission guards;
- sandbox transfer;
- channel contracts;
- proactive self-invocation mechanisms.

Product contracts also include:

- long-lived identity and memory;
- background subagents;
- crons/heartbeats;
- remote computers;
- permissions;
- secrets kept out of normal context.

Classification:

```text
UPSTREAM_CONTRACT_TEST_DENSITY = HIGH
MEMORY/RECOVERY/PERMISSION_TESTS = DIRECTLY_RELEVANT
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, before contract transfer audit
```

## 5. PersonalJarvis

Repository:
`PersonalJarvis/PersonalJarvis`

Pin:
`1be33c457739ca7e161ee6fbaf298ec10d4dad3b`

### Upstream evidence present

Upstream documentation explicitly records platform validation boundaries rather than treating all OSes as equal.

Observed claims tied to named tests include:

- routine-hook authentication, HMAC, replay protection and persistence;
- archive reopening and conversation continuity;
- stable memory ids/corrections;
- configuration provenance;
- routine ownership/permissions;
- browser runtime installation;
- Windows native computer-use paths;
- explicit marking of macOS/Linux real-desktop gaps where unverified.

Classification:

```text
UPSTREAM_PLATFORM_CONTRACT_EVIDENCE = MATERIAL
TARGET_OS_TRANSFER_CHECK = REQUIRED
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_DESKTOP_TEST = ONLY_FOR_UNPROVEN_TARGET_OS_DELTA
```

## 6. Octop

Repository:
`TencentCloud/Octop`

Pin:
`e473dd3c4a4741618ffde1a42a3492341a189e8e`

### Upstream / external evidence present

The repository has an extensive test surface around:

- browser;
- cron;
- memory;
- security;
- multi-user/multi-agent state;
- desktop/runtime components.

A third-party sandboxed operational review was found for an older September revision and environment.

That run is useful as an independent execution signal, but it is not the exact current pin and must not be promoted to current-pin proof.

Classification:

```text
UPSTREAM_TEST_SURFACE = MATERIAL
INDEPENDENT_EXTERNAL_EXECUTION = OLDER_PIN_SIGNAL
EXACT_PIN_TRANSFER_AUDIT = COMPLETE_V1
DEFAULT_HITL = DISABLED
DEFAULT_TOOL_GUARD = WARN
PENDING_HITL_RESTART_CONTINUITY = NOT_ESTABLISHED
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, except later decision-critical composition deltas
```

## 7. Agent Zero

Repository:
`agent0ai/agent-zero`

Pin:
`e3051fb584b1a36be2b0a0c90606f1c2c2d356ec`

### Upstream evidence present

The product/runtime surface contains:

- persistent project-scoped memory;
- scheduler APIs;
- browser runtime;
- host-browser bridge;
- host computer-use plugins;
- project-scoped settings/secrets;
- Web UI and plugin lifecycle;
- scheduled operations.

The exact mapping from these product surfaces to directly relevant contract/e2e tests is not yet complete.

Classification:

```text
UPSTREAM_PRODUCT_SURFACE = STRONG
EXACT_PIN_TRANSFER_AUDIT = COMPLETE_V1
PROJECT_MEMORY_ISOLATION_DEFAULT = TRUE
TOOL_POLICY_DEFAULT = INHERIT_ALLOW
FRAMEWORK_PRODUCT_BOUNDARY = MAPPED_WITH_COMPOSITION_RESIDUALS
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, except later decision-critical composition deltas
```

## 8. Rome

Repository:
`rome-os/rome`

Pin:
`ef523c4659149e2711744deb04ec42c3be339907`

### Upstream evidence present

Rome's upstream product contract includes:

- persistent agents;
- scheduled work;
- memory;
- reusable executable actions;
- approval-aware actions;
- apps/interfaces generated around repeated workloads;
- self-hosting.

The repository documents ordinary unit/typecheck/build gates, but a comparable runtime/eval result at the exact pin has not yet been established.

Classification:

```text
UPSTREAM_PRODUCT_CONTRACT = MATERIAL
EXACT_PIN_TRANSFER_AUDIT = COMPLETE_V1
PROFILE_DATA_ISOLATION = EXPLICIT_CONTRACT
ACTION_APPROVAL = STRONG_WHEN_CONFIGURED
CAPABILITY_CREATION_AUTOAPPROVAL_DEFAULT = TRUE
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, except later decision-critical composition deltas
```

## 9. OpenGrokBot

Repository:
`wolfqing/OpenGrokBot`

Pin:
`43ba51fc0487b7adbb23861a1062a113390833d9`

### Upstream evidence present

Visible tests directly cover:

- approvals;
- computer lifecycle;
- memory;
- routines;
- scheduler;
- corresponding UI state.

Product docs describe:

- per-bot Docker computer;
- persistent browser login profiles;
- allowlisted bot-to-bot handoffs;
- routines and memory;
- approval UX.

Classification:

```text
UPSTREAM_CONTRACT_TESTS = PRESENT
DIRECT_GROK_BOT_CLASS_MATCH = YES
PER_BOT_CONTAINER_BOUNDARY = STRONG_STATIC_CONTRACT
OUTWARD_BROWSER_APPROVAL = CONVENTION_NOT_ENFORCEMENT
ROUTINE_TOOLSET = FULL
MATURITY_EVIDENCE = LIMITED
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
LOCAL_BENCHMARK_JUSTIFIED = NO, except later decision-critical composition deltas
```

## Transfer audit: Suna / Letta Code / PersonalJarvis

A deeper transferability pass is recorded in:

`docs/evaluation/naia-transfer-audit-suna-letta-jarvis-2026-09-29.md`

Key residuals found without local execution:

```text
Suna:
  v2 per-agent grants = deny-by-default
  connector policy default = allow_all
  project memory = shared project brain
  scheduler dedups fires, not arbitrary work/effects

Letta Code:
  default permission mode = unrestricted
  in-process cross-agent file guard = strong
  spawned shell cross-agent sandbox = opt-in
  shared memory / cross-agent discovery are intentional product features

PersonalJarvis:
  scheduled preauthorization = trace-bound + grant-bound
  society memory = agent namespace
  shell = local path containment, not container isolation
  strict per-society-agent credential isolation = not established
```

No generic local probe is justified yet.

## Transfer audit: Rakazo / Gobii

A deeper transferability pass is recorded in:

`docs/evaluation/naia-transfer-audit-rakazo-gobii-2026-09-29.md`

Key residuals found without local execution:

```text
Rakazo:
  Space = application privacy boundary in schema/source
  data-bearing credentials = Space scoped; bot secrets = user+space+bot
  approval replay = bound to resource/tool/revision/args
  interrupted external effect = explicit uncertain; no blind replay
  consequential-action default = permissive unless rules configured
  Team Computer != security boundary

Gobii:
  per-agent SQLite recovery + event lock/pending-drain contracts are strong
  secure credential delegation uses opaque refs into exact child/domain/key
  contact approval defaults to require_approval
  email content review is a separate policy and may default to automatic
  queue serialization != exactly-once external effects
```

No generic local NCP is justified yet.

## Transfer audit: Octop / Agent Zero / Rome / OpenGrokBot

A deeper transferability pass is recorded in:

docs/evaluation/naia-transfer-audit-octop-agentzero-rome-opengrokbot-2026-09-30.md

Key residuals found without local execution:

~~~text
Octop:
  default HITL = disabled
  default tool guard = warn
  pending HITL registry = process-local / TTL
  per-account default-open connectors can flow into empty Cron selections
  hardened NAIA security/profile composition is required

Agent Zero:
  project memory isolation default = true
  project secrets/agents/skills/MCP are scoped
  tool policy default = inherit + allow for local and MCP
  instance-wide plugins and host Computer Use are separate authority domains
  scheduled effective profile/policy composition remains an Atento delta

Rome:
  profile = explicit data-isolation boundary
  approval state machine/API = strong when requiresApproval is configured
  action visibility defaults public; requiresApproval is optional metadata
  agent-initiated skill/tool/workflow creation autoapproval defaults true
  Codex provider uses danger-full-access + approvalPolicy=never at the provider seam

OpenGrokBot:
  per-bot container/workspace and gateway approval endpoint boundaries are strong
  bot cannot authenticate its own hold approval
  outward browser hold discipline is explicitly not an enforcement point
  routines run with the full toolset
~~~

These are configuration/topology residuals, not reasons to run generic benchmarks now.

## Admission audit: SelfAgent / GoClaw / Nebo

The same-protocol admission record is:

`docs/evaluation/naia-admission-audit-selfagent-goclaw-nebo-2026-09-30.md`

Exact-pin admission results:

~~~text
SelfAgent:
  comparable persistent personal-assistant product = YES
  confirmation metadata exists but is not enforced by the central registry path
  scheduler definitions are persisted but startup reload/re-arm is not wired
  scheduled raw shell bypasses the interactive terminal/registry authority path
  strict NAIA/Anna composition requires separate runtimes/stores

GoClaw:
  comparable persistent multi-agent assistant product = YES
  per-agent sessions/workspaces/tool policies = PRESENT
  default bash policy = FULL
  BM25 memory + Cortex = INSTANCE_GLOBAL
  ask_agent target scope = ALL_CONFIGURED_AGENTS when enabled
  strict NAIA/Anna composition requires memory/store separation and delegation control

Nebo:
  comparable persistent desktop personal-assistant product = YES
  hard host safeguard + direct tests = PRESENT
  source-level comm/app/skill shell deny = ENABLED
  default interactive policy = ALLOWLIST / ON_MISS
  OriginSystem work auto-approves ordinary approval requests
  strict NAIA/Anna composition requires separate runtime/data authority domains
~~~

For all three exact pins:

~~~text
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
CURRENT_PIN_QUALIFIED = NO
LOCAL_GENERIC_NCP_NOW = NO
~~~

## Secondary-pool admission screen

The bounded secondary-pool screen is recorded in:

`docs/evaluation/naia-secondary-pool-admission-screen-2026-09-30.md`

Exact-pin result:

~~~text
ADMITTED_COMPARABLE:
  AutoMate
  AgentOS
  OpenAgentd
  HubOS
  Engram
  Holt
  RustFox

DEFERRED_AT_CURRENT_PIN:
  Open Intern
~~~

All eight screened pins had no observable GitHub workflow runs or combined statuses through the available connector, so no hosted PASS/FAIL is inferred.

The seven admitted candidates require upstream implementation/test/eval transfer mapping before any local NCP. Open Intern is deferred at its current pin because the repository itself marks proactive heartbeat, human approval workflow and browser automation as not yet shipped.

## 10. Cross-candidate conclusion

The expanded universe contains significantly more reusable upstream evidence than the original discovery pool implied.

The main next task is **not** to execute all upstream suites.

For each candidate:

```text
1. map exact upstream test/eval to NAIA property
2. determine whether config/topology keeps the same boundary
3. mark UPSTREAM_PROVEN or TRANSFERABLE_WITH_CONSTRAINTS where defensible
4. isolate ATENTO_DELTA / UNPROVEN only
5. run the smallest local check only for those residuals
```

Immediate state:

```text
EXPANDED_UPSTREAM_EVIDENCE_MATRIX = COMPLETE_V1
PROVISIONAL_SELFAGENT_GOCLAW_NEBO_ADMISSION = COMPLETE
REGISTERED_DISCOVERY_POOL_SCREENING = COMPLETE_V1
FROZEN_CANDIDATE_UNIVERSE_V1 = COMPLETE
CANDIDATE_UNIVERSE_COMPLETE = true_for_frozen_v1_snapshot
SECONDARY_TRANSFER_AUDITS = REQUIRED
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
