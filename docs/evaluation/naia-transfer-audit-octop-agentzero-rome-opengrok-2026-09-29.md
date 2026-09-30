# NAIA upstream transfer audit — Octop / Agent Zero / Rome / OpenGrokBot — 2026-09-29

## Contract

This record maps upstream mechanisms to reusable NAIA evidence and isolates the remaining Atento-specific deltas.

It does not rank, shortlist, qualify, accept or select any candidate.

```text
FEATURE_PRESENT != HARDENED_DEFAULT
TOOL_BLOCK_POLICY != HUMAN_APPROVAL
PER_AGENT_WORKSPACE != HOSTILE_MULTI_TENANT_ISOLATION
PROMPT_CONVENTION != ENFORCEMENT
```

Pins:

```text
Octop        e473dd3c4a4741618ffde1a42a3492341a189e8e
Agent Zero   e3051fb584b1a36be2b0a0c90606f1c2c2d356ec
Rome         ef523c4659149e2711744deb04ec42c3be339907
OpenGrokBot  43ba51fc0487b7adbb23861a1062a113390833d9
```

No exact-pin GitHub Actions run / combined status was observed for these four pins in the prior matrix.

---

## 1. Octop

### 1.1 Product/runtime comparability

Octop is a persistent assistant product, not merely a framework.

The current README documents:

- multi-user JWT auth;
- multiple experts per user;
- per-expert workspace, providers, channels and cron;
- persistent portable memory;
- browser automation with persistent profiles;
- remote desktop;
- connectors/MCP;
- proactive cron;
- one control-plane DB rebuilt into runtime state on boot.

```text
DIRECT_PERSISTENT_ASSISTANT_COMPARABILITY = YES
RESTART_REHYDRATION_DESIGN = PRESENT
```

### 1.2 Approval and shell guard defaults

The security-policy store gives a precise default:

```text
hitl.enabled = false
tool_guard.enabled = true
tool_guard.mode = warn
```

Unit and integration tests assert those defaults.

Octop supports:

- HITL tool approval for a configured tool catalog;
- block / warn / require_approval command-guard modes;
- approval cards and IM `/approve` / `/reject`;
- hot reload of security policy into running agents.

Therefore:

```text
HITL_ENFORCEMENT_MECHANISM = PRESENT
TOOL_GUARD_MECHANISM = PRESENT
DEFAULT_MATCHES_HARDENED_NAIA = NO
ATENTO_DELTA = EXPLICIT_SECURITY_POLICY
```

A hardened NAIA profile must not inherit HITL-off + warn-only shell guard.

The local delta, if Octop is later shortlisted, is configuration/catalog coverage: prove that all consequential browser/shell/connector paths are either blocked or placed behind approval as intended.

### 1.3 Agent/user isolation

Upstream product design provides:

- JWT user isolation;
- per-agent workspace;
- per-agent provider/channel/cron configuration;
- connector binding to agents;
- owner-gated skill/package operations.

It also intentionally supports shared expert packages, knowledge bases and team coordination.

Thus:

```text
PER_AGENT_WORKSPACE = PRESENT
PER_USER_AUTH_BOUNDARY = PRESENT
SHARED_RESOURCE_FEATURES = INTENTIONAL
STRICT_NAIA_ANNA_ISOLATION = REQUIRES_TOPOLOGY_AUDIT
```

Do not infer hostile multi-tenant isolation merely from separate expert directories.

### 1.4 Browser / desktop

Octop has first-class browser and remote-desktop surfaces, including persistent browser profiles.

This is a substantive product fit signal.

It does not by itself prove that a high-risk GUI action cannot bypass an approval catalog.

```text
BROWSER_COMPUTER_SURFACE = PRESENT
GUI_ACTION_AUTHORITY_PARITY = UNPROVEN
```

### 1.5 Octop residual

```text
OCTOP_ATENTO_DELTA:
  - turn HITL on for the consequential tool set
  - change command guard from warn to the required block/approval posture
  - map every browser/desktop/connector effect into that authority model
  - prove strict NAIA/Anna resource/credential topology
  - only then test any remaining restart/composition delta

LOCAL_GENERIC_NCP_NOW = NO
```

