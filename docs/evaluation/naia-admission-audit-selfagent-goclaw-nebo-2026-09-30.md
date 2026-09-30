# NAIA admission audit — SelfAgent / GoClaw / Nebo — 2026-09-30

## Contract

This record performs the same-protocol admission/completeness pass for the three previously provisional persistent-agent candidates:

- SelfAgent
- GoClaw
- Nebo

It does not rank, shortlist, qualify, accept, promote or select any candidate.

~~~text
README_FEATURE != ENFORCED_BOUNDARY
PERSISTED_FILE != RESTART_CONTINUITY
PER_AGENT_SESSION != PER_AGENT_MEMORY_AUTHORITY
APPROVAL_MECHANISM != BACKGROUND_APPROVAL_PARITY
UPSTREAM_TEST_SOURCE != CURRENT_PIN_RUNTIME_PASS
~~~

Exact pins:

~~~text
SelfAgent  oezercet/SelfAgent  c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1
GoClaw     sausheong/goclaw   c24c50ba2d16daff6aa2809b6c1a6f592977ae54
Nebo       NeboLoop/nebo-go   d566d27ec7c5ab36f3b95fdfda371bb45994dfd7
~~~

All three pins were checked for observable GitHub workflow runs and combined commit statuses through the available connector.

Observed for each:

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

The source/test findings below are static exact-pin evidence only.

---

## 1. SelfAgent

Repository:
`oezercet/SelfAgent`

Pin:
`c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1`

### 1.1 Product-shape admission

The exact-pin product/source surface is a direct personal-assistant chassis:

- persistent SQLite conversation memory;
- semantic recall through ChromaDB;
- persistent task tracking;
- Playwright browser automation;
- file, terminal, Git, email and system-action tools;
- one-time and recurring scheduling;
- provider switching including Ollama;
- local Web chat;
- plugin loading.

The roadmap explicitly leaves multi-agent collaboration for a future phase.

Classification:

~~~text
PERSISTENT_PERSONAL_ASSISTANT_PRODUCT = YES
BROWSER = PRESENT
SCHEDULER = PRESENT
MESSAGING_EMAIL_EFFECT = PRESENT
PROVIDER_REPLACEABILITY = PRESENT
NATIVE_MULTI_AGENT_ROLE_MODEL = NO
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

Admission does not imply that the current safety claims are technically enforced.

### 1.2 Confirmation metadata is not enforced by the central execution path

The exact-pin base tool class defines:

~~~text
requires_confirmation: bool = False
~~~

and consequential tools such as terminal, file manager, system control, database and email set that flag to true.

However the exact-pin central execution path does not consume it.

`core/agent.py` obtains enabled tool schemas and executes model-selected tools through:

~~~text
self.tools.execute(tc.name, **tc.arguments)
~~~

`tools/registry.py` checks only:

- tool exists;
- tool is not disabled;
- then calls `tool.execute(...)`.

No confirmation branch is present there.

A repository search for `requires_confirmation` finds declarations, but no approval/confirmation consumer.

Therefore:

~~~text
CONFIRMATION_METADATA = PRESENT
CENTRAL_CONFIRMATION_ENFORCEMENT = NOT_WIRED_AT_PIN
README_DESTRUCTIVE_CONFIRMATION_CLAIM = NOT_TRANSFERRED_AS_TECHNICAL_PROOF
~~~

This is decision-relevant because email and shell are consequential external/host effects.

### 1.3 Scheduler persistence does not establish restart continuity

The exact-pin scheduler stores definitions/state in:

~~~text
storage/scheduler.json
~~~

and contains a private `_load()` method.

But the exact-pin startup path in `chat/server.py` registers a fresh:

~~~text
SchedulerTool()
~~~

without calling `_load()`, and no other exact-pin caller of `_load()` was found.

Further, even loading definitions would not by itself recreate the in-process asyncio handles; the source does not expose a restart re-arm pass.

Therefore:

~~~text
SCHEDULE_STATE_FILE = PERSISTED
SCHEDULE_RELOAD_ON_STARTUP = NOT_WIRED
SCHEDULE_REARM_AFTER_RESTART = NOT_ESTABLISHED
SCHEDULE_SURVIVES_RESTART = NO_STATIC_PROOF
~~~

This is a concrete example of:

~~~text
PERSISTED_FILE != RESTART_CONTINUITY
~~~

### 1.4 Scheduled command execution bypasses the ordinary terminal tool boundary

The scheduler accepts a raw `command` and executes it through:

~~~text
asyncio.create_subprocess_shell(command)
~~~

inside `SchedulerTool._exec_command()`.

That path does not call the tool registry, does not consult `requires_confirmation`, and does not reuse the terminal tool's configured blocked-command checks.

