# NAIA upstream transfer audit — Octop / Agent Zero / Rome / OpenGrokBot — 2026-09-30

## Contract

This record determines which exact-pin upstream mechanisms from Octop, Agent Zero, Rome and OpenGrokBot can be reused for NAIA without rerunning equivalent local tests, and which properties remain Atento-specific configuration or topology deltas.

It does not rank, shortlist, qualify, accept or select any candidate.

~~~text
TEST_SOURCE_PRESENT != TEST_EXECUTED
STATIC_SOURCE != RUNTIME_PASS
AVAILABLE_GUARDRAIL != SAFE_DEFAULT
APPROVAL_TOOL != ENFORCED_EXTERNAL_EFFECT_GATE
PERSISTED_SCHEDULER != EXACTLY_ONCE_EXTERNAL_EFFECT
PROJECT_OR_PROFILE_ISOLATION != AUTOMATIC_NAIA_ANNA_COMPOSITION
~~~

Pins:

~~~text
Octop        e473dd3c4a4741618ffde1a42a3492341a189e8e
Agent Zero   e3051fb584b1a36be2b0a0c90606f1c2c2d356ec
Rome         ef523c4659149e2711744deb04ec42c3be339907
OpenGrokBot  43ba51fc0487b7adbb23861a1062a113390833d9
~~~

Exact-pin GitHub visibility checked through the available connector:

~~~text
Octop:
  workflow_runs = []
  combined_statuses = []

Agent Zero:
  workflow_runs = []
  combined_statuses = []

Rome:
  workflow_runs = []
  combined_statuses = []

OpenGrokBot:
  workflow_runs = []
  combined_statuses = []
~~~

Subsequent exact-pin workflow enumeration found hosted execution for Octop that the earlier PR-only lookup missed. See:

`docs/evaluation/octop-exhaustive-verification-2026-09-30.md`

Observed Octop status:

~~~text
release non-live suite = 3951 passed / 17 skipped
CodeQL = PASS
desktop package/runtime smoke = PASS across macOS/Linux/Windows targets
Docker/release packaging = PASS
~~~

The same passing suite makes the cross-user workspace denial, security-default tests and Bridge path-policy tests run-backed at this pin. The stock Bridge policy also exposes agent-scoped mutation authority, including tool-setting/plugin-tool changes and browser handoff, so it is not equivalent to the Atento broker-only contract.

For Agent Zero, Rome and OpenGrokBot, this document's original hosted-execution statements remain governed by their later candidate-specific verification records where present.

The source/test contracts below remain reusable at their exact proven scope.

---

## 1. Octop

Repository:
TencentCloud/Octop

Pin:
e473dd3c4a4741618ffde1a42a3492341a189e8e

### 1.1 Product and state model

The exact-pin README describes Octop as a self-hosted, multi-user, multi-agent assistant with:

- per-user experts;
- per-expert workspace, providers, channels and cron;
- persistent memory tied to the workspace;
- browser automation with persistent profiles;
- remote desktop;
- multiple IM channels;
- a single control-plane database;
- runtime state rebuilt from that database on boot.

This is a direct persistent-assistant product match.

Transfer classification:

~~~text
PERSISTENT_ASSISTANT_PRODUCT = YES
MULTI_USER_MULTI_AGENT_MODEL = PRESENT
CONTROL_PLANE_RESTART_REBUILD = DOCUMENTED
BROWSER_AND_CHANNEL_SURFACE = PRESENT
~~~

This does not by itself prove every in-flight authority state survives restart.

### 1.2 User/workspace and cron ownership boundaries

The exact-pin integration test tests/integration/test_workspace_api.py proves a non-owner receives 403 when attempting to read another user's agent workspace.

The cron test surface includes agent/user isolation and owner-bound management contracts.

Therefore:

~~~text
CROSS_USER_WORKSPACE_ACCESS = TECHNICALLY_DENIED_BY_TEST_SOURCE
CRON_OWNER_SCOPE = DIRECT_TEST_SURFACE_PRESENT
STRICT_NAIA_ANNA_ISOLATION = NOT_YET_EQUIVALENT
~~~

The Atento requirement is stricter than ordinary multi-user isolation because NAIA and Anna must not silently share memory, credentials, tool authority or channels.

### 1.3 Security defaults are not the hardened NAIA defaults

The exact-pin tests/unit/test_security_settings.py establishes the missing-policy defaults:

~~~text
hitl.enabled = false
tool_guard.enabled = true
tool_guard.mode = warn
~~~