---

## 2. Agent Zero

### 2.1 Product/runtime boundary

Agent Zero has a substantial user-facing product/runtime surface:

- Web UI;
- scheduler;
- projects;
- memory;
- browser;
- Docker environment;
- host-browser/host-computer bridge;
- profiles/plugins;
- MCP and external integrations.

It is therefore technically comparable enough to retain in the universe even though it also describes itself as a framework.

```text
FRAMEWORK_PRODUCT_BOUNDARY = HYBRID
TECHNICAL_COMPARABILITY = YES
```

### 2.2 Tool policy

Agent Zero has real tool-policy enforcement, not only prompt advice.

Upstream tests verify:

- blocked tools disappear from prompt/tool schemas;
- execution rechecks policy after advertisement;
- profile policies remain isolated across prompt/schema/execution;
- local and MCP defaults can be controlled independently;
- explicit block wins at execution.

However the policy normalization defaults are:

```text
default = allow
mcp_default = allow
mode = inherit
```

and the UI presents non-custom policy as allow.

Therefore:

```text
TOOL_BLOCK_ENFORCEMENT = STRONG
DEFAULT_MATCHES_HARDENED_NAIA = NO
HUMAN_APPROVAL_BROKER_EQUIVALENT = NOT_ESTABLISHED
```

A deny-by-default custom profile is possible, but allow/block policy is not the same contract as trace-bound human approval and resume.

### 2.3 Project scoping

Projects are explicitly intended to keep context from leaking across unrelated work.

A project can own:

- instructions;
- files;
- memory;
- variables;
- encrypted project secrets;
- MCP servers;
- skills;
- model/profile overrides.

Tests cover project metadata, project-specific agent/profile availability and project MCP persistence.

This is useful scoping, but it is application-level project structure inside one Agent Zero deployment.

```text
PROJECT_CONTEXT_SCOPE = STRONG
PROJECT_SECRET_SCOPE = PRESENT
STRICT_PROCESS/AUTHORITY_ISOLATION = NOT_ESTABLISHED
```

For NAIA/Anna, separate projects alone are not yet a sufficient hard boundary.

### 2.4 Secret handling

Agent Zero's secret manager:

- stores named secrets;
- exposes aliases such as `§§secret(KEY)`;
- masks full secret values;
- uses a streaming filter to avoid chunk-boundary leakage;
- masks secrets in model/tool output paths;
- has project-specific encrypted `.a0proj/secrets.env` support.

Tests cover masking and lossless save/masked round-trip.

Transfer classification:

```text
SECRET_MASKING = UPSTREAM_PROVEN_BY_SOURCE_TESTS
PROJECT_SECRET_STORAGE = PRESENT
STRICT_AGENT_TO_AGENT_CREDENTIAL_SEPARATION = NOT_ESTABLISHED
```

### 2.5 Scheduler

The scheduler persists task definitions/results under `usr/scheduler`, supports scheduled/planned/ad-hoc tasks and project activation, and explicitly reloads/saves around success/error updates.

Current unit coverage includes timezone behavior and missing-context recovery behavior.

That is useful persistence evidence, but there is no current evidence here for exactly-once external effects or a fail-closed background authority boundary.

### 2.6 Browser / host computer

The default Docker browser is separated from the host.

Agent Zero also supports Bring Your Own Browser / host computer control. Its own docs warn that remote debugging grants full control of that browser session, including cookies/site data/navigation.

Therefore host-browser mode is a separate authority profile and must not inherit trust from the Docker-browser path.

### 2.7 Agent Zero residual

```text
AGENT_ZERO_ATENTO_DELTA:
  - explicit deny-by-default tool + MCP policy
  - add/compose a real human-approval contract for consequential effects if required
  - strict NAIA/Anna process/storage/credential topology
  - background scheduler authority parity
  - separate Docker-browser and host-browser risk profiles

LOCAL_GENERIC_NCP_NOW = NO
```

The largest open question is architectural, not benchmark performance: whether the missing approval/isolation boundary can be added through existing extension seams without a cross-cutting fork.

---

## 3. Rome

### 3.1 Approval engine

Rome has a DB-backed action approval engine with substantial E2E coverage.

