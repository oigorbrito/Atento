# NAIA upstream transfer audit — Engram / Holt — 2026-09-30

## Contract

This record closes the final grouped upstream/transfer audit for the frozen V1 secondary NAIA candidate pool.

It does not rank, shortlist, qualify, accept, promote or select any candidate.

~~~text
SOURCE_CONTRACT != RUNTIME_PASS
AUDIT_LEDGER != PREVENTIVE_AUTHORITY
SIGNED_AUTONOMY != UNIVERSAL_ACTION_APPROVAL
SCHEDULE_PERSISTENCE != EXACTLY_ONCE_EXTERNAL_EFFECT
BRAIN_PERMISSION_UI != HOLT_OWNED_AUTHORITY
WORKSPACE_MEMORY_ISOLATION != FULL_ROLE_ISOLATION
~~~

Pins:

~~~text
Engram  radotsvetkov/engram  3a43667deec4a680b42f3e880d7d6bac3baf0746
Holt    holt-os/holt         3a9cb8b0fd62e0b61e5e600a3fa341bd5b03e65e
~~~

At the admission screen, neither exact pin had observable workflow runs or combined statuses through the available connector.

Therefore:

~~~text
CODE_PASS = NOT_CLAIMED
CODE_FAIL = NOT_CLAIMED
HOSTED_EXECUTION = NOT_OBSERVED
~~~

---

## 1. Engram

### 1.1 Core authority model is technical, not prompt-only

The exact-pin ToolCtx carries:

- taint;
- sensitive-data state;
- filesystem workdir;
- per-run Policy;
- memory scope;
- per-agent allowed-tools scope;
- signed standing autonomy;
- shared egress budget;
- explicit attended/unattended mode.

The Tool registry is filtered at the run chokepoint by:

- global disabled tools;
- optional per-agent allowed tools.

Delegated subagents inherit the parent tool scope rather than gaining a broader set.

Classification:

~~~text
TECHNICAL_TOOL_SCOPE = PRESENT
SUBAGENT_AUTHORITY_EXPANSION = CONSTRAINED_BY_PARENT_SCOPE
PROMPT_ONLY_POLICY = NO
~~~

### 1.2 Defaults are materially conservative in some dimensions

Exact Policy defaults include:

~~~text
allow_shell = false
approved = false
approved_dest = none
autonomy = none
daemon_allowlist = []
attended = true
~~~

The security config also defaults shell disabled.

Filesystem paths are confined to the workdir with lexical and symlink escape checks.

Classification:

~~~text
SHELL_DEFAULT = OFF
EGRESS_ONE_TIME_APPROVAL_DEFAULT = OFF
STANDING_AUTONOMY_DEFAULT = NONE
FILESYSTEM_WORKDIR_CONFINEMENT = PRESENT
~~~

### 1.3 Taint + sensitive + egress gate is a strong reusable boundary

The agent centrally tracks two provenance dimensions:

~~~text
untrusted content
private/sensitive data
~~~

When both are present, egress tools are routed through a destination-aware gate.

The gate evaluates, in order:

- hardline policy floor;
- one-time human approval, optionally destination-scoped;
- signed standing autonomy policy;
- daemon-level approved destination list;
- attended refusal or unattended staging.

Opaque destinations under a standing policy do not auto-allow.

Autonomy has a shared action budget, including delegated subagents.

Every decision is ledgered.

Classification:

~~~text
DESTINATION_AWARE_EGRESS_GATE = TECHNICAL
ONE_TIME_APPROVAL_DEST_SCOPE = PRESENT
SIGNED_UNATTENDED_AUTONOMY = PRESENT
OPAQUE_DESTINATION_AUTO_ALLOW = NO
SUBAGENT_EGRESS_BUDGET_SHARED = YES
UNATTENDED_UNKNOWN_EGRESS = STAGED
~~~

This evidence should be reused rather than duplicated with a generic approval benchmark.

### 1.4 Browser action is outside that egress classification

The exact tool contract deliberately marks interactive browser operations as non-egress.

In particular:

~~~text
browser_open.is_egress = false
browser_click.is_egress = false
browser_type.is_egress = false
browser_extract.is_egress = false
~~~

Browser click/type are marked side-effecting, but they do not pass through the destination-aware egress approval decision merely because they are consequential.

The source rationale treats the interactive browser as visible research/ingress rather than a generic outbound channel.

Therefore:

~~~text
BROWSER_SIDE_EFFECTS = PRESENT
BROWSER_DESTINATION_EGRESS_GATE = NO
BROWSER_CONSEQUENTIAL_ACTION_APPROVAL = NOT_ESTABLISHED
~~~