Therefore:

~~~text
BACKGROUND_RAW_SHELL = PRESENT
BACKGROUND_USES_TOOL_REGISTRY = NO
BACKGROUND_USES_TERMINAL_BLOCKLIST = NO
BACKGROUND_CONFIRMATION_GATE = NO
BACKGROUND_AUTHORITY_LE_INTERACTIVE_AUTHORITY = NOT_ESTABLISHED
~~~

This is the principal SelfAgent authority gap for NAIA.

### 1.5 Role isolation

SelfAgent is a single-agent product at this pin.

Memory, provider configuration, email configuration, tool registry and scheduler are instantiated as one application context.

A strict NAIA/Anna deployment therefore cannot infer role isolation from the native product.

The smallest composition boundary is separate application/runtime state, including separate storage/configuration.

Classification:

~~~text
NATIVE_NAIA_ANNA_ISOLATION = NO
SEPARATE_RUNTIME_STORE_COMPOSITION = REQUIRED_IF_USED
SILENT_CROSS_ROLE_MEMORY_BY_NATIVE_MULTI_AGENT = NOT_APPLICABLE
~~~

### 1.6 SelfAgent residual

~~~text
SELFAGENT_ATENTO_DELTA:
  - implement a real technical approval/authority gate at or below the registry boundary
  - route scheduled effects through the same-or-narrower authority policy
  - implement restart reload/re-arm semantics before claiming durable scheduled work
  - compose NAIA and Anna as separate runtime/store/config domains
  - audit plugin loading and credential scope under that topology

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 2. GoClaw

Repository:
`sausheong/goclaw`

Pin:
`c24c50ba2d16daff6aa2809b6c1a6f592977ae54`

### 2.1 Product-shape admission

The exact-pin product/runtime includes:

- Telegram, WhatsApp, CLI and Web/tray interfaces;
- multiple named agents;
- persistent sessions;
- persistent memory plus Cortex knowledge graph;
- heartbeat and cron;
- browser automation;
- per-agent workspaces;
- per-agent tool allow/deny lists;
- inter-agent delegation through `ask_agent`;
- multiple model providers;
- Docker/namespace sandbox configuration surfaces.

Classification:

~~~text
PERSISTENT_MULTI_AGENT_ASSISTANT_PRODUCT = YES
MESSAGING_CHANNELS = PRESENT
SCHEDULER_HEARTBEAT = PRESENT
BROWSER = PRESENT
PER_AGENT_TOOL_POLICY = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

### 2.2 Per-agent workspaces and sessions are concrete boundaries

The exact-pin configuration assigns every agent its own workspace.

If an agent omits one, validation derives:

~~~text
~/.goclaw/workspace-<agent-id>
~~~

The session store also keys persisted JSONL sessions under:

~~~text
<session-base>/<agent-id>/<session-key>.jsonl
~~~

This is useful native separation for filesystem-facing context and conversation history.

Classification:

~~~text
WORKSPACE_SCOPE = PER_AGENT
SESSION_SCOPE = PER_AGENT
SESSION_FILE_PERMISSIONS = OWNER_ONLY_BY_SOURCE
~~~

### 2.3 Shell authority defaults are permissive

The exact-pin default agent receives:

~~~text
read_file
write_file
edit_file
bash
web_fetch
web_search
browser
send_message
cron
~~~

The exact-pin global execution policy default is:

~~~text
ExecApprovals.Level = "full"
~~~

The bash tool supports:

- `deny`;
- `allowlist`;
- `full`.

But `full` is the default, and nil/unrecognized policy also allows execution.

Therefore:

~~~text
BASH_POLICY_MECHANISM = PRESENT
DEFAULT_BASH_POLICY = FULL
DEFAULT_AGENT_HAS_BASH = YES
DEFAULT_MATCHES_HARDENED_NAIA = NO
ATENTO_DELTA = DENY_OR_ALLOWLIST_PROFILE_REQUIRED
~~~

### 2.4 Tool policy is per agent and is reapplied to delegated agents

`AgentRunnerImpl.RunAgent()` resolves the target agent configuration, creates a fresh core registry, applies the global shell execution policy, then wraps the registry with the target agent's own allow/deny policy.

The delegated agent does not receive `ask_agent`, preventing recursive delegation.

This is real technical scoping for tool availability.

Classification:

~~~text
TARGET_AGENT_TOOL_POLICY = TECHNICALLY_APPLIED
RECURSIVE_DELEGATION = BLOCKED
DELEGATED_SESSION = SEPARATE
~~~

### 2.5 Delegation reachability is not an NAIA/Anna authorization boundary

The `ask_agent` tool enumerates all configured agents through `AvailableAgents()`.

