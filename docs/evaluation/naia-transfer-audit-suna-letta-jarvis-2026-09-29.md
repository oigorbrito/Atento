# NAIA upstream transfer audit — Suna / Letta Code / PersonalJarvis — 2026-09-29

## Contract

This record determines which upstream mechanisms are reusable for NAIA **without rerunning them locally**, and which properties still require an Atento-specific delta.

It does not rank, shortlist, qualify, accept or select any candidate.

```text
UPSTREAM_TEST_SOURCE != EXECUTED_AT_CURRENT_PIN
TRANSFERABLE_WITH_CONSTRAINTS != ATENTO_ACCEPTED
CONFIG_HARDENING != CORE_FORK
PRODUCT_FEATURE != STRICT_ISOLATION
```

Pins:

```text
Suna           270c4a57c8ae5ffb85eff6d5b9700c5713612f28
Letta Code     21daa38a8cdd74f2d03b634c8312253080bacfc1
PersonalJarvis 1be33c457739ca7e161ee6fbaf298ec10d4dad3b
```

No GitHub workflow run / combined status was observable at these exact pins through the available connector during this audit.

---

## 1. Kortix / Suna

### 1.1 Per-agent grants

The current v2 path is materially stronger than the v1 compatibility path.

The runtime parser for v2 explicitly resolves:

- connectors;
- secrets;
- Kortix permissions;
- apps;

through `resolveGrantSet(..., 'none')`.

The manifest-schema helper also states:

```text
v1 omitted grant -> all
v2 omitted grant -> none
```

and the current docs describe v2 as deny-by-default for connectors, secrets, permissions, skills and apps.

There is one documentation inconsistency worth preserving: a type comment on `AgentBlockV2.secrets` still says `all (default when omitted)`, while the actual v2 parser resolves omitted secrets to `none`. Runtime parser + tests are the stronger source for this audit.

Transfer classification:

```text
PER_AGENT_CONNECTOR_GRANTS = UPSTREAM_PROVEN_BY_SOURCE_TESTS
PER_AGENT_SECRET_GRANTS = UPSTREAM_PROVEN_BY_SOURCE_TESTS
PER_AGENT_PLATFORM_PERMISSIONS = UPSTREAM_PROVEN_BY_SOURCE_TESTS
V2_OMITTED_GRANT_FAILS_CLOSED = UPSTREAM_PROVEN_BY_SOURCE_TESTS
```

No local reimplementation test is justified if NAIA uses the unchanged v2 grant path.

### 1.2 Connector-action approval default

Project connector policy has two fallback modes:

- `risk`: reads run; write/destructive require approval;
- `allow_all`: unmatched tools run.

The current default for a missing `policy:` block is explicitly `allow_all` for backward compatibility.

Therefore:

```text
MECHANISM_FOR_HARDENING = PRESENT
DEFAULT_MATCHES_NAIA = NO
ATENTO_DELTA = EXPLICIT_CONFIG
```

Minimum NAIA hardening profile must declare at least:

```yaml
policy:
  default_mode: risk
```

plus explicit `block` / argument-scoped rules where the NAIA authority model requires a stronger deny than risk-tier approval.

This is a configuration delta unless a required tool bypasses that policy path.

### 1.3 Scheduled/background idempotency

Suna's own scheduler guidance is explicit:

```text
the platform dedups fires, not your work
```

A cron slot is not double-spawned, but application work must track its own high-water mark / handled identifiers.

Therefore scheduler-level dedup does **not** prove duplicate-free external effects.

Transfer classification:

```text
CRON_FIRE_DEDUP = TRANSFERABLE_WITH_CONSTRAINTS
ARBITRARY_EXTERNAL_EFFECT_DEDUP = UNPROVEN
```

Atento should not rerun a generic cron test merely to rediscover this documented boundary.

The residual NAIA question is whether the concrete high-risk external adapters selected for NAIA provide idempotency/readback/reconciliation.

### 1.4 NAIA / Anna isolation

Suna sessions are isolated sandboxes, but the product model is project-centric:

- one project is one shared repository;
- `memory/` is described as the project brain;
- any number of agents can work in that shared workspace;
- session branches/sandboxes isolate execution, not the underlying project knowledge domain.

Therefore same-project multi-agent isolation is not equivalent to ADR-001's strict NAIA/Anna authority boundary.

```text
SESSION_SANDBOX_ISOLATION = TRANSFERABLE
SAME_PROJECT_MEMORY_ISOLATION = NOT_STRICT
STRICT_NAIA_ANNA_ISOLATION = ATENTO_DELTA
```

The plausible no-core-fork topology is separate Kortix projects / repositories / grants, connected only through the explicit Atento handoff broker. That topology still needs a composition proof if Suna reaches the shortlist.

