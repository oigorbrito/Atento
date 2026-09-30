# NAIA persistent-agent discovery expansion — 2026-09-29

## Contract

This record expands the NAIA candidate universe after the initial seven-candidate static block.

It does not rank, shortlist, select, qualify, accept or promote any candidate.

```text
ENUMERATED != QUALIFIED
QUALIFIED != SHORTLISTED
SHORTLISTED != SELECTED
EXTERNAL_SIGNAL != LOCAL_PROOF
UPSTREAM_TEST != ATENTO_DELTA_PASS
PRODUCT_REFERENCE != ADOPTABLE_SOURCE
```

For this technical discovery phase, license is not used as an exclusion or ordering criterion. Legal/adoption metadata remains a separate concern and must not distort technical enumeration.

```text
LICENSE_FILTER_FOR_TECHNICAL_DISCOVERY = DISABLED
```

## 1. Reference product shape

The discovery target is broader than "chatbot with tools".

Two current closed products make the target shape concrete.

### Grok Bot

Official product documentation describes persistent named Bots with:

- a persistent cloud computer;
- browser, filesystem and terminal;
- long-lived memory/context;
- work that continues while the user's device is closed;
- bot-to-bot coordination and handoff;
- learned workflows/skills from demonstration;
- scheduled/event-driven routines;
- explicit approval points.

Reference:
https://docs.x.ai/grok-bot/overview

### Meta Muse

Official product documentation describes:

- a persistent isolated Linux VM;
- a browser shared by user and agent;
- proactive work against longer-lived goals;
- persistent state and personalization;
- user intervention/control over computer actions.

Reference:
https://ai.meta.com/muse/

These are **product-shape references**, not source candidates.

They add useful discovery axes:

```text
persistent named identity
+ persistent computer/browser state
+ background/proactive execution
+ routine/schedule/event wakeups
+ approvals / human boundaries
+ long-lived memory
+ multi-agent or delegated coordination
+ user-visible activity/history
```

These axes supplement, not replace, the existing NAIA minimum capability profile.

## 2. Newly surfaced high-relevance technical candidates

The following repositories satisfy enough of the persistent-agent product shape to require comparable admission/audit work before the candidate universe can be considered closed.

### Rakazo

Repository:
`elie222/rakazo`

Observed head:
`f4583525d632fcd8643fd6e24c7f51e3e04cb990`

Product shape:

- explicitly positions itself as an open Grok Bot alternative;
- persistent bots with conversations, memory, routines and history;
- shared team computers and isolated private computers;
- browser, terminal, files and graphical desktop;
- peer-bot delegation and short-lived subagents;
- multiple computer providers including local Docker and remote sandboxes;
- app integrations and MCP/OpenAPI surfaces;
- web, desktop and mobile clients.

Repository evidence surface includes:

- unit/property tests;
- integration tests;
- Playwright E2E;
- topology/recovery tests;
- approval tests;
- browser/computer conformance tests;
- real-provider E2E/canary paths;
- explicit performance documentation.

Classification:

```text
PERSISTENT_AGENT_PRODUCT_SHAPE = STRONG
DIRECT_GROK_BOT_CLASS_MATCH = YES
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### Gobii

Repository:
`gobii-ai/gobii-platform`

Observed head:
`c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb`

Product shape:

- persistent AI employees with identity;
- per-agent durable queue/event wakeups;
- schedules and cron;
- real browser/computer execution;
- email/SMS/event contact surfaces;
- multi-agent coordination;
- persistent workspace/context;
- approval and contact boundaries;
- secret/credential handling;
- sandbox-compute support.

The repository contains a first-class eval subsystem under `api/evals` with scenarios directly relevant to NAIA, including:

- scheduled work cycles;
- responsibility boundaries;
- secure credential delegation;
- computer integration;
- structured peer handoffs;
- outreach safety;
- capability routing;
- notification terminality;
- webhook/event behavior.

Classification:

```text
PERSISTENT_AGENT_PRODUCT_SHAPE = STRONG
DURABLE_EVENT_DRIVEN_AGENT_RUNTIME = PRESENT
UPSTREAM_EVAL_SURFACE = STRONG
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### TencentCloud Octop

Repository:
`TencentCloud/Octop`

Observed head:
`e473dd3c4a4741618ffde1a42a3492341a189e8e`

Product shape:

- self-hosted multi-user, multi-agent assistant;
- per-expert workspace/providers/channels/cron;
- web dashboard, CLI and multiple messaging channels;
- proactive cron;
- browser automation;
- remote desktop / GUI work;
- tool approval and shell guardrails;
- portable memory;
- connector/MCP ecosystem;
- restart-safe control-plane state.

Classification:

```text
PERSISTENT_ASSISTANT_PRODUCT_SHAPE = STRONG
MULTI_USER_MULTI_AGENT = YES
BROWSER_AND_DESKTOP_SURFACE = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### PersonalJarvis

Repository:
`PersonalJarvis/PersonalJarvis`

Observed head:
`1be33c457739ca7e161ee6fbaf298ec10d4dad3b`

Product shape:

- persistent personal-assistant application;
- schedules/routines with visible run history;
- browser;
- native computer-use paths;
- Linux/macOS/Windows surfaces;
- persistent conversation/memory;
- safety/approval surfaces;
- mission/recovery code;
- connected channels/calling.

Upstream documentation records explicit platform validation boundaries, including real browser runs and contract tests for routine hooks and conversation continuity.

Classification:

```text
PERSISTENT_ASSISTANT_PRODUCT_SHAPE = STRONG
DESKTOP_COMPUTER_USE = PRESENT
UPSTREAM_PLATFORM_CONTRACT_EVIDENCE = MATERIAL
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### Letta Code

Repository:
`letta-ai/letta-code`

Observed head:
`21daa38a8cdd74f2d03b634c8312253080bacfc1`

Product shape:

- long-lived agents with identity and persistent memory;
- continual learning/reflection;
- always-on/proactive operation;
- crons and heartbeats;
- Slack/Telegram/Discord/custom channels;
- permissions/approval modes;
- background subagents and cross-agent calls;
- remote computers;
- secret delivery with values kept out of normal context.

The source tree includes substantial tests around:

- approval execution and recovery;
- interrupt/turn recovery;
- memory confinement and conflict repair;
- cron/scheduler behavior;
- cross-agent permission guards;
- sandbox transfer;
- channel contracts.

Classification:

```text
PERSISTENT_AGENT_RUNTIME = STRONG
PRODUCT_HARNESS_HYBRID = YES
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### Kortix / Suna

Repository:
`kortix-ai/suna`

Observed head:
`270c4a57c8ae5ffb85eff6d5b9700c5713612f28`

Product shape:

- agent management system rather than one-shot agent;
- named logical agents;
- persistent project/repository context;
- cron, webhook and monitor triggers;
- agent-scoped connector, secret, skill and sandbox grants;
- isolated session runtimes;
- browser/sandbox execution;
- deployment/self-hosting control plane;
- deterministic browser/release test lanes.

Upstream test guidance documents:

- unit/package checks;
- deterministic browser journeys;
- exact-SHA staging smoke/full release gates;
- timing artifacts;
- production release blocking on mismatched SHA or failed journeys.

Classification:

```text
PERSISTENT_AGENT_PLATFORM = STRONG
TEAM/PROJECT_ORIENTED = YES
COMPARABLE_TO_NAIA_CHASSIS = REQUIRES_ROLE_FIT_AUDIT
CURRENT_PIN_QUALIFIED = NO
```

### Rome

Repository:
`rome-os/rome`

Observed head:
`ef523c4659149e2711744deb04ec42c3be339907`

Product shape:

- explicitly positions itself as an open alternative to Grok Bot and Meta Muse;
- persistent recursive agents;
- scheduled work;
- memory/persistence;
- reusable executable actions;
- custom apps/interfaces;
- approval-aware actions;
- self-hosted runtime;
- compounding skills/SOPs rather than disposable sessions.

Classification:

```text
PERSISTENT_AGENT_PRODUCT_SHAPE = STRONG
DIRECT_GROK_BOT_MUSE_CLASS_MATCH = YES
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

### Agent Zero

Repository:
`agent0ai/agent-zero`

Observed head:
`e3051fb584b1a36be2b0a0c90606f1c2c2d356ec`

Product shape:

- full Linux computer environment;
- browser automation and host-browser bridge;
- desktop computer use;
- persistent vector memory;
- project-scoped memory/secrets/instructions;
- scheduled operations;
- multi-agent/subordinate execution;
- Web UI and plugin ecosystem.

The project calls itself a framework, so admission must distinguish its product/runtime surface from framework-only components.

Classification:

```text
PRODUCT_RUNTIME_SURFACE = STRONG
FRAMEWORK_PRODUCT_BOUNDARY = REQUIRES_ADMISSION_AUDIT
COMPARABLE_CANDIDATE = PROVISIONAL_YES
CURRENT_PIN_QUALIFIED = NO
```

### OpenGrokBot

Repository:
`wolfqing/OpenGrokBot`

Observed head:
`43ba51fc0487b7adbb23861a1062a113390833d9`

Product shape:

- explicitly models always-on AI teammates;
- one isolated computer/container per bot;
- persistent browser login/session state;
- memory and routines;
- group threads and bot-to-bot handoffs;
- allowlisted handoff directions;
- approval UI;
- browser/terminal/filesystem.

The repository is materially smaller/newer than several candidates above. That is a maturity signal, not a rejection.

Classification:

```text
DIRECT_GROK_BOT_CLASS_MATCH = YES
PERSISTENT_AGENT_PRODUCT_SHAPE = PRESENT
MATURITY = REQUIRES_AUDIT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
```