Execution accepts an arbitrary configured `agent_id` and directly calls the target runner.

No caller-to-target allowlist is present in this exact path.

Therefore, when `ask_agent` is allowed to a role:

~~~text
DELEGATION_TARGET_SCOPE = ALL_CONFIGURED_AGENTS
CALLER_TARGET_ALLOWLIST = NOT_PRESENT_IN_ASK_AGENT_PATH
ONE_LEVEL_ONLY != ROLE_ISOLATION
~~~

For NAIA/Anna, `ask_agent` must be disabled across the boundary or replaced by an explicit broker/handoff policy.

### 2.6 Native memory/Cortex are instance-global, not per-agent

This is the strongest native-isolation limitation.

Gateway/chat startup creates one memory manager at:

~~~text
<data-dir>/memory
~~~

and one Cortex instance.

Those same objects are injected into agent runtimes and delegated runtimes.

Inside `Runtime.Run()`, memory recall calls:

~~~text
r.Memory.Search(userMsg, 3)
~~~

without an `AgentID` namespace.

Cortex recall is also performed through the shared Cortex object without an agent namespace in this execution path.

Therefore:

~~~text
SESSION_SCOPE = PER_AGENT
WORKSPACE_SCOPE = PER_AGENT
BM25_MEMORY_SCOPE = INSTANCE_GLOBAL
CORTEX_SCOPE = INSTANCE_GLOBAL
STRICT_NATIVE_NAIA_ANNA_MEMORY_ISOLATION = NO
~~~

Per-agent sessions must not be mistaken for per-agent memory authority.

### 2.7 GoClaw residual

~~~text
GOCLAW_ATENTO_DELTA:
  - change shell default from full to deny/allowlist
  - freeze an explicit per-agent capability allowlist
  - disable cross-role ask_agent or place delegation behind an explicit broker
  - isolate BM25/Cortex stores by role, or use separate GoClaw runtimes/data directories
  - prove cron/heartbeat use the same-or-narrower role policy if the candidate advances
  - keep channel bindings/credentials role-scoped in the chosen topology

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 3. Nebo

Repository:
`NeboLoop/nebo-go`

Pin:
`d566d27ec7c5ab36f3b95fdfda371bb45994dfd7`

### 3.1 Product-shape admission

Nebo is a direct desktop personal-assistant product with:

- persistent memory and sessions;
- browser automation;
- file and shell capabilities;
- recurring schedules/reminders;
- sub-agent execution;
- app/plugin platform;
- desktop automation;
- multiple providers including local models;
- channel integrations through apps/NeboLoop;
- persisted scheduled and pending work in SQLite according to exact-pin architecture documentation.

Classification:

~~~text
PERSISTENT_PERSONAL_ASSISTANT_PRODUCT = YES
BROWSER_DESKTOP = PRESENT
SCHEDULED_BACKGROUND_WORK = PRESENT
MULTI_PROVIDER = PRESENT
APP_PLATFORM = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

### 3.2 Hard safeguard is implemented and has direct source tests

The exact-pin registry calls `CheckSafeguard()` before invoking the underlying tool.

The safeguard cannot be disabled by normal policy/autonomous settings and blocks classes including:

- sudo/su;
- destructive disk operations;
- root filesystem wipe;
- writes to protected system paths;
- writes to sensitive credential paths;
- writes to Nebo's own DB/data files.

`safeguard_test.go` directly exercises multiple blocked and allowed cases.

Classification:

~~~text
HARD_HOST_SAFEGUARD = IMPLEMENTED
HARD_SAFEGUARD_TEST_SOURCE = PRESENT
AUTONOMOUS_MODE_BYPASSES_HARD_SAFEGUARD = NO_BY_SOURCE
~~~

No current-pin runtime pass is inferred from the test source.

### 3.3 Source/doc drift: origin deny is enabled in code

The exact-pin `SECURITY.md` includes stale text claiming `defaultOriginDenyList()` returns nil.

The exact-pin source does not.

`policy.go` currently constructs hard deny entries:

~~~text
OriginComm  -> shell denied
OriginApp   -> shell denied
OriginSkill -> shell denied
~~~

and `registry.go` checks `IsDeniedForOrigin()` before approval logic.

For this clause, exact source supersedes the stale documentation statement.

Classification:

~~~text
ORIGIN_TAGGING = IMPLEMENTED
COMM_APP_SKILL_SHELL_DENY = IMPLEMENTED_BY_CURRENT_SOURCE
SECURITY_MD_ORIGIN_STATUS = STALE_AT_PIN
~~~

### 3.4 Default interactive approval posture is materially stronger than full-auto

The exact-pin default policy is:

~~~text
Level   = allowlist
AskMode = on-miss
~~~