### 1.5 Current residual

```text
SUNA_ATENTO_DELTA:
  - explicit policy.default_mode=risk + NAIA deny rules
  - separate-project topology for NAIA/Anna if strict boundary is required
  - adapter-specific idempotency/reconciliation for consequential external effects

LOCAL_NCP_NOW = NO
```

The next evidence should be static/topology composition mapping, not a generic Suna benchmark.

---

## 2. Letta Code

### 2.1 Permission default

The current source defines:

```text
DEFAULT_PERMISSION_MODE = unrestricted
```

and tests explicitly assert:

```text
unrestricted mode - allows all tools
```

Explicit deny rules and `alwaysAsk` rules still override unrestricted mode, and a separate `strict` mode routes tools through approval.

Therefore:

```text
PERMISSION_MECHANISM = STRONG
DEFAULT_MATCHES_NAIA = NO
ATENTO_DELTA = EXPLICIT_HARDENED_MODE/RULESET
```

A NAIA profile cannot inherit the default. It must pin `strict` or a deliberately constructed ruleset and verify the effective mode on every background/channel surface.

### 2.2 Cross-agent memory and shell boundary

Letta has a strong in-process cross-agent memory guard for file tools.

The guard:

- is evaluated before ordinary permission logic;
- allows only self and explicit parent-agent memory;
- denies another agent's memory paths for in-process file tools;
- protects both API and local memory trees.

However shell execution has a materially different boundary.

The source states:

- shell commands are no longer path-scanned;
- cross-agent shell confinement is opt-in via `LETTA_FS_SANDBOX=1`;
- agent shells run unconfined by default;
- memory subagents have stronger default process confinement.

The product also intentionally supports:

- shared memory attached to multiple agents;
- searching across agents/conversations.

Therefore a same-runtime Letta deployment does not automatically satisfy a strict NAIA/Anna boundary.

```text
IN_PROCESS_FILE_MEMORY_GUARD = UPSTREAM_PROVEN_BY_SOURCE_TESTS
SHELL_CROSS_AGENT_ISOLATION_DEFAULT = INSUFFICIENT
SHARED_MEMORY_FEATURE = INTENTIONAL
STRICT_NAIA_ANNA_ISOLATION = ATENTO_DELTA
```

A hardened profile would minimally require:

- `LETTA_FS_SANDBOX=1` where supported;
- no shared-memory attachment across the NAIA/Anna boundary;
- no cross-agent conversation/search route across that boundary;
- or stronger: separate Letta runtimes/storage authority with explicit brokered handoff.

If Letta reaches a later shortlist, the topology boundary is the useful local test — not another unit test of the in-process guard.

### 2.3 Cron / persistence

Letta's scheduler has source contracts for:

- persisted cron task definitions;
- scheduler leases;
- per-minute double-fire suppression;
- pause re-check before enqueue;
- missed/failed outcome recording;
- run logs;
- conversation-scoped queueing.

This is substantial upstream contract evidence.

It does not by itself prove:

- process-crash recovery at the target deployment boundary;
- exactly-once external effects;
- authority parity after restart.

Classification:

```text
CRON_SCHEDULER_CONTRACT = TRANSFERABLE_WITH_CONSTRAINTS
RESTART_EXTERNAL_EFFECT_EXACTNESS = UNPROVEN
```

### 2.4 Current residual

```text
LETTA_ATENTO_DELTA:
  - replace unrestricted default with explicit hardened permission profile
  - enable/prove shell confinement or use separate runtime topology
  - disable cross-boundary shared-memory/search behavior
  - prove only the remaining restart/topology delta if shortlisted

LOCAL_NCP_NOW = NO
```

---

## 3. PersonalJarvis

### 3.1 Scheduled-task authority

PersonalJarvis has a particularly concrete upstream mechanism for unattended actions.

`TaskAutoApprover`:

- arms one scheduled turn by `trace_id`;
- receives an explicit set of pre-authorized plugin ids;
- approves only an `ActionApprovalRequired` whose trace matches;
- checks the tool against the granted plugin set;
- does not approve ungranted tools;
- does not consume preauthorization on proposal alone;
- disarms after the turn;
- leaves unmatched ask-tier calls to deny on timeout;
- preserves the normal audit chain rather than bypassing the approval workflow.

Integration tests directly cover:

- correct trace;
- actual execution through `ToolExecutor`;
- ungranted tool refusal;
- wrong-trace refusal;
- disarm;
- namespaced MCP tool matching;
- inert read-only/empty grant.

Transfer classification:

```text
SCHEDULED_PREAUTH_TRACE_BINDING = UPSTREAM_PROVEN_BY_SOURCE_TESTS
UNGRANTED_BACKGROUND_TOOL_AUTO_APPROVAL = DENIED_BY_CONTRACT
BACKGROUND_APPROVAL_AUDIT_CHAIN = PRESENT
```

