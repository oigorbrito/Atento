# NAIA upstream transfer audit — AutoMate / AgentOS / OpenAgentd — 2026-09-30

## Contract

This record maps exact-pin upstream/source evidence from AutoMate, AgentOS and OpenAgentd onto the frozen NAIA capability and authority contract.

It does not rank, shortlist, qualify, accept, promote or select any candidate.

~~~text
SOURCE_CONTRACT != RUNTIME_PASS
CONFIGURABLE_APPROVAL != SAFE_DEFAULT
PERSISTED_SCHEDULE != EXACTLY_ONCE_EXTERNAL_EFFECT
PER_AGENT_PROFILE != STRICT_NAIA_ANNA_ISOLATION
SANDBOX != UNIVERSAL_EFFECT_MEDIATION
~~~

Pins:

~~~text
AutoMate    supastishn/AutoMate    7e197b49135590b0f78c8cd9cd570dfd6764afab
AgentOS     use-agent-os/agent-os  226c906291fc68f3c4517623446bdaec1b48a82d
OpenAgentd  TBNRFPS01/OpenAgent    b2acf236f4e9e6b503281f2364e9915a60158376
~~~

At admission, all three exact pins had no observable GitHub workflow runs or combined statuses through the available connector.

Therefore:

~~~text
CODE_PASS = NOT_CLAIMED
CODE_FAIL = NOT_CLAIMED
HOSTED_EXECUTION = NOT_OBSERVED
~~~

---

## 1. AutoMate

### 1.1 Per-agent state composition is concrete

The exact-pin multi-agent router creates one managed runtime per profile.

For each profile it derives or accepts separate:

- memory directory;
- session directory;
- skills directory;
- model/provider settings;
- channel patterns;
- caller allow-list;
- tool allow/deny policy;
- heartbeat manager;
- scheduler reference.

The default per-agent memory/session paths live under the profile name.

Classification:

~~~text
PER_AGENT_MEMORY_DIRECTORY = PRESENT
PER_AGENT_SESSION_DIRECTORY = PRESENT
PER_AGENT_TOOL_ALLOW_DENY = PRESENT
PER_AGENT_CHANNEL_ROUTING = PRESENT
NATIVE_MULTI_AGENT_COMPOSITION = REAL
~~~

### 1.2 Shared memory is also an explicit product feature

The base config has:

~~~text
memory.sharedDirectory = ~/.automate/shared
~~~

and the agent wires that shared directory into shared-memory tools.

Therefore the per-agent memory directories are not, by themselves, a proof that two roles cannot cross-read shared memory.

~~~text
PRIVATE_AGENT_MEMORY = PRESENT
SHARED_AGENT_MEMORY = PRESENT
STRICT_NAIA_ANNA_MEMORY_ISOLATION = CONFIGURATION_DEPENDENT
~~~

For Atento, the shared-memory tool/path must not silently bridge NAIA and Anna.

### 1.3 Tool allow/deny is enforced; approval is not established at the registry boundary

The exact-pin ToolRegistry technically filters tool definitions and execution through allow/deny policy.

An empty allow list means tools are allowed unless explicitly denied.

The config additionally declares:

~~~text
tools.requireApproval = []
~~~

but exact-pin source search found no execution consumer for this field, and the central ToolRegistry execution path checks allow/deny only before invoking the tool.

Named profile composition also resets:

~~~text
requireApproval: []
~~~

when a per-agent tools block is provided.

Therefore:

~~~text
TECHNICAL_TOOL_ALLOW_DENY = PRESENT
DEFAULT_ALLOWLIST = EMPTY_MEANS_ALLOW_ALL
REQUIRE_APPROVAL_CONFIG = PRESENT
CENTRAL_REQUIRE_APPROVAL_ENFORCEMENT = NOT_ESTABLISHED
DEFAULT_MATCHES_HARDENED_NAIA = NO
~~~

### 1.4 Elevated execution can disable shell safeguards

The bash tool maintains a dangerous-command pattern block while the context is not elevated.

Its exact source returns immediately from the command check when:

