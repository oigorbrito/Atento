# NAIA secondary discovery-pool admission screen — 2026-09-30

## Contract

This record performs the bounded same-protocol admission screen for the remaining named secondary discovery pool.

It does not rank, shortlist, qualify, accept, promote or select a NAIA base.

~~~text
README_FEATURE != ENFORCED_BOUNDARY
ADMISSION != QUALIFICATION
SOURCE_CONTRACT != RUNTIME_PASS
SCHEDULED_SURFACE != RESTART_SAFE_EFFECT
MULTI_AGENT != STRICT_ROLE_ISOLATION
AVAILABLE_APPROVAL != SAFE_DEFAULT
~~~

Exact pins:

~~~text
AutoMate     supastishn/AutoMate       7e197b49135590b0f78c8cd9cd570dfd6764afab
AgentOS      use-agent-os/agent-os     226c906291fc68f3c4517623446bdaec1b48a82d
OpenAgentd   TBNRFPS01/OpenAgent       b2acf236f4e9e6b503281f2364e9915a60158376
Open Intern  truenorth-lj/open-intern  e2d9dc312a1a07a304c55d88a92c1f0b86cd68c9
HubOS        hubos-ai/HubOS             7c14b14ed1d26c3d1b597cc213cf97ddfbb7cdcb
Engram       radotsvetkov/engram       3a43667deec4a680b42f3e880d7d6bac3baf0746
Holt         holt-os/holt              3a9cb8b0fd62e0b61e5e600a3fa341bd5b03e65e
RustFox      chinkan/RustFox           6e24388d36d1c6fac399039d8cab07cd9cb8264b
~~~

For all eight exact pins, the available GitHub connector returned:

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

Admission below is based on exact-pin product/source evidence only.

---

## 1. AutoMate

Repository:
supastishn/AutoMate

Pin:
7e197b49135590b0f78c8cd9cd570dfd6764afab

### Product shape

The exact-pin product includes:

- browser automation;
- shell/file/web tools;
- cron and heartbeat;
- background processes;
- persistent memory;
- Discord/Web/CLI surfaces;
- multiple agent profiles;
- provider abstraction;
- plugins.

The source-level multi-agent router constructs separate memory and session managers per agent profile and derives per-agent default paths.

Classification:

~~~text
PERSISTENT_PERSONAL_AGENT_PRODUCT = YES
MULTI_AGENT_RUNTIME = PRESENT
PER_AGENT_MEMORY_DIR = PRESENT
PER_AGENT_SESSION_DIR = PRESENT
BROWSER = PRESENT
CRON_HEARTBEAT = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

### Authority / isolation caveats

The exact-pin config defaults are materially permissive:

~~~text
tools.allow = []
tools.deny = []
tools.requireApproval = []
~~~

where an empty allow list means allow-all.

Named agent profiles may also carry an elevated flag. The bash tool skips its dangerous-command checks when the execution context is elevated.

The multi-agent config additionally defines a shared memory directory. Therefore per-agent memory directories are useful building blocks, but the existence of a shared memory facility means strict NAIA/Anna isolation still requires a frozen topology that does not silently expose that shared store.

Residual:

~~~text
AUTOMATE_ATENTO_DELTA:
  - deny-by-default tool profile
  - explicit consequential-action approval policy
  - elevated mode disabled or tightly bounded
  - shared-memory path excluded across NAIA/Anna
  - cron/heartbeat authority proven same-or-narrower than interactive authority
  - credential/channel scope audited per role
~~~

No generic local NCP is justified before a transfer audit maps these exact source paths.

---

## 2. AgentOS

Repository:
use-agent-os/agent-os

Pin:
226c906291fc68f3c4517623446bdaec1b48a82d

### Product shape

The exact-pin product surface includes:

- persistent local memory;
- cron and channels;
- desktop/Web/CLI interfaces;
- browser automation;
- multi-provider routing;
- sandbox configuration;
- approval/elevation mechanics;
- skills and MCP;
- extensive current hardening/release evidence.