That is material.

Octop has a real HITL/tool-guard mechanism, but the default posture at this pin is not fail-closed for consequential tool use.

Therefore:

~~~text
HITL_MECHANISM = PRESENT
TOOL_GUARD_MECHANISM = PRESENT
DEFAULT_HITL = DISABLED
DEFAULT_TOOL_GUARD_MODE = WARN
DEFAULT_MATCHES_HARDENED_NAIA = NO
ATENTO_DELTA = EXPLICIT_HARDENED_SECURITY_PROFILE
~~~

### 1.4 Pending HITL restart continuity is not established

The exact-pin src/octop/infra/gateway/hitl/store.py calls the pending approval registry:

~~~text
Session-scoped pending HITL records (process-local, TTL-gc).
~~~

The records are held in an in-memory dictionary and expire by TTL.

This is narrower than the general control-plane restart claim.

Therefore:

~~~text
GENERAL_STATE_RESTART_REBUILD = DOCUMENTED
PENDING_HITL_STORE = PROCESS_LOCAL
PENDING_HITL_RESTART_CONTINUITY = NOT_ESTABLISHED
~~~

A later local restart probe is justified only if Octop reaches a shortlist and no other exact upstream recovery path closes this gap.

### 1.5 Connector authority can be implicitly inherited by cron

The exact-pin connector API defines a per-account default_open flag whose description states that, when enabled, connector tools are injected for the owner on IM and on Cron jobs with no explicit connector picks.

Cron with explicit picks follows the explicit selection.

Therefore:

~~~text
CRON_CONNECTOR_AUTHORITY = CAN_INHERIT_ACCOUNT_DEFAULTS
BACKGROUND_AUTHORITY_CONFIGURATION = MATERIAL
IMPLICIT_CONNECTOR_INHERITANCE = MUST_BE_DISABLED_OR_EXPLICITLY_AUDITED_FOR_NAIA
~~~

This is not a defect by itself; it is a configuration surface that can broaden background authority if left implicit.

### 1.6 Octop residual

~~~text
OCTOP_ATENTO_DELTA:
  - freeze HITL/tool-guard settings into a fail-closed NAIA profile
  - remove or explicitly bound default-open connector inheritance for cron
  - prove the chosen NAIA/Anna topology separates memory, credentials, tools and channels
  - resolve pending-approval restart behavior only if decision-critical
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 2. Agent Zero

Repository:
agent0ai/agent-zero

Pin:
e3051fb584b1a36be2b0a0c90606f1c2c2d356ec

### 2.1 Project isolation is a first-class product contract

The exact-pin README states that Projects isolate:

- workspaces;
- instructions;
- memory;
- secrets;
- knowledge;
- repositories;
- model-preset choices.

The exact-pin project reference further maps project-owned material to .a0proj, including:

- encrypted project secrets;
- per-project agent profiles;
- project-scoped skills;
- project MCP server configuration.

The exact-pin memory plugin default is:

~~~text
project_memory_isolation: true
~~~

Transfer classification:

~~~text
PROJECT_MEMORY_ISOLATION_DEFAULT = TRUE
PROJECT_SCOPED_SECRETS = PRESENT
PROJECT_SCOPED_AGENT/SKILL/MCP = PRESENT
STRICT_ROLE_TOPOLOGY_BUILDING_BLOCK = STRONG
~~~

### 2.2 Tool policy enforcement is real, but the default is permissive

The exact-pin helpers/tool_policy.py resolves tool policy at project/profile scope and technically denies a blocked tool through RepairableException.

The exact-pin tests/test_tool_policy.py exercises policy across prompt exposure, provider-native schemas and execution.

However the exact-pin bundled default config is:

~~~text
mode: inherit
default: allow
mcp_default: allow
allowed: []
blocked: []
~~~

The normalizer also treats unspecified local/MCP defaults as allow.

Therefore:

~~~text
TECHNICAL_TOOL_POLICY = STRONG
PROFILE_SCOPED_POLICY = PRESENT
DEFAULT_LOCAL_TOOLS = ALLOW
DEFAULT_MCP_TOOLS = ALLOW
DEFAULT_MATCHES_HARDENED_NAIA = NO
ATENTO_DELTA = CUSTOM_DENY_BY_DEFAULT_PROFILE
~~~

### 2.3 Scheduled work persists, but effective background policy still needs composition proof

The exact-pin scheduler persists task state in tasks.json and reloads it.