~~~text
ctx.elevated = true
~~~

Profiles may declare an elevated default.

Therefore:

~~~text
NON_ELEVATED_SHELL_BLOCKLIST = PRESENT
ELEVATED_BYPASSES_SHELL_PATTERN_GUARD = YES
PROFILE_ELEVATION = AUTHORITY_CRITICAL
~~~

NAIA cannot inherit an elevated profile as a convenience default.

### 1.5 Scheduler restart continuity is directly implemented

The exact-pin Scheduler:

- persists jobs to <cron-dir>/jobs.json;
- loads that file in its constructor;
- starts its timer from the constructor;
- preserves enabled state, lastRun, nextRun and runCount;
- recomputes nextRun for enable/update operations.

The per-agent router constructs the scheduler and routes a firing back through:

~~~text
agent.processMessage(sessionId, job.prompt)
~~~

Therefore:

~~~text
SCHEDULE_DEFINITION_PERSISTENCE = PRESENT
SCHEDULE_RELOAD_ON_CONSTRUCTION = PRESENT
SCHEDULE_TIMER_RESTART = PRESENT
BACKGROUND_AGENT_TURN_PATH = SAME_AGENT_PROCESS_MESSAGE_PATH
~~~

However this still does not prove generic exactly-once external effects. The scheduler records the run state before invoking the asynchronous trigger, and no generic provider reconciliation contract was established here.

~~~text
GENERIC_EXACTLY_ONCE_EXTERNAL_EFFECT = NOT_PROVEN
~~~

### 1.6 AutoMate residual

~~~text
AUTOMATE_ATENTO_DELTA:
  - freeze explicit deny-by-default tool allowlist
  - implement/prove a technical consequential-action approval gate
  - disable or tightly bound elevated profile execution
  - exclude shared-memory authority across NAIA/Anna
  - prove cron/heartbeat cannot silently broaden authority
  - audit role-specific credentials and channels
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 2. AgentOS

### 2.1 Persistent/scheduled chassis is mature and source-backed

The exact-pin product has:

- persistent workspace memory;
- SQLite-backed scheduler JobStore;
- structured cron/every/at schedules;
- explicit cron execution records/state;
- channels;
- browser automation;
- skills/MCP;
- multiple providers;
- approval/elevation controls;
- sandbox levels.

The scheduler source stores CronJob records in SQLite and the operations layer validates and persists schedule, session target, payload, delivery and tool policy.

Classification:

~~~text
PERSISTENT_MEMORY = PRESENT
SCHEDULER_SQLITE_STORE = PRESENT
STRUCTURED_SCHEDULE_POLICY = PRESENT
MESSAGING_CHANNELS = PRESENT
BROWSER = PRESENT
APPROVAL_AND_SANDBOX_SURFACES = PRESENT
~~~

### 2.2 Interactive permission default is bypass

The exact-pin config schema and shipped example state:

~~~text
permissions.default_mode = bypass
~~~

The product describes bypass as host execution with approvals auto-granted while hard/sensitive-path protections remain.

Therefore:

~~~text
APPROVAL_MECHANISM = PRESENT
INTERACTIVE_DEFAULT_PERMISSION = BYPASS
DEFAULT_INTERACTIVE_APPROVAL = AUTO_GRANTED
DEFAULT_MATCHES_HARDENED_NAIA = NO
~~~

This is a configuration delta, not absence of a permission system.

### 2.3 Unattended cron default is also bypass

The exact-pin source function configured_cron_default_elevated returns bypass when the permission config is absent and defaults cron_default_mode to bypass.

Current docs and a dedicated scheduler test surface confirm that agent-turn cron jobs run elevated under bypass by default.

The docs explicitly state that such a job can run shell-based skills unattended with no approval prompt.

Other job kinds such as reminders/script runs do not inherit agent-turn elevation.

Classification:

~~~text
CRON_AGENT_TURN_DEFAULT = BYPASS
CRON_AGENT_TURN_UNATTENDED_SHELL = AVAILABLE_BY_DEFAULT
BACKGROUND_AUTHORITY_LE_INTERACTIVE_AUTHORITY = NOT_SATISFIED_BY_HARDENED_NAIA_DEFAULT
PER_JOB_NO_ELEVATED_OVERRIDE = AVAILABLE
~~~

This is a first-order NAIA hardening delta.

### 2.4 Cron has useful policy boundaries that should be reused

Exact source/docs also show controls that should not be discarded:

- cron elevation is accepted only for agent-turn handlers;
- non-operator callers cannot explicitly request elevated tool policy;
- cron callers cannot revive force-denied private-memory reads;
- cron jobs cannot use the cron tool to recursively schedule/elevate another job in the documented hardened path;
- per-job elevation can be explicitly disabled.

Therefore:

~~~text
CRON_POLICY_PRIMITIVES = STRONG
DEFAULT_CRON_POSTURE = TOO_PERMISSIVE_FOR_NAIA
REWRITE_SCHEDULER = NOT_JUSTIFIED
HARDEN_CONFIGURATION_FIRST = YES
~~~

### 2.5 Browser is outside the process sandbox

The exact-pin configuration documentation says the browser engine runs outside the ordinary process sandbox because Chromium cannot run inside the selected sandbox backends.

AgentOS instead applies browser-specific controls such as:

- SSRF guards;
- redirect revalidation;
- optional domain allowlist;
- local-only CDP attach plus explicit confirmation;
- environment minimization;
- credential-shaped typing restrictions and transcript redaction in upstream hardening notes.

Therefore:

~~~text
PROCESS_SANDBOX_COVERS_BROWSER = NO
BROWSER_POLICY_LAYER = SEPARATE
BROWSER_HARDENING = MUST_BE_FROZEN_WITH_NAIA_PROFILE
~~~

### 2.6 AgentOS residual

~~~text
AGENTOS_ATENTO_DELTA:
  - change interactive default_mode away from bypass
  - change cron_default_mode away from bypass
  - use the narrowest tool profile that can complete each unattended task
  - freeze browser-specific policy together with process sandbox policy
  - prove NAIA/Anna memory, credential and channel authority separation
  - reuse scheduler/security upstream tests rather than rerunning broad suites
  - run only a later composition delta if source cannot close it

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 3. OpenAgentd

### 3.1 Product surface is broad enough, but the trust model is explicit

The exact-pin canonical feature catalogue records:

- native desktop/server product;
- durable sessions;
- lead/member agent teams;
- editable persistent memory plus Dream consolidation;
- schedule_task;
- filesystem/shell/web search/fetch;
- 15 providers;
- MCP/plugins/skills;
- allow/deny/ask permission rules;
- observability and reconnect-safe streaming.

Classification:

~~~text
PERSISTENT_AGENT_PRODUCT = YES
MULTI_AGENT_TEAM = PRESENT
PERSISTENT_MEMORY = PRESENT
SCHEDULE_TASK = PRESENT
PERMISSION_RULES = PRESENT
PROVIDER_REPLACEABILITY = STRONG
~~~

### 3.2 Default permission service auto-allows every tool call

The exact-pin sandbox/permissions documentation distinguishes:

- AutoAllowPermissionService
- blocking PermissionService

It explicitly states:

~~~text
AutoAllowPermissionService = Default
~~~

and that this implementation emits permission_asked events for observability but does not block.

The blocking service can apply wildcard last-match-wins rules and wait for a user reply.

Therefore:

~~~text
ALLOW_DENY_ASK_ENGINE = PRESENT
DEFAULT_PERMISSION_SERVICE = AUTO_ALLOW
PERMISSION_ASK_EVENT != BLOCKING_APPROVAL
DEFAULT_MATCHES_HARDENED_NAIA = NO
~~~

### 3.3 Shell safety inherits a trusted-host model

The exact-pin sandbox is a denylist, not a workdir-only security boundary.

The docs state:

- absolute paths are accepted unless under denied roots or user patterns;
- shell path scanning is best effort;
- the old shell dangerous-command denylist was removed in favor of the permission system;
- the overall model is single-user and the host is trusted.