Classification:

~~~text
PERSISTENT_AGENT_PRODUCT = YES
MEMORY = PRESENT
CRON = PRESENT
MESSAGING_CHANNELS = PRESENT
BROWSER = PRESENT
SANDBOX_POLICY = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

### Authority caveat

The exact-pin configuration documentation explicitly states:

~~~text
interactive default permission mode = bypass
cron_default_mode = bypass
~~~

The bundled skill/config docs describe bypass as host execution with approvals auto-granted while sensitive-path blocks remain active.

The browser also runs outside the ordinary process sandbox, with AgentOS-owned browser policy controls handling SSRF/domain restrictions.

Therefore:

~~~text
APPROVAL_MECHANISM = PRESENT
INTERACTIVE_DEFAULT = BYPASS
CRON_DEFAULT = BYPASS
DEFAULT_MATCHES_HARDENED_NAIA = NO
BROWSER_OUTSIDE_PROCESS_SANDBOX = YES
~~~

Residual:

~~~text
AGENTOS_ATENTO_DELTA:
  - freeze interactive and cron modes away from bypass
  - prove cron authority <= interactive authority
  - freeze sandbox/browser policy together rather than assuming sandbox covers browser
  - prove NAIA/Anna memory/credential/channel separation topology
  - reuse upstream hardening evidence instead of rerunning broad security suites
~~~

---

## 3. OpenAgentd

Repository:
TBNRFPS01/OpenAgent

Pin:
b2acf236f4e9e6b503281f2364e9915a60158376

### Product shape

The exact-pin canonical feature catalogue records:

- native desktop cockpit;
- persistent sessions;
- lead + member agent teams;
- background/dream memory consolidation;
- durable editable memory;
- 15 provider integrations;
- filesystem/shell/web tools;
- schedule_task;
- permission rules with allow / deny / ask;
- skills, plugins and MCP;
- observability and reconnect-safe streaming.

Classification:

~~~text
PERSISTENT_DESKTOP_AGENT_PRODUCT = YES
MULTI_AGENT_TEAM_RUNTIME = PRESENT
PERSISTENT_MEMORY = PRESENT
SCHEDULE_TASK = PRESENT
WEB_SEARCH_FETCH = PRESENT
PERMISSION_ALLOW_DENY_ASK = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

### Boundary caveats

The exact-pin sandbox documentation is explicit that the model is single-user and the host is trusted.

Its built-in web surface is search/fetch; full browser automation is not part of the built-in feature catalogue at this pin.

Lead/member agents are collaboration roles, not automatically independent security principals.

Residual:

~~~text
OPENAGENTD_ATENTO_DELTA:
  - strict NAIA/Anna role isolation cannot be inferred from lead/member topology
  - browser action capability requires explicit composition if needed
  - permission ask/allow/deny policy must be frozen for unattended scheduling
  - host-trust assumptions must be reconciled with the NAIA hardening profile
  - role-specific credentials and MCP grants require explicit isolation proof
~~~

---

## 4. Open Intern

Repository:
truenorth-lj/open-intern

Pin:
e2d9dc312a1a07a304c55d88a92c1f0b86cd68c9

### Product shape present

The exact-pin product already exposes:

- multiple managed agents;
- PostgreSQL/pgvector persistent memory;
- shared/channel/personal memory layers;
- Lark/Discord/Slack adapters;
- sandbox-oriented execution architecture;
- safety middleware / permission classification;
- multiple model providers;
- Web dashboard.

However the same exact-pin README marks the following as not yet shipped:

~~~text
Proactive Heartbeat
Human Approval Workflow
Multi-Agent Coordination
Browser Automation
~~~

The product-design narrative describes these capabilities, but the explicit feature-status table does not claim them as implemented.

Classification:

~~~text
PERSISTENT_TEAM_AGENT_PLATFORM = PRESENT
PERSISTENT_MEMORY = PRESENT
MESSAGING_CHANNELS = PRESENT
SANDBOX_ARCHITECTURE = PRESENT
REQUIRED_BACKGROUND_WAKEUP = NOT_SHIPPED_AT_PIN
REQUIRED_BROWSER_AUTOMATION = NOT_SHIPPED_AT_PIN
HUMAN_APPROVAL_WORKFLOW = NOT_SHIPPED_AT_PIN
COMPARABLE_CANDIDATE = DEFERRED_AT_CURRENT_PIN
CURRENT_PIN_QUALIFIED = NO
~~~

This is not a negative quality verdict. It is an admission-boundary statement: the current pin does not yet expose enough of the frozen NAIA capability profile to justify the same full transfer-audit protocol as candidates that already implement those surfaces.

Re-admission trigger:

~~~text
OPEN_INTERN_READMISSION =
  material upstream release that ships background/proactive execution
  + browser/web action surface
  + effective approval workflow
~~~

---

## 5. HubOS

Repository:
hubos-ai/HubOS

Pin:
7c14b14ed1d26c3d1b597cc213cf97ddfbb7cdcb

### Product shape

The exact-pin product surface describes:

- multiple persistent agents with identity, skills, memory and responsibilities;
- independent workspaces/sessions/memory;
- 14+ channel integrations;
- browser automation and Web/search tools;
- email;
- cron scheduling;
- per-agent model configuration;
- Tool Guard with risk levels and human approval;
- RBAC/JWT;
- multi-agent orchestration.

Classification:

~~~text
PERSISTENT_MULTI_AGENT_PRODUCT = YES
MULTI_CHANNEL = YES
PERSISTENT_MEMORY = PRESENT
BROWSER = PRESENT
CRON = PRESENT
TOOL_GUARD_SURFACE = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

Admission does not transfer README security claims as runtime proof.

Residual before any local work:

~~~text
HUBOS_NEXT_EVIDENCE:
  - map Tool Guard enforcement point and defaults
  - map per-agent memory/workspace isolation to technical source/tests
  - map cron/background authority
  - map credential/channel scope
  - identify shared dispatcher authority across NAIA/Anna
~~~

---

## 6. Engram

Repository:
radotsvetkov/engram

Pin:
3a43667deec4a680b42f3e880d7d6bac3baf0746

### Product shape

The exact-pin product surface describes a persistent personal agent with:

- memory;
- workdir-confined files;
- shell backends;
- Web search/fetch;
- headless and interactive Chrome;
- subagents;
- messaging;
- scheduling and real OS wake timers;
- zero-idle service activation;
- signed/hash-chained append-only receipts for memory/skill/tool activity.

Classification:

~~~text
PERSISTENT_PERSONAL_AGENT_PRODUCT = YES
MEMORY = PRESENT
BROWSER = PRESENT
SCHEDULED_WAKE = PRESENT
MESSAGING = PRESENT
AUDIT_LEDGER = MATERIAL_PRODUCT_SURFACE
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

Residual before local work:

~~~text
ENGRAM_NEXT_EVIDENCE:
  - map approval/external-effect authority, not only audit receipts
  - map restart/wake semantics and duplicate-effect behavior
  - map credential custody
  - map NAIA/Anna separation topology
  - distinguish signed evidence after an action from prevention before an action
~~~

---

## 7. Holt

Repository:
holt-os/holt

Pin:
3a9cb8b0fd62e0b61e5e600a3fa341bd5b03e65e

### Product shape

The exact-pin product is a local personal-agent OS with:

- private persistent memory;
- named routines/tasks;
- real OS scheduling on macOS/Linux/Windows;
- Telegram access;
- MCP;
- provider/brain switching;
- local skill system;
- direct API brains and external agentic CLI brains.

Classification:

~~~text
PERSISTENT_PERSONAL_AGENT_CHASSIS = YES
MEMORY = PRESENT
SCHEDULING = PRESENT
TELEGRAM = PRESENT
PROVIDER_BRAIN_REPLACEABILITY = PRESENT
COMPARABLE_CANDIDATE = YES_WITH_EXTERNAL_BRAIN_DEPENDENCY
CURRENT_PIN_QUALIFIED = NO
~~~