The current approval-flow suite verifies:

- a sensitive root action creates a pending approval;
- a nested sensitive action also surfaces approval;
- multiple pending approvals coexist independently;
- approving runs the exact approved payload and resumes the session;
- rejecting does not execute the action;
- a second approve after execution is a no-op;
- pending approval persists rather than auto-expiring;
- HTTP approval can produce both live and durable continuation.

This is high-value reusable evidence.

```text
APPROVAL_PERSISTENCE = STRONG
APPROVAL_RESUME = STRONG
DUPLICATE_APPROVE_EXECUTION = PREVENTED
NESTED_ACTION_APPROVAL = PRESENT
```

### 3.2 Approval declaration gap

Rome action metadata distinguishes:

```text
sideEffects: read-only | write
requiresApproval?: boolean
```

Approval is therefore an explicit action property, not automatically implied by every write side effect.

That is a useful mechanism, but it creates a catalog-completeness obligation.

```text
APPROVAL_MECHANISM = STRONG
WRITE_IMPLIES_APPROVAL_AUTOMATICALLY = NO_EVIDENCE
ATENTO_DELTA = ACTION_CATALOG_HARDENING
```

For NAIA, every consequential action must be audited so an omitted `requiresApproval` cannot silently widen authority.

### 3.3 Policy engine

Rome also has a persisted policy engine.

Tests show:

- sender-specific, thread, sender-tier, channel and global policy scopes;
- actions `allow`, `block`, `require_approval`, `sentinel_review`;
- specificity wins over broader policy priority;
- non-trusted bond levels default to `sentinel_review`;
- trusted guardian level defaults to allow;
- decision events are emitted into traces.

This is useful ingress/social-authority governance, but it is distinct from action-level effect approval.

### 3.4 Routine durability

Rome routines are DB-backed and expose:

- activation/deactivation;
- manual run with persisted run history;
- trace retrieval;
- cancellation;
- cancellation repair that marks a run stuck `running` across a restart as `cancelled`;
- managed-by ownership preventing a guardian/dashboard path from deleting app-owned routines.

This is material persistent-runtime evidence.

It is not generic exactly-once external-effect proof.

### 3.5 Replay/effect contract

Rome has execution journals and stable action+argument hashes used for replay/divergence detection.

That is useful deterministic-replay machinery.

The audit does not yet establish provider reconciliation after:

```text
external effect applied
→ process dies
→ terminal local commit absent
```

So:

```text
DETERMINISTIC_ACTION_REPLAY = MATERIAL
GENERIC_EXTERNAL_EFFECT_EXACTLY_ONCE = NOT_PROVEN
```

### 3.6 Strict role isolation

Rome supports agents/subagents/delegated action workers and isolates some fork/session state.

The current evidence does not establish a strict NAIA-vs-Anna memory/credential/runtime boundary equivalent to ADR-001.

```text
MULTI_AGENT_EXECUTION = PRESENT
STRICT_ROLE_STORAGE/AUTHORITY_ISOLATION = UNPROVEN
```

### 3.7 Rome residual

```text
ROME_ATENTO_DELTA:
  - exhaustive consequential-action catalog audit
  - explicit NAIA/Anna memory/credential/runtime topology
  - adapter-specific ambiguous-effect reconciliation
  - only composition tests left after those mappings

LOCAL_GENERIC_NCP_NOW = NO
```

---

## 4. OpenGrokBot

### 4.1 Direct product-shape match

OpenGrokBot intentionally implements the Grok Bot class:

- persistent teammates;
- one Docker computer per bot;
- persistent browser profile/login state;
- memory;
- routines;
- group threads;
- bot-to-bot handoffs;
- approval chips;
- always-on operation.

```text
DIRECT_GROK_BOT_CLASS_MATCH = YES
```

### 4.2 Computer containment

The security document is unusually explicit.

Enforced properties include:

- each bot computer is a separate container;
- container-to-container traffic is disabled;
- per-container shell/CDP/VNC secrets;
- resource limits and no-new-privileges;
- only the bot's own workspace is mounted;
- gateway binds loopback by default;
- gateway auth token never enters the bot workspace.

Transfer classification:

```text
PER_BOT_COMPUTER_ISOLATION = STRONG_BY_DESIGN
BOT_CANNOT_AUTHENTICATE_GATEWAY = ENFORCED
PEER_CONTAINER_NETWORK = DENIED
```

### 4.3 Standing memory rules

`MEMORY.md` is stored gateway-side outside the bot workspace.

Tests verify:

- a workspace-written `MEMORY.md` is ignored;
- only gateway-side memory is read;
- migration from the old workspace location happens once;
- duplicate rule append is a no-op.

This prevents a bot from silently rewriting its own standing rules through ordinary workspace access.

```text
STANDING_MEMORY_OUTSIDE_COMPUTER = UPSTREAM_PROVEN_BY_SOURCE_TESTS
SILENT_WORKSPACE_MEMORY_OVERRIDE = DENIED
```

### 4.4 Handoff policy

A2A tests verify:

- peer directions are empty by default;
- chief ↔ teammate communication is allowed;
- optional peer directions are directional;
- self-message is denied;
- relay depth is capped at two.

This is a meaningful broker-like restriction.

### 4.5 Approval limitation — material

OpenGrokBot's own security document explicitly classifies outward-action approval as:

```text
a convention, not a wall
```

Bots are instructed to call `hold_for_approval`, and the approval database itself is idempotent, but a signed-in bot browser can still click Send directly.

This distinction is decisive for the NAIA authority model.

```text
APPROVAL_UI/STATE = PRESENT
APPROVAL_DECISION_IDEMPOTENCY = PRESENT
OUTWARD_EFFECT_ENFORCEMENT = NOT_HARD
PROMPT/AGENTS_MD_DISCIPLINE = INSUFFICIENT_FOR_NAIA
```

This is not a missing test. It is an upstream architectural boundary explicitly acknowledged by the project.

The required Atento delta is therefore structural unless every consequential path is moved behind controlled gateway adapters or equivalent browser/network enforcement.

### 4.6 Routines

Routine storage tests verify cron validation, persistent records and last-run metadata.

That is useful scheduler source evidence but not restart/fault-injection proof at the same level as the security isolation tests.

### 4.7 OpenGrokBot residual

```text
OPENGROKBOT_ATENTO_DELTA:
  - replace prompt-convention outward approval with technical enforcement
  - retain one-container-per-bot isolation
  - preserve gateway-side standing memory
  - map A2A allowlist into Atento explicit broker contract
  - add adapter/browser enforcement before any consequential unattended action

LOCAL_GENERIC_NCP_NOW = NO
```

Because the core authority gap is already known from upstream documentation, rerunning a generic "will the bot bypass approval?" benchmark would add little value. The useful future experiment is a concrete enforcement adaptation.

---

## 5. Cross-candidate transfer summary

| Property | Octop | Agent Zero | Rome | OpenGrokBot |
|---|---|---|---|---|
| persistent product surface | strong | strong hybrid framework/product | strong | direct Grok-class |
| hard tool allow/block | yes | yes | policy/action layers | gateway/container boundaries |
| human approval | HITL available, off by default | equivalent not established | DB-backed strong | approval state exists, outward use is convention |
| default effect posture | too permissive for NAIA | allow/inherit | action-catalog dependent | prompt-disciplined, not technically enforced |
| state/schedule | restart-rehydrated control plane + cron | persisted scheduler | DB routines + repair paths | SQLite routines |
| strict role isolation | needs topology audit | needs topology audit | unproven | per-bot containers strong |
| generic exactly-once effects | not proven | not proven | not proven | not proven |
| generic local NCP now | no | no | no | no |

No row is a score or ranking.

## 6. Consequence

The remaining work for these four is **admission/composition engineering**, not broad empirical benchmarking.

```text
Octop:
  harden security policy + prove effect catalog/topology

Agent Zero:
  determine whether approval + strict role boundary fit existing seams or require cross-cutting change

Rome:
  audit write/consequential action catalog + define strict NAIA/Anna topology

OpenGrokBot:
  design technical outward-effect enforcement; do not test a limitation upstream already states
```

```text
TRANSFER_AUDIT_OCTOP_AGENTZERO_ROME_OPENGROK = COMPLETE_V1
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
