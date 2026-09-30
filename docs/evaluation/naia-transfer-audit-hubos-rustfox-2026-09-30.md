# NAIA upstream transfer audit — HubOS / RustFox — 2026-09-30

## Contract

This record maps exact-pin upstream/source evidence from HubOS and RustFox onto the frozen NAIA capability, authority and isolation contract.

It does not rank, shortlist, qualify, accept, promote or select any candidate.

~~~text
SOURCE_CONTRACT != RUNTIME_PASS
INTERACTIVE_APPROVAL != BACKGROUND_APPROVAL
RISK_CLASSIFICATION != UNIVERSAL_EFFECT_GATE
PERSISTED_SCHEDULE != EXACTLY_ONCE_EXTERNAL_EFFECT
MULTI_AGENT_CONTEXT_SEPARATION != STRICT_ROLE_AUTHORITY_ISOLATION
AUDIT_OR_RETRY != DUPLICATE_EFFECT_PREVENTION
~~~

Pins:

~~~text
HubOS    hubos-ai/HubOS    7c14b14ed1d26c3d1b597cc213cf97ddfbb7cdcb
RustFox  chinkan/RustFox   6e24388d36d1c6fac399039d8cab07cd9cb8264b
~~~

At admission, both exact pins had:

~~~text
workflow_runs = []
combined_statuses = []
~~~

Therefore:

~~~text
CODE_PASS = NOT_CLAIMED
CODE_FAIL = NOT_CLAIMED
HOSTED_EXECUTION = NOT_OBSERVED
~~~

---

## 1. HubOS

### 1.1 Persistent multi-agent product surface is real

The exact-pin product/runtime exposes:

- per-agent profile configuration;
- per-agent workspace references;
- per-agent model, channel, MCP, heartbeat, tool and security configuration;
- persistent memory managers;
- native browser automation;
- multi-agent fan-out, DAG workflow and background delegation;
- many messaging channels;
- agent instance pooling with explicit session-memory reset on reuse.

The runner also avoids reusing one borrowed pooled instance concurrently; it creates a temporary agent to prevent cross-session memory contamination.

Classification:

~~~text
PERSISTENT_MULTI_AGENT_PRODUCT = YES
PER_AGENT_WORKSPACE_REF = PRESENT
PER_AGENT_CHANNEL/MCP/TOOLS/SECURITY_CONFIG = PRESENT
NATIVE_BROWSER = PRESENT
MULTI_AGENT_ORCHESTRATION = PRESENT
POOL_CONCURRENT_SESSION_MEMORY_REUSE = GUARDED
~~~

This is a useful composition substrate, not proof of strict NAIA/Anna authority isolation.

### 1.2 Tool Guard is a real pre-execution enforcement path

HubOS does not rely only on a README security claim.

The exact-pin HubOSAgent MRO is:

~~~text
HubOSAgent -> ToolGuardMixin -> ReActAgent
~~~

and the mixin intercepts _acting before the parent tool execution path.

The exact source implements:

1. unconditionally denied tools;
2. guarded-tool evaluation;
3. always-run file-path guarding even outside the ordinary guard scope;
4. pending approval creation;
5. exact approved tool-call replay;
6. session/tool/parameter-bound one-shot approval consumption;
7. timeout denial;
8. FIFO pending approval handling in the runner.

The guard engine defaults enabled when config cannot be loaded, and the sensitive-file guardian defaults to protecting the HubOS secret directory.

Classification:

~~~text
PRE_TOOL_EXECUTION_GUARD = TECHNICAL
DENIED_TOOL_AUTO_DENY = PRESENT
SENSITIVE_FILE_GUARD_ALWAYS_RUN = PRESENT
GUARD_ENGINE_FALLBACK_DEFAULT = ENABLED
APPROVAL_REPLAY = STORED_TOOL_CALL
PREAPPROVAL_SCOPE = SESSION + TOOL + PARAMETERS
APPROVAL_TIMEOUT = FAILS_CLOSED
INTERACTIVE_TOOL_APPROVAL = STRONG_STATIC_CONTRACT
~~~