### Authority boundary

For CLI brains such as Claude/Codex/Gemini, Holt intentionally preserves the selected brain's native agentic tool and permission UI rather than owning the entire execution/approval policy itself.

Therefore:

~~~text
EFFECTIVE_TOOL_AUTHORITY = BRAIN_DEPENDENT_FOR_CLI_BRAINS
HOLT_POLICY_ALONE != COMPLETE_ACTION_AUTHORITY
~~~

Residual:

~~~text
HOLT_ATENTO_DELTA:
  - choose/freeze exact brain + permission topology before evaluation
  - determine which consequential effects Holt mediates versus delegates
  - prove scheduled runs preserve the intended brain authority policy
  - compose NAIA/Anna with independent memory/credential authority
  - count external-brain maintenance as part of total migration cost
~~~

---

## 8. RustFox

Repository:
chinkan/RustFox

Pin:
6e24388d36d1c6fac399039d8cab07cd9cb8264b

### Product shape

The exact-pin source/product surface includes:

- Telegram assistant;
- persistent SQLite memory + vector/RAG;
- sandboxed built-in tools;
- MCP;
- isolated subagent loops with model/tool whitelists;
- multiple bot/persona configurations;
- cron and one-shot scheduling;
- SQLite-persisted scheduled tasks;
- dead-letter rerun queue;
- Web control portal;
- provider flexibility including local models.

Exact source visibly persists scheduled-task rows and exposes agent tool-whitelist enforcement surfaces.

Classification:

~~~text
PERSISTENT_ASSISTANT_PRODUCT = YES
PERSISTENT_MEMORY = PRESENT
MESSAGING = TELEGRAM
SCHEDULE_PERSISTENCE = PRESENT
SUBAGENT_TOOL_WHITELIST = PRESENT
MULTI_BOT_PERSONA = PRESENT
COMPARABLE_CANDIDATE = YES
CURRENT_PIN_QUALIFIED = NO
~~~

Residual before local work:

~~~text
RUSTFOX_NEXT_EVIDENCE:
  - map main-agent consequential-action approval defaults
  - map sandbox/secret-store authority to scheduled work
  - prove multi-bot persona memory/credential isolation
  - map rerun/dead-letter semantics to duplicate external effects
  - map browser/web-action capability through built-in/MCP composition
~~~

---

## 9. Admission result

The bounded secondary screen yields:

~~~text
ADMITTED_COMPARABLE:
  - AutoMate
  - AgentOS
  - OpenAgentd
  - HubOS
  - Engram
  - Holt
  - RustFox

DEFERRED_AT_CURRENT_PIN:
  - Open Intern
~~~

This is a technical inclusion decision only. It is not a ranking or recommendation.

No candidate in this screen is current-pin qualified.

---

## 10. Candidate-universe consequence

The previously named discovery pools have now received an admission screen.

Therefore the discovery snapshot can be frozen for evidence reconciliation:

~~~text
REGISTERED_DISCOVERY_POOL_SCREENING = COMPLETE_V1
FROZEN_CANDIDATE_UNIVERSE_V1 = COMPLETE
CANDIDATE_UNIVERSE_COMPLETE = true_for_frozen_v1_snapshot
~~~

This does not mean no new project can ever be discovered. Reopen the universe only on a material new candidate, not by continuously broadening search while decision-relevant evidence remains unresolved.

The newly admitted seven still require upstream evidence/transfer mapping before any common local NCP.

~~~text
SECONDARY_POOL_ADMISSION_SCREEN = COMPLETE_V1
NEW_SECONDARY_COMPARABLE_COUNT = 7
OPEN_INTERN_ADMISSION = DEFERRED_AT_CURRENT_PIN

LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED

NEXT_BLOCK =
  upstream evidence + transfer audit for newly admitted secondary candidates,
  grouped to minimize repeated work
~~~