Scheduled tasks carry project_name and context_id. The scheduler prevents an already RUNNING task from being launched again through the ordinary run-by-id path and persists success/error state.

This supports:

~~~text
SCHEDULE_DEFINITION_PERSISTENCE = PRESENT
SCHEDULER_RELOAD = PRESENT
PROJECT_ASSOCIATION = PRESENT
SAME_EFFECTIVE_PROFILE_POLICY_IN_BACKGROUND = NOT_FULLY_ESTABLISHED_HERE
ARBITRARY_EXTERNAL_EFFECT_EXACTLY_ONCE = NOT_PROVEN
~~~

The remaining question is not whether Agent Zero has a scheduler; it is whether the chosen scheduled NAIA context resolves the same or narrower deny-by-default tool/MCP policy as the interactive NAIA profile.

### 2.4 Instance-global and host-level surfaces remain separate authority domains

The exact-pin WhatsApp/Telegram product docs state that plugin toggles are instance-wide, while per-profile permissions edit Tools and MCPs.

Host Computer Use permissions are controlled through the Launcher/CLI rather than solely through the ordinary profile permission editor.

Therefore:

~~~text
PROJECT_SCOPE != INSTANCE_WIDE_PLUGIN_SCOPE
PROFILE_TOOL_POLICY != HOST_COMPUTER_AUTHORITY
~~~

A one-instance NAIA/Anna deployment must not infer strict isolation from project memory isolation alone.

### 2.5 Agent Zero residual

~~~text
AGENT_ZERO_ATENTO_DELTA:
  - create separate NAIA and Anna projects/profiles
  - set local-tool and MCP defaults to block, then allow only explicit NAIA capabilities
  - verify scheduled runs resolve the intended project/profile policy
  - audit instance-wide plugins and global/OAuth material for cross-role authority
  - keep host Computer Use as a separately granted deployment capability
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 3. Rome

Repository:
rome-os/rome

Pin:
ef523c4659149e2711744deb04ec42c3be339907

### 3.1 Profile is an explicit hard data boundary

The exact-pin docs/concepts/deployment.md states:

~~~text
The profile is the data isolation boundary: nothing in one profile
(database, memory, apps, auth state) is visible from another.
~~~

The exact-pin process architecture further requires one Rome process per host/profile pair and stores the profile lockfile under the profile-specific directory.

Transfer classification:

~~~text
ROME_PROFILE_DATA_ISOLATION = EXPLICIT_CONTRACT
DATABASE_MEMORY_APPS_AUTH_CROSS_PROFILE_VISIBILITY = DENIED_BY_DESIGN
NAIA_ANNA_TWO_PROFILE_TOPOLOGY = DIRECTLY_SUPPORTED
~~~

This is strong source-level topology evidence, not a runtime qualification.

### 3.2 Approval flow has durable, explicit contracts

The exact-pin approval-flow E2E uses real DB-backed repositories and the production action engine/approval handler.

It directly covers:

- requiresApproval actions becoming pending;
- nested sensitive actions surfacing a pending approval;
- multiple pending approvals coexisting independently;
- approval executing the originally approved payload;
- durable execution/approval state.

The exact-pin approvals API tests additionally establish:

- anonymous and visitor actors cannot use approval entry points;
- foreign/missing origin evidence receives 403 without changing approval state;
- chat-style affirmations such as yes/send it/ok do not flip a pending approval;
- explicit approval routes are required;
- already-resolved approvals conflict rather than silently changing state.

Transfer classification:

~~~text
ACTION_APPROVAL_STATE_MACHINE = STRONG
GUARDIAN_ONLY_APPROVAL_SURFACE = DIRECTLY_TESTED
CHAT_AFFIRMATION_AUTO_APPROVAL = NEGATIVE
CROSS_ORIGIN_APPROVAL = DENIED
~~~

Equivalent local unit tests are not justified if these mechanisms remain unchanged.

### 3.3 Approval is action metadata, not a universal default

The exact-pin ActionConfig declares:

~~~text
visibility?: public | explicit
requiresApproval?: boolean
~~~

and documents visibility as public by default.

Therefore a sensitive action must actually be marked and routed through the approval-aware action contract; the presence of the approval engine alone is not a universal fail-closed guarantee.

Additionally, the exact-pin environment example documents:

~~~text
Auto-approve agent-initiated creations (default: true)
AUTO_APPROVE_SKILLS=true
AUTO_APPROVE_TOOLS=true
AUTO_APPROVE_WORKFLOWS=true
~~~