Equivalent local tests for ordinary interactive approval mechanics are not justified if the mechanism is unchanged.

### 1.3 Guard findings require an approval-capable session

The exact mixin creates a pending approval only when:

~~~text
request_context.session_id is present
~~~

If a guarded tool produces findings but no session id is available, the approval branch is not entered and the call may fall through to the underlying execution path unless the tool itself is in the unconditional denied set.

This matters for unattended/background execution.

Therefore:

~~~text
INTERACTIVE_SESSION_GUARD = STRONG
HEADLESS_OR_BACKGROUND_WITHOUT_SESSION_ID = NOT_ESTABLISHED_FAIL_CLOSED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY = NOT_PROVEN
~~~

The NAIA deployment must not assume the interactive approval UI automatically protects every cron/heartbeat/delegated path.

### 1.4 Guard evaluation exceptions are explicitly non-blocking

The exact _acting override catches errors while deciding the guard action and logs:

~~~text
Tool guard check error (non-blocking)
~~~

It then falls through to normal execution.

Therefore:

~~~text
GUARD_ENGINE_EXCEPTION_POLICY = FAIL_OPEN_FOR_NON_DENIED_TOOLS
DEFAULT_MATCHES_HARDENED_NAIA = NO
~~~

This is a material hardening delta. NAIA requires failure of the authority-control layer to reduce or deny authority, not silently restore ordinary execution.

### 1.5 Guard scope is risk-detection based, not universal approval

The rule-based guardian ships a bounded default ruleset centered on dangerous shell commands, while the file-path guardian always runs.

For a guarded tool, approval is requested when findings exist. A tool call with no finding is allowed through.

Therefore:

~~~text
TOOL_GUARD_PRESENT != REQUIRE_APPROVAL_FOR_ALL_CONSEQUENTIAL_ACTIONS
CONSEQUENTIAL_EFFECT_POLICY = REQUIRES_EXPLICIT_NAIA_PROFILE
~~~

This is especially relevant for browser/send/integration operations that may be consequential without matching a dangerous-shell or sensitive-file signature.

### 1.6 Tool and channel defaults need explicit tightening

The exact agent construction path enables a built-in tool by default when the tool is absent from the per-agent tool configuration, for backward compatibility.

The base channel configuration defaults direct-message and group policies to:

~~~text
open
~~~

unless overridden.

Therefore:

~~~text
UNMENTIONED_BUILTIN_TOOL_DEFAULT = ENABLED
CHANNEL_DM_DEFAULT = OPEN
CHANNEL_GROUP_DEFAULT = OPEN
DEFAULT_MATCHES_LEAST_PRIVILEGE_NAIA = NO
~~~

A frozen NAIA profile should enumerate tools and channel callers explicitly rather than inherit these convenience defaults.

### 1.7 Native multi-agent collaboration is not the Atento broker

HubOS intentionally supports:

- general-manager dispatch;
- sub-agent spawning;
- DAG coordination;
- background delegation;
- one team serving many channels.

This is useful functionality, but it is broader than the Atento rule:

~~~text
NAIA <-> Anna = explicit handoff only
~~~

Agent profiles may have separate workspaces and configuration, yet the orchestration layer is designed to connect agents.

Therefore:

~~~text
NATIVE_AGENT_COLLABORATION = STRONG
STRICT_NAIA_ANNA_BROKER_ONLY_BOUNDARY = NOT_NATIVE_BY_DEFAULT
~~~

The hardened composition must prevent the general dispatcher, spawn/delegate tools, shared channel routing or shared credentials from silently crossing the role boundary.

### 1.8 HubOS residual

~~~text
HUBOS_ATENTO_DELTA:
  - make guard failures fail closed
  - ensure every unattended/background path carries an enforceable authority context
  - define consequential actions that require technical approval even without regex findings
  - use explicit tool allowlists rather than enable-by-absence
  - tighten channel policies from open to role-specific allowlists
  - prevent native dispatcher/subagent tools from silently bridging NAIA and Anna
  - prove credential and durable-memory separation for the chosen topology
  - map cron/heartbeat/delegated execution to the same-or-narrower authority
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 2. RustFox