Safe read/inspection commands are allowlisted, while non-allowlisted operations can require approval when the tool declares `RequiresApproval()`.

Capability permissions can remove whole categories from registration.

Classification:

~~~text
DEFAULT_TOOL_POLICY = ALLOWLIST
DEFAULT_ASK_MODE = ON_MISS
CAPABILITY_REGISTRATION_FILTER = PRESENT
~~~

This is still not a claim that every consequential operation is correctly marked as approval-requiring.

### 3.5 System-origin background work auto-approves

The same exact `policy.go` contains a special rule:

~~~text
if GetOrigin(ctx) == OriginSystem:
    return approved
~~~

with the source comment identifying reminders, heartbeat and recovery as system-origin work.

The origin deny list has no `OriginSystem` restrictions.

The hard safeguard still executes before the underlying effect, but ordinary approval parity does not hold.

Therefore:

~~~text
SYSTEM_ORIGIN_APPROVAL = AUTO_APPROVE
SYSTEM_ORIGIN_SHELL_DENY = NO_DEFAULT_DENY
HARD_SAFEGUARD_STILL_APPLIES = YES
BACKGROUND_AUTHORITY_LE_INTERACTIVE_AUTHORITY = NOT_ESTABLISHED
~~~

This is the principal NAIA background-authority composition delta at the current pin.

### 3.6 One companion context is not a native NAIA/Anna boundary

Nebo is built around one persistent companion.

Its channel model routes owner interactions to the same companion context; sub-agents are execution workers rather than independently isolated persistent personal roles.

Strict NAIA/Anna separation therefore requires separate Nebo runtime/data authority domains or an explicitly proven new partitioning mechanism.

Classification:

~~~text
NATIVE_PERSISTENT_MULTI_ROLE_ISOLATION = NO
SEPARATE_RUNTIME_DATA_DIR_COMPOSITION = REQUIRED_IF_USED
~~~

### 3.7 Open hardening items remain documented

The exact-pin security record also documents unresolved areas including:

- memory prompt-injection risk;
- compaction-summary poisoning;
- browser/web-content sanitization concerns;
- local API authentication audit work;
- sub-agent resource/concurrency limits.

Those are not converted into runtime failures, but they remain current-pin hardening evidence.

### 3.8 Nebo residual

~~~text
NEBO_ATENTO_DELTA:
  - keep hard safeguard and allowlist/on-miss posture intact
  - make scheduled/system-origin authority equal to or narrower than interactive NAIA authority
  - compose NAIA and Anna as separate runtime/data/credential domains
  - retain origin-based restrictions and verify no alternate execution path bypasses registry
  - close decision-critical web/memory prompt-injection gaps if Nebo advances
  - bound sub-agent authority/concurrency for the NAIA profile

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 4. Admission result

All three provisional candidates meet the technical product-shape threshold for the comparable set.

~~~text
SELFAGENT_COMPARABLE_CANDIDATE = YES
GOCLAW_COMPARABLE_CANDIDATE = YES
NEBO_COMPARABLE_CANDIDATE = YES

SELFAGENT_CURRENT_PIN_QUALIFIED = NO
GOCLAW_CURRENT_PIN_QUALIFIED = NO
NEBO_CURRENT_PIN_QUALIFIED = NO
~~~

This admission is not an evaluative ordering.

The most important exact-pin residual boundaries are descriptive:

| Candidate | Native role/data boundary | Current authority issue that remains |
|---|---|---|
| SelfAgent | single runtime/store | confirmation metadata is not enforced; scheduler executes raw shell outside registry |
| GoClaw | per-agent sessions/workspaces, but shared memory/Cortex | shell default is full; delegation can target any configured agent |
| Nebo | one companion/runtime authority domain | system-origin scheduled/recovery work auto-approves ordinary approval requests |

No row is a score or verdict.

---

## 5. Candidate-universe consequence

This audit closes the provisional admission block for:

~~~text
SelfAgent
GoClaw
Nebo
~~~

The discovery record still contains a secondary pool that has not received the same admission screening:

~~~text
supastishn/AutoMate
use-agent-os/agent-os
TBNRFPS01/OpenAgent
truenorth-lj/open-intern
hubos-ai/HubOS
radotsvetkov/engram
holt-os/holt
chinkan/RustFox
~~~

Therefore the universe is not closed yet.

~~~text
PROVISIONAL_SELFAGENT_GOCLAW_NEBO_ADMISSION = COMPLETE
SECONDARY_DISCOVERY_POOL_SCREENING = REQUIRED
CANDIDATE_UNIVERSE_COMPLETE = false
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~

The next block is a bounded secondary-pool admission screen, not a local benchmark.