This mechanism should be reused rather than reconstructed locally.

### 3.2 Computer/browser evidence

Current docs record a historical successful Browser Runtime GitHub Actions run:

```text
run_id = 34451340158
head_sha = 92a86c3ece138f0f9babf2f0700900e5d627d8d5
conclusion = success
created_at = 2026-09-10
```

That run is not the current discovery pin, so:

```text
HISTORICAL_BROWSER_CI = EXECUTED_SUCCESS
CURRENT_PIN_BROWSER_CI = NOT_OBSERVED
```

The same OS-parity document explicitly distinguishes verified Windows/Linux/browser paths from unverified native macOS/Linux desktop paths.

This is useful transfer evidence by platform, not a blanket current-pin pass.

### 3.3 Society memory and tools

Current source provides meaningful agent scoping:

- each society agent has a namespaced memory folder;
- the wiki-note tool has no arbitrary path input and writes only under `society/<agent_id>/`;
- ordinary agents do not contribute to a shared knowledge pool through that tool;
- agent shell tooling is path-contained to the agent workspace;
- society messaging is a dedicated one-target path with caller/target checks and a kill switch;
- the agent definition exposes `knowledge_scope: own|shared`.

This is stronger than prompt-only separation.

However:

- society shell isolation is local/path containment, not a container or separate OS authority boundary;
- the broader product has a shared vault concept;
- model/provider credentials are obtained through provider-level Agent secret resolution in the inspected execution paths, not proven as distinct per-society-agent credential stores;
- grouping agents explicitly does not itself change permissions.

Therefore:

```text
AGENT_MEMORY_NAMESPACE = UPSTREAM_PROVEN_BY_SOURCE
AGENT_WORKSPACE_PATH_CONTAINMENT = UPSTREAM_PROVEN_BY_SOURCE
STRICT_OS_PROCESS_ISOLATION = NOT_PRESENT_BY_DEFAULT
STRICT_PER_AGENT_CREDENTIAL_ISOLATION = NOT_ESTABLISHED
STRICT_NAIA_ANNA_ISOLATION = ATENTO_DELTA
```

For ADR-001, the safe transfer claim is memory/tool namespace separation — not full hostile multi-tenant isolation.

### 3.4 Background/computer authority caveat

The user-facing safety docs state that:

- a scheduled task with Write/Full grant may execute the matching action without asking again;
- Computer Use can start immediately because the outer tool and many desktop steps are classified safe/monitor.

These are coherent with the product's grant model but are not the NAIA hardening defaults by themselves.

Atento must freeze the exact allowed background grant set and any computer-use risk reclassification before treating those mechanisms as acceptable.

### 3.5 Current residual

```text
PERSONALJARVIS_ATENTO_DELTA:
  - define NAIA-specific background grant profile
  - define computer-use approval boundary
  - prove strict NAIA/Anna credential/runtime isolation topology
  - target-OS acceptance only where upstream platform evidence is absent

LOCAL_NCP_NOW = NO
```

---

## 4. Transfer summary

| Property | Suna | Letta Code | PersonalJarvis |
|---|---|---|---|
| per-agent grants | upstream-proven v2 deny-by-default | permission rules exist; default unrestricted | tool/grant surfaces present |
| default external-action posture | permissive `allow_all` unless hardened | `unrestricted` | mixed risk tiers + explicit grants |
| scheduled authority | trigger grant + policy; work dedup left to app | cron scheduler + permission mode | trace-bound scheduled preauthorization |
| memory isolation | project memory is shared | file guard strong; shared memory intentional; shell gap | namespaced society memory strong |
| shell/process isolation | per-session sandbox | shell sandbox opt-in | local path containment; no container by default |
| strict NAIA/Anna boundary | separate-project topology needed | hardened/separate-runtime topology needed | separate-runtime/credential topology needed |
| generic exactly-once effects | not proven | not proven | not proven |
| current-pin hosted CI | not observed | not observed | not observed |

No row above is a score or ranking.

## 5. Consequence for NCP

For these three candidates, broad local probing would still be premature.

The only future local checks justified by current evidence are topology/configuration deltas:

```text
Suna:
  prove hardened policy + separate-project NAIA/Anna composition if shortlisted

Letta:
  prove strict permission mode + shell sandbox/separate-runtime boundary if shortlisted

PersonalJarvis:
  prove NAIA/Anna credential/runtime separation + target-OS computer boundary if shortlisted
```

Do not rerun the upstream unit/integration contracts listed above merely to duplicate them.

```text
TRANSFER_AUDIT_SUNA_LETTA_JARVIS = COMPLETE_V1
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