### 2.1 Persistent assistant and scheduler continuity are source-backed

The exact pin exposes:

- SQLite persistent conversation/memory state;
- vector/RAG retrieval;
- persistent scheduled tasks;
- one-shot and recurring schedules;
- Telegram;
- subagents and multi-bot personas;
- sandboxed file/command operations;
- MCP;
- provider replaceability;
- a supervisor with persisted task state.

The agent has an explicit startup method:

~~~text
restore_scheduled_tasks()
~~~

which reads active task rows from the persistent task store and re-registers them with the scheduler. The main startup path calls it.

Classification:

~~~text
PERSISTENT_ASSISTANT_PRODUCT = YES
SCHEDULE_DB_PERSISTENCE = PRESENT
SCHEDULE_RESTORE_AT_STARTUP = PRESENT
PERSISTENT_SUPERVISOR_STATE = PRESENT
~~~

This closes generic schedule-definition continuity. It does not establish exactly-once external effects.

### 2.2 Supervisor high-risk approval is real and tested

The exact-pin supervisor policy returns:

~~~text
RequireApproval
~~~

for High-risk tasks.

Source tests directly cover that high-risk work requires approval.

The thresholds can also be tightened so Medium/Low tasks require approval.

Classification:

~~~text
SUPERVISOR_HIGH_RISK_APPROVAL = TECHNICAL
SUPERVISOR_POLICY_TEST_SOURCE = PRESENT
RISK_THRESHOLDS = CONFIGURABLE
~~~

### 2.3 Medium-risk work auto-executes under the source default

The source-level default is derived from false-valued boolean thresholds, and the policy test explicitly verifies that Medium-risk work preserves auto-execution by default.

Therefore:

~~~text
HIGH_RISK_DEFAULT = REQUIRE_APPROVAL
MEDIUM_RISK_DEFAULT = AUTO_EXECUTE
LOW_RISK_WELL_SCOPED_DEFAULT = AUTO_EXECUTE
DEFAULT_MATCHES_HARDENED_NAIA = NO_FOR_ALL_CONSEQUENTIAL_EFFECTS
~~~

The NAIA contract cannot equate “not classified High” with permission to execute any consequential external effect unattended.

### 2.4 Supervisor approval is not yet a universal raw-tool gate

RustFox has both:

- a task supervisor/policy layer;
- ordinary agent tool execution surfaces.

The evidence above proves the supervisor’s task gate. It does not establish that every direct command, MCP, browser-like adapter, message send or other raw effect is necessarily submitted through that supervisor first.

Therefore:

~~~text
SUPERVISOR_APPROVAL = STRONG_FOR_SUPERVISED_TASKS
UNIVERSAL_TOOL_EFFECT_MEDIATION = NOT_ESTABLISHED
~~~

The Atento mapping must identify the actual execution owner for each consequential NAIA capability rather than assume the supervisor governs all paths.

### 2.5 Sandbox and secret bridge are concrete useful mechanisms

The exact-pin file/command tools resolve paths through the configured sandbox root.

The secret-store bridge provides named secret lookup/injection and remembers values for redaction. Command-tool tests verify secret environment injection while allowing the result to be redacted.

Classification:

~~~text
FILE_COMMAND_SANDBOX_CONTAINMENT = PRESENT
NAMED_SECRET_BRIDGE = PRESENT
SECRET_ENV_INJECTION = TEST_SOURCE_PRESENT
SECRET_RESULT_REDACTION = TEST_SOURCE_PRESENT
~~~

This is useful reusable evidence.

It does not by itself prove per-role credential isolation in a multi-bot NAIA/Anna composition.

### 2.6 Multi-bot context isolation is partial by design

RustFox supports per-bot:

- Telegram identity/routing;
- persona;
- model override;
- tool whitelist;
- conversation context.

However its exact README and agent source explicitly state:

~~~text
USER.md stays shared under RUSTFOX_HOME
~~~

The multi-agent tools may target another persona/bot, with bounded peer depth/cycle detection.

Therefore:

~~~text
PER_BOT_CONVERSATION_CONTEXT = PRESENT
PER_BOT_TOOL_WHITELIST = PRESENT
INSTALL_WIDE_USER_MEMORY = SHARED
PEER_AGENT_INVOCATION = PRESENT
STRICT_NAIA_ANNA_MEMORY_ISOLATION = NO_IN_ONE_DEFAULT_INSTALL
~~~

Strict Atento composition requires separate memory authority domains and explicit cross-role handoff control.

### 2.7 Dead-letter recovery explicitly allows duplicate-effect risk

RustFox has unusually explicit documentation around scheduled-task failures.

Its dead-letter rerun design uses a two-strike model:

- a transient failure may be auto re-fired once;
- another failure requires user intervention.

The ADR explicitly states the rerun is a full replay and may duplicate a side effect if the prior run published successfully before failing.

This is valuable evidence because it avoids an exactly-once overclaim.

Classification:

~~~text
DEAD_LETTER_RERUN = PRESENT
BLIND_INFINITE_RETRY = NO
FIRST_TRANSIENT_RERUN = AUTOMATIC_ONCE
FULL_REPLAY_DUPLICATE_EFFECT_RISK = EXPLICIT
GENERIC_EXACTLY_ONCE_EXTERNAL_EFFECT = NO
~~~

For consequential NAIA jobs, an adapter-specific idempotency/reconciliation contract is needed before automatic replay is accepted.

### 2.8 RustFox residual

~~~text
RUSTFOX_ATENTO_DELTA:
  - require technical approval by effect class, not only supervisor risk classification
  - prove all consequential execution paths are mediated by the intended authority owner
  - tighten Medium-risk/default auto-execution where effects are consequential
  - separate NAIA and Anna durable USER/memory authority
  - restrict invoke_agent/spawn_agents to the explicit Atento broker boundary
  - prove role-specific SecretStore grants rather than install-wide availability
  - map scheduled-task tool authority to the hardened interactive policy
  - replace/restrict automatic full replay for non-idempotent external effects
  - freeze the concrete browser/web-action path if required

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 3. Transfer summary

| Property | HubOS | RustFox |
|---|---|---|
| persistent agent state | per-agent workspace/config + persistent memory surfaces | SQLite memory/conversation + persona state |
| scheduled/background work | heartbeat/delegation/cron product surfaces | persisted schedules + startup restore |
| interactive authority | technical pre-tool guard + exact approval replay | supervisor high-risk approval |
| default authority caveat | tools/channels permissive; findings without session may fall through; guard errors non-blocking | Medium/Low normally auto-execute; supervisor not proven universal tool gate |
| browser/web action | native browser tool | concrete final browser path still requires composition mapping |
| credentials | per-agent/MCP config surface; role-isolation proof pending | SecretBridge injection/redaction; per-role scope proof pending |
| strict NAIA/Anna isolation | collaboration topology must be constrained | USER.md shared and peer invocation present in one install |
| restart schedule continuity | background mechanism still needs exact authority mapping | startup schedule restore present |
| generic exactly-once effect | not established | explicitly not provided by dead-letter full replay |
| exact-pin hosted runtime | not observed | not observed |

No row is a score, rank or verdict.

---

## 4. Consequence for local NCP

HubOS and RustFox both have enough exact source evidence to avoid a generic local benchmark now.

Future work should stay limited to the residual authority/composition seams.

Do not rerun:

- HubOS ordinary interactive pending-approval mechanics merely to duplicate its exact pre-tool guard flow;
- HubOS sensitive-file guard behavior merely to show the source path exists;
- RustFox schedule-definition restart restoration merely to duplicate the exact startup wiring;
- RustFox supervisor High-risk policy unit behavior;
- RustFox SecretBridge injection/redaction source tests.

Remaining external-evidence group after this audit:

~~~text
Engram
Holt
~~~

State:

~~~text
TRANSFER_AUDIT_HUBOS_RUSTFOX = COMPLETE_V1
SECONDARY_TRANSFER_AUDITS = IN_PROGRESS_5_OF_7
CURRENT_PIN_QUALIFIED = 0
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~