This is a specific NAIA residual. Browser navigation safety/SSRF and consequential browser action authority are separate questions.

### 1.5 Trusted-run consequential effects are not universally approval-gated

The egress gate is armed by the untrusted+sensitive combination.

That is a strong exfiltration boundary, but it is not equivalent to:

~~~text
all consequential external effects require explicit technical authority
~~~

A trusted run that has not armed the trifecta may still execute allowed side-effecting tools without a per-action human approval.

Therefore:

~~~text
EXFILTRATION_GUARD = STRONG
UNIVERSAL_CONSEQUENTIAL_EFFECT_APPROVAL = NO
~~~

For NAIA, the fixed effect-authority profile must be layered on top of the existing taint model, not confused with it.

### 1.6 Scheduling persistence and crash behavior are explicit

The exact scheduler:

- persists jobs to jobs.json;
- atomically rewrites the store;
- reloads jobs on open;
- persists next/last fire data;
- supports first-class agent binding;
- skips missed-fire stampedes by advancing to the next future recurrence;
- has tests for persistence across reopen and agent binding.

The daemon supports:

~~~text
engramd --run-due
~~~

and marks a due occurrence fired before executing the resulting task, specifically to avoid a crash causing that occurrence to fire twice.

Classification:

~~~text
SCHEDULE_DEFINITION_PERSISTENCE = PRESENT
SCHEDULE_REOPEN_TEST = PRESENT
MISSED_FIRE_STAMPEDE = AVOIDED
DUE_OCCURRENCE_MARKED_BEFORE_TASK_EXECUTION = YES
DUPLICATE_TRIGGER_ON_MIDRUN_CRASH = REDUCED_BY_DESIGN
~~~

The tradeoff is that a crash after marking fired but before completing the external effect can lose the occurrence. This is not exactly-once semantics.

### 1.7 Dynamic zero-idle wake arming is incomplete at this pin

The scheduler exposes next_wake and the systemd module can generate a wake timer that calls --run-due.

However the exact scheduler module states that automatic wake re-arming from next_wake is not yet wired into daemon/deploy lifecycle.

The documented production wake remains a static calendar path unless an operator/integration explicitly wires the dynamic primitive.

Therefore:

~~~text
NEXT_WAKE_PRIMITIVE = PRESENT
RUN_DUE_PRIMITIVE = PRESENT
DYNAMIC_WAKE_REARMING = NOT_WIRED_AT_PIN
ARBITRARY_ZERO_IDLE_SCHEDULE_ACCURACY = NOT_ESTABLISHED
~~~

This is a bounded deployment-composition gap, not a reason to re-test scheduler persistence broadly.

### 1.8 Agent memory/credential scope is not strict NAIA/Anna isolation

Durable agents can have:

- their own provider/base URL/API key;
- allowed tool set;
- home project;
- signed autonomy policy.

Per-agent API keys live in the owner-only agents.json and are masked from the API.

But an agent home project is still defined as:

~~~text
project ring + user-global memory
~~~

rather than a private role memory authority.

The durable-agent store itself is one process-wide file under one ENGRAM_HOME.

Therefore:

~~~text
PER_AGENT_PROVIDER_KEY = PRESENT
PER_AGENT_TOOL_SCOPE = PRESENT
PER_AGENT_PROJECT_SCOPE = PRESENT
USER_GLOBAL_MEMORY = SHARED_ACROSS_AGENTS
STRICT_NAIA_ANNA_MEMORY_ISOLATION_IN_ONE_HOME = NO
STRICT_CREDENTIAL_STORE_AUTHORITY_IN_ONE_HOME = NOT_ESTABLISHED
~~~

A two-home/two-runtime composition is a valid Atento topology and should be costed rather than rejected automatically.

### 1.9 Signed ledger is evidence, not preventive authority

Engram's append-only signed ledger and offline verification are materially useful.

It can reconstruct autonomous egress decisions after the fact.

But:

~~~text
SIGNED_RECEIPT != PRE_ACTION_APPROVAL
~~~

The ledger strengthens auditability; it does not close the browser/universal-effect authority residual by itself.

### 1.10 Engram residual

~~~text
ENGRAM_ATENTO_DELTA:
  - add/freeze technical authority for consequential browser actions
  - define approval/allowlist policy for trusted-run consequential effects, not only exfiltration cases
  - compose strict NAIA/Anna memory + credential domains, likely separate ENGRAM_HOME/runtime
  - wire or otherwise guarantee schedule wake accuracy for the chosen zero-idle deployment
  - preserve existing signed autonomy, tool-scope inheritance, taint gate and ledger
  - measure the two-home/runtime composition cost
  - do not claim generic exactly-once external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 2. Holt