Those creation approvals are distinct from action execution approvals, but they still affect capability-growth authority and must be frozen for NAIA.

Classification:

~~~text
APPROVAL_ENGINE = STRONG
REQUIRES_APPROVAL = PER_ACTION_METADATA
ACTION_VISIBILITY_DEFAULT = PUBLIC
AGENT_INITIATED_CAPABILITY_CREATION_AUTO_APPROVAL_DEFAULT = TRUE
DEFAULT_MATCHES_HARDENED_NAIA = NO
~~~

### 3.4 Provider-native execution is a separate authority seam

At the exact pin, the Codex app-server provider opens ordinary threads with:

~~~text
sandbox: danger-full-access
approvalPolicy: never
~~~

while Rome exposes its own dynamic action/tool facade.

This means the Atento review must not assume the upstream model provider's native approval/sandbox is a second safety layer.

The exact question is whether every consequential capability reachable in the chosen NAIA configuration is mediated by the Rome-owned action/tool policy that Atento intends to rely on.

Therefore:

~~~text
PROVIDER_NATIVE_SANDBOX = NOT_A_HARDENING_LAYER_AT_THIS_PIN
ROME_OWNED_ACTION_GATE = DECISION_CRITICAL
BYPASS_REVIEW = REQUIRED_FOR_CHOSEN_PROVIDER/TOOLSET
~~~

### 3.5 Rome residual

~~~text
ROME_ATENTO_DELTA:
  - compose NAIA and Anna as separate Rome profiles/processes
  - disable or explicitly constrain agent-initiated capability auto-approval
  - require approval on every consequential NAIA action, not merely selected examples
  - audit provider-native tools so danger-full-access/approval-never cannot bypass Rome's intended gate
  - keep explicit broker-only cross-profile handoff
  - do not claim generic exactly-once external effects without adapter evidence

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 4. OpenGrokBot

Repository:
wolfqing/OpenGrokBot

Pin:
43ba51fc0487b7adbb23861a1062a113390833d9

### 4.1 Per-bot computer isolation has concrete enforcement

The exact-pin security document separates enforced boundaries from conventions.

Enforced boundaries include:

- gateway API protected by a gateway token;
- state-changing requests restricted to the gateway/UI origin;
- gateway bound to loopback by default;
- gateway token absent from bot workspaces, so a bot cannot approve its own hold;
- container-to-container traffic disabled;
- per-container shell/CDP/VNC credentials;
- one workspace mounted per bot container;
- no-new-privileges plus resource/process limits;
- allowlisted bot-to-bot handoffs;
- peer-to-peer handoffs disabled by default unless explicitly configured.

Transfer classification:

~~~text
PER_BOT_COMPUTER_BOUNDARY = STRONG_STATIC_CONTRACT
BOT_SELF_APPROVAL = TECHNICALLY_BLOCKED
PEER_HANDOFF_DEFAULT = CLOSED_EXCEPT_CHIEF_ROUTING
CONTAINER_CROSS_REACH = TECHNICALLY_RESTRICTED
~~~

### 4.2 Standing memory is outside the bot workspace

The exact-pin gateway memory contract stores standing MEMORY.md outside the bot workspace.

The security document says a bot-authored MEMORY.md inside its own workspace is ignored and standing-rule changes go through save_memory with a diff chip.

Therefore:

~~~text
STANDING_MEMORY_MUTATION_PATH = GATEWAY_OWNED
BOT_WORKSPACE_CANNOT_SILENTLY_REWRITE_STANDING_MEMORY = YES_BY_CONTRACT
~~~

This is useful evidence for memory authority. It does not by itself prove a full NAIA/Anna memory taxonomy or cross-role broker.

### 4.3 Browser login isolation is per bot

The exact-pin security document states each bot's browser login/session lives in that bot's workspace profile.

The gateway does not hold the website password.

Per-container shim/CDP/VNC secrets are separately generated.

Therefore:

~~~text
BROWSER_SESSION_SCOPE = PER_BOT_PROFILE
CONTAINER_CONTROL_SECRETS = PER_CONTAINER
MODEL_PROVIDER_KEY = GATEWAY_ENVIRONMENT_LEVEL
~~~

The shared model-provider key is not equivalent to shared data-bearing website credentials.

### 4.4 Approval for outward browser effects is explicitly not an enforcement wall

This is the most important OpenGrokBot constraint.

The exact-pin security document explicitly says that hold_for_approval before outward actions is:

~~~text
a strong discipline, not an enforcement point
~~~