## 3. Existing discovery pool — now technically plausible

The old discovery pool remains relevant and should no longer be treated as merely names without product-shape evidence.

### SelfAgent

`oezercet/SelfAgent`
observed head `c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1`

Exact-pin admission confirms a persistent personal-assistant product with SQLite/semantic memory, Playwright browser, email/terminal/system tools and scheduling.

Material admission constraints:

- consequential tools mark `requires_confirmation`, but the central agent/registry execution path does not enforce that metadata;
- the scheduler persists JSON definitions but startup does not call its `_load()` path or re-arm persisted jobs;
- scheduled commands execute raw shell outside the ordinary tool registry/terminal blocklist;
- the current product is single-agent, so strict NAIA/Anna isolation requires separate runtime/store/config domains.

```text
COMPARABLE_CANDIDATE = YES
ADMISSION_AUDIT = COMPLETE
CURRENT_PIN_QUALIFIED = NO
```

### GoClaw

`sausheong/goclaw`
observed head `c24c50ba2d16daff6aa2809b6c1a6f592977ae54`

Exact-pin admission confirms a persistent multi-agent assistant runtime with messaging channels, cron/heartbeat, browser, per-agent workspaces/sessions and tool policy.

Material admission constraints:

- the default shell execution policy is `full`;
- per-agent workspaces and sessions are real, but BM25 memory and Cortex are instance-global and injected into all runtimes without an agent namespace;
- `ask_agent` can address any configured agent when the tool is available; one-level recursion prevention is not a role authorization boundary.

```text
COMPARABLE_CANDIDATE = YES
ADMISSION_AUDIT = COMPLETE
CURRENT_PIN_QUALIFIED = NO
```

### Nebo

`NeboLoop/nebo-go`
observed head `d566d27ec7c5ab36f3b95fdfda371bb45994dfd7`

Exact-pin admission confirms a persistent desktop personal-assistant product with memory, browser/desktop, scheduling, subagents, channels and an app platform.

Material admission constraints:

- hard host safeguards are implemented and directly tested in source;
- the current source enables shell denies for comm/app/skill origins even though one exact-pin security-doc paragraph is stale and says the deny list is disabled;
- default interactive policy is allowlist/on-miss;
- system-origin work (reminders/heartbeat/recovery) auto-approves ordinary approval requests;
- the product is one persistent companion context, so strict NAIA/Anna isolation requires separate runtime/data authority domains.

```text
COMPARABLE_CANDIDATE = YES
ADMISSION_AUDIT = COMPLETE
CURRENT_PIN_QUALIFIED = NO
```

## 4. Secondary discovery pool — screened

The bounded same-protocol screen is recorded in:

`docs/evaluation/naia-secondary-pool-admission-screen-2026-09-30.md`

Exact-pin result:

~~~text
ADMITTED_COMPARABLE:
  - supastishn/AutoMate
  - use-agent-os/agent-os
  - TBNRFPS01/OpenAgent
  - hubos-ai/HubOS
  - radotsvetkov/engram
  - holt-os/holt
  - chinkan/RustFox

DEFERRED_AT_CURRENT_PIN:
  - truenorth-lj/open-intern
~~~

Open Intern remains in discovery history, but its exact current pin explicitly marks proactive heartbeat, human approval workflow and browser automation as not yet shipped. Re-admission is triggered by a material upstream release that closes those product-surface gaps.

The seven admitted systems require upstream evidence/transfer mapping before any local NCP.

## 5. Result

The registered discovery pools have now received bounded admission screening.

~~~text
PREVIOUS_ENUMERATED_SET_COMPLETE = NO
REGISTERED_DISCOVERY_POOL_SCREENING = COMPLETE_V1
FROZEN_CANDIDATE_UNIVERSE_V1 = COMPLETE
CANDIDATE_UNIVERSE_COMPLETE = true_for_frozen_v1_snapshot

NEW_COMPARABLE:
  - Rakazo
  - Gobii
  - Octop
  - PersonalJarvis
  - Letta Code
  - Kortix/Suna
  - Rome
  - Agent Zero
  - OpenGrokBot
  - SelfAgent
  - GoClaw
  - Nebo
  - AutoMate
  - AgentOS
  - OpenAgentd
  - HubOS
  - Engram
  - Holt
  - RustFox

DEFERRED_AT_CURRENT_PIN:
  - Open Intern

REFERENCE_PRODUCTS:
  - Grok Bot
  - Meta Muse

LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~

The frozen V1 universe is a decision snapshot, not a claim that no future project can ever be discovered. Reopen discovery only for a material new candidate or material upstream delta; do not continuously broaden the search while decision-relevant evidence remains unresolved.

The next block is upstream evidence and transfer reconciliation for the seven newly admitted secondary candidates, not local benchmarking.