Therefore:

~~~text
HOST_TRUST_MODEL = SINGLE_USER_TRUSTED_HOST
FILESYSTEM_BOUNDARY = DENYLIST
SHELL_PATH_SCAN = BEST_EFFORT
DEFAULT_AUTO_ALLOW + TRUSTED_HOST = NOT_HARDENED_NAIA
~~~

A hardened NAIA profile must not combine AutoAllow with the assumption that prompt/tool behavior is fully trusted.

### 3.4 Lead/member collaboration is not a strict NAIA/Anna authority boundary

Team members install their own sandbox context during activation and can have per-agent tool/MCP configuration.

But the product is designed as one collaborating team, with:

- one lead driving conversation;
- member spawning;
- team_message;
- unified team view;
- shared durable user/wiki memory surfaces.

Therefore:

~~~text
MULTI_AGENT_COLLABORATION = STRONG
STRICT_NATIVE_ROLE_ISOLATION = NOT_ESTABLISHED
LEAD_MEMBER_TOPOLOGY != NAIA_ANNA_SECURITY_BOUNDARY
~~~

For Atento, NAIA and Anna should not be represented merely as two cooperating members in one team.

### 3.5 Browser requirement is a composition delta at this pin

The exact-pin built-in Web tools are web_search and web_fetch.

The canonical feature catalogue does not list a built-in interactive browser automation tool for this pin.

Therefore:

~~~text
BUILTIN_WEB_SEARCH_FETCH = PRESENT
BUILTIN_INTERACTIVE_BROWSER = NOT_ESTABLISHED_AT_PIN
NAIA_BROWSER_ACTION = COMPOSITION_DELTA
~~~

This should be counted in adaptation cost rather than silently treated as native.

### 3.6 OpenAgentd residual

~~~text
OPENAGENTD_ATENTO_DELTA:
  - replace default AutoAllow with a blocking deny/ask/allow NAIA ruleset
  - harden the trusted-host / denylist shell posture
  - compose NAIA and Anna in separate authority domains, not one lead/member team
  - add/freeze a browser action path if required by the NAIA target
  - audit per-role MCP/provider credentials and channel authority
  - verify scheduled work uses the same-or-narrower permission policy
  - measure browser/isolation composition as migration cost

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 4. Transfer summary

| Property | AutoMate | AgentOS | OpenAgentd |
|---|---|---|---|
| persistent state | per-agent memory/session dirs + shared memory option | workspace memory + persistent scheduler/state | durable sessions + wiki/Dream memory |
| scheduled work | jobs.json reload + per-agent scheduler | SQLite JobStore + cron policy | schedule_task surface |
| tool policy | per-agent allow/deny | profiles + permission/elevation modes | allow/deny/ask rules |
| default authority | allow-all unless constrained; approval not established | interactive bypass; cron bypass | AutoAllowPermissionService |
| strict NAIA/Anna native boundary | not automatic because shared memory exists | requires explicit topology proof | lead/member team is collaborative, not isolation |
| browser | native | native, outside process sandbox | interactive browser not established as built-in |
| current-pin hosted runtime | not observed | not observed | not observed |

No row is a score, rank or verdict.

---

## 5. Consequence for local NCP

These three candidates already expose enough exact upstream/source contract to avoid generic local benchmarking.

The next evidence should stay candidate-specific and upstream-first:

~~~text
AutoMate:
  locate approval/authority tests or confirm absence
  + map shared-memory and cron policy tests
  + only later test frozen hardened composition

AgentOS:
  reuse permission/cron/browser/sandbox hardening tests
  + map exact NAIA hardened config
  + only later test any topology delta not closed by source

OpenAgentd:
  map blocking PermissionService + scheduled-task path
  + map per-agent MCP/tool credential surfaces
  + measure browser and strict-role composition cost
~~~

State:

~~~text
TRANSFER_AUDIT_AUTOMATE_AGENTOS_OPENAGENTD = COMPLETE_V1
CURRENT_PIN_QUALIFIED = 0
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~