### 2.1 Holt is a persistent personal-agent chassis with OS-native scheduling

The exact-pin product has:

- per-workspace persistent memory;
- optional semantic recall;
- named routines;
- OS-native schedules on macOS/Linux/Windows;
- Telegram;
- skill system;
- MCP memory exposure;
- CLI brains and direct API brains;
- provider switching.

The scheduler source keeps a JSON source of truth at:

~~~text
~/.holt/schedules.json
~~~

and installs the actual schedule into:

- launchd on macOS;
- user crontab on Linux;
- Task Scheduler on Windows.

The scheduled command executes the Holt binary in the captured workspace.

Classification:

~~~text
PERSISTENT_PERSONAL_AGENT_CHASSIS = YES
OS_NATIVE_SCHEDULING = PRESENT
SCHEDULE_SOURCE_OF_TRUTH = PERSISTENT_JSON
MAC_LINUX_WINDOWS_BUILDERS = PRESENT
WINDOWS_SCHEDULER_PURE_TESTS = PRESENT
~~~

Because the OS scheduler owns the trigger, restart continuity does not depend on a resident Holt process.

### 2.2 Per-workspace memory is isolated by default

Holt stores ordinary memory under the current workspace.

The exact README/source explicitly state that recall does not cross folders by default.

A shared global fact store exists, but it is opt-in.

Classification:

~~~text
PER_WORKSPACE_MEMORY = DEFAULT
CROSS_WORKSPACE_GLOBAL_MEMORY = OPT_IN
DEFAULT_MEMORY_CROSS_WORKSPACE_READ = NO
~~~

This is a useful primitive for role composition.

### 2.3 Global authority surfaces remain shared across workspaces

Holt also defines one process-user global root:

~~~text
~/.holt
~~~

which contains, among other things:

- trust registry;
- credentials.json;
- telegram.json;
- schedules.json;
- routines.json;
- optional global memory.

Direct API credentials are stored by provider in the global credentials file, mode 0600.

Telegram is also single-user/global and contains one token + allowed chat id.

Therefore two role workspaces under one OS user do not automatically have independent credential/channel authority.

~~~text
PER_WORKSPACE_MEMORY != PER_WORKSPACE_CREDENTIAL_AUTHORITY
GLOBAL_PROVIDER_CREDENTIAL_STORE = YES
GLOBAL_TELEGRAM_CONFIG = YES
STRICT_NAIA_ANNA_AUTHORITY_IN_ONE_OS_USER = NO
~~~

Separate OS-user homes or a Holt storage refactor/broker would be needed for strict Atento role authority.

### 2.4 Interactive CLI-brain authority belongs to the selected brain

Bare Holt launches the real interactive brain CLI.

The README is explicit that this preserves the brain's:

- agentic edits;
- tool use;
- permission UI;
- MCP.

Holt does not replace that permission system with its own universal executor.

Classification:

~~~text
INTERACTIVE_AGENTIC_AUTHORITY_OWNER = SELECTED_CLI_BRAIN
HOLT_OWNED_UNIVERSAL_TOOL_GATE = NO
~~~

This means a Holt evaluation is incomplete until the exact brain and its permission profile are frozen.

### 2.5 Holt has a narrow external-file permission gate for Claude

For paths outside the trusted workspace, Holt provides a session-only gate.

When granted, Claude Code receives only:

~~~text
Read, Glob, Grep
~~~

for the external directory.

The source explicitly avoids dangerous-skip-permissions and edit-accepting modes for this cross-folder grant.

Classification:

~~~text
EXTERNAL_FILE_GRANT_DEFAULT = DENY
EXTERNAL_FILE_GRANT_SCOPE = SESSION_ONLY
CLAUDE_EXTERNAL_GRANT = READ_ONLY_TOOLS
~~~

This is useful but narrow. It does not mediate the brain's ordinary in-workspace agentic authority.

### 2.6 Scheduled runs delegate authority to the brain non-interactively

OS schedules execute:

~~~text
holt run <task> --quiet
~~~

or a routine subcommand that eventually executes the configured task path.

The noninteractive runner resolves the selected brain and dispatches to either:

- CLI brain via its configured noninteractive arguments;
- direct API brain via plain provider HTTP.

For CLI brains, Holt does not inject a Holt-owned per-action approval policy into the scheduled run.

For direct API brains, the Holt runner itself is text-only; provider calls do not expose Holt-native tool execution.

Therefore:

~~~text
SCHEDULED_CLI_BRAIN_AUTHORITY = BRAIN_CLI_DEFAULTS
SCHEDULED_DIRECT_API_BRAIN_TOOL_AUTHORITY = NONE_IN_HOLT_RUNNER
BACKGROUND_AUTHORITY_OWNER = DEPENDS_ON_FROZEN_BRAIN
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY = NOT_PROVEN_GENERICALLY
~~~

This is the central Holt transfer constraint.

### 2.7 Schedule notification is a configured external effect

A scheduled Holt job can optionally send its output through Holt's Telegram notify path after a successful run.

Telegram itself is restricted to the configured allowed chat id.

The user authorizes notification when configuring the job/routine, so this is closer to standing configured authority than an emergent model-selected recipient.

Still, Holt does not provide a generic action receipt/idempotency layer for every possible brain-side effect.

~~~text
SCHEDULE_NOTIFY_TARGET = CONFIGURED_SINGLE_CHAT
GENERIC_EXTERNAL_EFFECT_IDEMPOTENCY = NOT_ESTABLISHED
~~~

### 2.8 Credentials are protected by file mode but not role-isolated

CLI brains own their sign-in and Holt does not store those credentials.

Direct API brains resolve keys from:

1. a brain-specific environment variable;
2. the global Holt credentials file;
3. the provider standard environment variable.

The global credentials file is owner-only, but provider keys are shared across Holt workspaces by default.

Therefore:

~~~text
CLI_BRAIN_CREDENTIAL_CUSTODY = EXTERNAL_BRAIN
DIRECT_API_CREDENTIAL_FILE_MODE = 0600
DIRECT_API_CREDENTIAL_SCOPE = GLOBAL_BY_PROVIDER
STRICT_ROLE_CREDENTIAL_ISOLATION = NO_IN_ONE_OS_USER
~~~

### 2.9 Holt residual

~~~text
HOLT_ATENTO_DELTA:
  - freeze one exact brain/provider path before evaluating authority
  - for CLI brains, map and harden the brain's noninteractive permission defaults
  - prove scheduled authority is same-or-narrower than interactive authority for that exact brain
  - compose NAIA/Anna under separate credential/channel authority domains
  - keep global memory disabled across the role boundary
  - account for external-brain updates as ongoing maintenance cost
  - add adapter-level idempotency/reconciliation where scheduled brain actions can cause external effects

LOCAL_GENERIC_NCP_NOW = NO
~~~

---

## 3. Transfer summary

| Property | Engram | Holt |
|---|---|---|
| persistent memory | embedded persistent memory + scopes | per-workspace memory by default |
| scheduling | persistent scheduler + in-daemon tick + run-due | OS-native launchd/cron/Task Scheduler |
| restart continuity | job reopen tests; crash recovery primitives | OS scheduler persists independently of Holt process |
| authority owner | Engram tool/taint/autonomy policy | selected brain for agentic CLI paths |
| unattended policy | signed autonomy + staging for egress | brain-dependent for CLI; text-only for direct API brain |
| browser | native, but click/type are non-egress | depends on selected agentic brain |
| credentials | global provider secret store + per-agent keys in one owner-only store | CLI-owned login or global provider credentials file |
| strict NAIA/Anna memory isolation | not in one shared user-global ring | feasible by workspace if global memory stays off |
| strict NAIA/Anna credential/channel isolation | not established in one ENGRAM_HOME | not in one OS-user ~/.holt |
| generic exactly-once external effect | no | no |
| exact-pin hosted runtime | not observed | not observed |

No row is a score, rank or verdict.

---

## 4. Secondary transfer gate result

With this record, all seven candidates admitted from the secondary pool have bounded upstream/transfer audits:

~~~text
AutoMate
AgentOS
OpenAgentd
HubOS
RustFox
Engram
Holt
~~~

No generic local benchmark is justified merely to re-demonstrate their already located product/source contracts.

The next phase must be residual-only:

~~~text
1. normalize each candidate's remaining Atento delta
2. group identical residuals
3. reuse prior local evidence where the boundary is materially the same
4. execute only the smallest unresolved composition/authority probe
5. collect adaptation/cost evidence during the same work
~~~

State:

~~~text
TRANSFER_AUDIT_ENGRAM_HOLT = COMPLETE_V1
SECONDARY_TRANSFER_AUDITS = COMPLETE_7_OF_7
EXPANDED_EXTERNAL_EVIDENCE_GATE = COMPLETE_V1
CURRENT_PIN_QUALIFIED = 0
LOCAL_GENERIC_NCP_PHASE = NOT_STARTED
RESIDUAL_ONLY_PROBE_DERIVATION = NEXT
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~