because a bot with a real signed-in browser can click Send directly.

Therefore:

~~~text
APPROVAL_UI = PRESENT
BOT_CANNOT_SELF_APPROVE_HOLD = ENFORCED
OUTWARD_BROWSER_EFFECT_REQUIRES_HOLD_TECHNICALLY = NO
PROMPT_ONLY_POLICY = INSUFFICIENT
DEFAULT_MATCHES_HARDENED_NAIA_EXTERNAL_EFFECT_AUTHORITY = NO
~~~

The technical gateway boundary protects the approval endpoint, but it does not force all consequential browser actions through that endpoint.

### 4.5 Routines reuse the full toolset

The exact-pin gateway test explicitly describes:

~~~text
routines run with the full toolset
~~~

and proves that a routine can voluntarily call hold_for_approval.

The same suite also tests that simultaneous firings of the same routine result in one run and one skip, and that bots may stop their own routines but not a teammate's.

Therefore:

~~~text
ROUTINE_DUPLICATE_CONCURRENT_FIRE = GUARDED_BY_TEST_SOURCE
ROUTINE_CAN_REQUEST_APPROVAL = YES
ROUTINE_TOOLSET = FULL
BACKGROUND_AUTHORITY_NARROWER_THAN_INTERACTIVE = NO_BY_DEFAULT
ARBITRARY_EXTERNAL_EFFECT_EXACTLY_ONCE = NOT_PROVEN
~~~

### 4.6 OpenGrokBot residual

~~~text
OPENGROKBOT_ATENTO_DELTA:
  - add a technical consequential-effect gate that browser/shell actions cannot bypass
  - make routine authority equal to or narrower than the hardened interactive NAIA authority
  - preserve per-bot browser/workspace/container separation for NAIA and Anna
  - keep peer handoff explicitly allowlisted/brokered
  - verify any role-specific credentials beyond browser logins are not shared through gateway/global configuration
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 5. Transfer summary

| Property | Octop | Agent Zero | Rome | OpenGrokBot |
|---|---|---|---|---|
| persistent role state | per-expert workspace/control plane | project-scoped state | profile-scoped data | per-bot workspace + gateway DB |
| strongest isolation primitive | user/agent ownership + workspace | project/profile | profile/process | per-bot container/workspace |
| memory default/boundary | workspace-portable memory; strict role composition still needed | project memory isolation true | profile data isolation explicit | standing memory gateway-owned; per-bot workspace |
| tool/action default | HITL off; guard warn | inherit/allow for local + MCP | approval optional per action; capability-creation autoapproval on | full tools; outward hold is convention |
| scheduled work | per-agent cron; connector defaults may flow into cron | persisted tasks with project association | routines/actions | routines use full toolset |
| approval strength | mechanism present, permissive default | technical deny policy available, permissive default | strong durable action approval when configured | hold endpoint protected, but browser can bypass |
| exact-pin hosted runtime | not observed | not observed | not observed | not observed |
| generic exactly-once external effect | not established | not established | not established | not established |

No row is a score or ranking.

---

## 6. Consequence for local NCP

This pass closes the missing exact-pin source/test inventory for these four expanded candidates.

It does not yet start local NCP because the candidate universe still contains provisional candidates requiring same-protocol admission.

If one of these four eventually reaches a shortlist, local work should be restricted to the residual composition delta above.

Do not rerun:

- Octop cross-user workspace denial merely to duplicate the exact upstream integration test;
- Agent Zero tool-policy prompt/schema/execution filtering merely to duplicate upstream tests;
- Rome approval API/state-machine cases already covered upstream;
- OpenGrokBot gateway/container/handoff contracts already represented in source/tests.

The future local checks, if decision-critical, are narrower:

~~~text
Octop:
  hardened security defaults
  + cron connector inheritance
  + strict NAIA/Anna topology
  + pending HITL restart only if still unresolved

Agent Zero:
  deny-by-default profile composition
  + scheduled context policy resolution
  + instance-global/plugin/OAuth/host-computer boundary

Rome:
  two-profile topology
  + capability-creation defaults
  + consequential-action completeness
  + provider-native bypass review

OpenGrokBot:
  technical browser/shell consequential-effect mediation
  + routine authority narrowing
  + strict role credential composition
~~~

State:

~~~text
TRANSFER_AUDIT_OCTOP_AGENTZERO_ROME_OPENGROKBOT = COMPLETE_V1
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
CANDIDATE_UNIVERSE_COMPLETE = false
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~
