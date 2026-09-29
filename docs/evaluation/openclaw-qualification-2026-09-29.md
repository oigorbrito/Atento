# OpenClaw qualification — 2026-09-29

## Contract

Este registro preserva a qualificação do OpenClaw como candidato a base da Nayá Assistente.

Não é uma decisão de seleção. O repositório canônico continua sendo o Atento.

- **Source:** `SRC-OPENCLAW`
- **Repo:** https://github.com/openclaw/openclaw
- **Qualification pin:** `e9571d77e76bd6d35996273d9e8398ad539b26e1`
- **Previous observed upstream pin:** `17cb0b6bf797d2d350f7268c00464b00aff7729a`
- **Delta:** 8 commits ahead on 2026-09-29
- **License at pin:** MIT
- **Decision state:** `NOT_SELECTED`

## Evidence reused

The qualification reused existing upstream evidence rather than rerunning generic benchmarks.

Primary inspected surfaces at the pin include:

- `docs/tools/goal.md`
- `docs/tools/permission-modes.md`
- `docs/nodes/node-exec.md`
- `docs/concepts/multi-agent.md`
- `docs/reference/memory-config.md`
- `docs/gateway/restart-recovery.md`
- `docs/gateway/audit.md`
- `docs/gateway/protocol/ledgers.md`
- `docs/gateway/security/trust-model.md`
- `docs/gateway/security/tool-permissions.md`
- `docs/plugins/sdk-channel-outbound.md`
- `docs/plugins/hooks.md`
- `docs/plugins/hooks/tool-policy.md`
- `SECURITY.md`
- relevant source/tests for exec approvals, restart recovery, subagent lifecycle and outbound delivery.

The GitHub connector exposed no combined status entries or pull-request workflow runs for the exact main-branch pin, so no hosted-CI claim is made here.

---

## 1. Generic external-effect durability vs channel durability

### Finding

OpenClaw has a strong durable outbound-message protocol.

Observed properties include:

- durable send intent before provider I/O when `durability: "required"`;
- queue ownership of retry/reconciliation;
- explicit outcomes for sent/suppressed/partial failure/failure;
- persisted provider receipts when available;
- ambiguous-send handling;
- optional `reconcileUnknownSend(...)` for channel adapters that can prove provider state using provider-owned idempotency or authoritative readback;
- fail-closed recovery when provider proof is incomplete.

This is materially stronger than ordinary "retry on error" messaging.

### Limit

The same general contract is not provided for arbitrary tool/SaaS writes.

The OpenClaw Goal documentation states that operation receipts prevent duplicate Goal mutations and input turns, but:

```text
They do not promise exactly-once external tool or provider effects.
```

Therefore:

```text
CHANNEL_OUTBOUND_DURABILITY     = STRONG_EVIDENCE
GENERIC_TOOL_EFFECT_DURABILITY  = NOT_PROVEN
GENERAL_EXACTLY_ONCE            = NOT_CLAIMED
```

A universal Nayá guarantee for arbitrary external actions would require one of:

1. a common persisted operation/effect envelope at the tool boundary, with tool participation in idempotency/readback/reconciliation; or
2. restricting high-risk writes to Atento-controlled adapters that implement those contracts individually.

The first is cross-cutting. The second can remain localized per critical integration.

---

## 2. Policy / approval fit

OpenClaw provides a substantial authority surface:

- host exec modes: `deny`, `allowlist`, `ask`, `auto`, `full`;
- layered host + config policy;
- persistent approval state;
- command/executable binding and revalidation before launch;
- cancellation/stale-authority defenses;
- plugin `before_tool_call` approval/block/rewrite hooks;
- trusted tool-policy hooks for host-trusted gates.

This is compatible with Nayá, but the defaults are not the Nayá target.

OpenClaw documents `auto` as the recommended default for coding agents. Nayá's required operational posture is narrower:

```text
default deny / least privilege
→ explicit allowlist
→ explicit approval where required
→ no stale authority recreation
→ audit evidence
```

Qualification result:

```text
POLICY_PRIMITIVES = STRONG
DEFAULT_POLICY_FIT = NEEDS_HARDENING
NAYA_POLICY_FIT = CONFIGURABLE_BUT_NOT_DEFAULT
```

A Nayá deployment should define an explicit hardening profile rather than inherit general-purpose defaults.

---

## 3. Memory isolation

OpenClaw supports meaningful per-agent separation:

- separate workspace;
- separate `agentDir`;
- separate SQLite session history;
- per-agent auth/config state;
- built-in memory searches same-agent configured memory/session sources rather than another agent's transcript corpus.

However, the separation is not universal automatically:

- plugin-owned storage follows plugin configuration;
- some plugin stores may be global unless explicitly scoped per agent;
- workspace is a default cwd, not a hard security sandbox;
- cross-agent session reach is enabled by default unless narrowed.

Therefore:

```text
PER_AGENT_CORE_STATE_ISOLATION = STRONG
PLUGIN_STORAGE_ISOLATION = CONFIG_DEPENDENT
CROSS_AGENT_SESSION_ISOLATION = NOT_DEFAULT
```

---

## 4. Assistant ↔ Therapist authority boundary

ADR-001 requires:

```text
Therapist cannot query Assistant memory by default
Assistant cannot query Therapy memory by default
Therapist cannot invoke personal-side-effect tools by default
Assistant cannot invoke therapy internals by default
```

OpenClaw's own security model says one Gateway is trusted-operator infrastructure, not an adversarial multi-tenant security boundary.

Its multi-agent documentation explicitly recommends separate Gateways for strict separation.

Therefore two agents inside one Gateway are not sufficient evidence for the stronger Nayá invariant "Therapy remains completely outside Assistant authority".

Recommended topology for qualification:

```text
NAYÁ ASSISTANT GATEWAY/RUNTIME
        |
   explicit broker
        |
THERAPY GATEWAY/RUNTIME
```

with independent:

- process/Gateway boundary;
- credentials;
- memory authority;
- tool registry;
- storage;
- policy state.

Cross-domain exchange should occur only through the explicit handoff contract defined by ADR-001.

Qualification result:

```text
SAME_GATEWAY_PERSONA_SEPARATION = SUPPORTED
STRICT_THERAPY_BOUNDARY = REQUIRES_SEPARATE_RUNTIME/GATEWAY
```

---

## 5. Trust/security assumptions

Material OpenClaw assumptions that Nayá must not inherit silently:

1. the Gateway is primarily a trusted-operator boundary;
2. session ownership/visibility are not security boundaries;
3. cross-agent access can be enabled broadly by default;
4. a workspace is not a hard sandbox by itself;
5. native plugins run in the Gateway process and must be trusted;
6. host execution can be configured to broad authority and some trusted-host modes intentionally skip ordinary approval paths.

These are not defects relative to OpenClaw's documented model, but they differ from Nayá's intended compartmentalization.

Required Nayá adjustments:

- explicit sandboxing where side effects are available;
- narrow `tools.sessions.visibility`;
- disable or tightly allowlist `tools.agentToAgent`;
- explicit per-agent tool profiles;
- no therapy credentials/storage on the Assistant Gateway;
- strict plugin allowlist/provenance;
- no `full` exec posture in normal operation;
- audit the effective policy, not only authored config.

---

## 6. Adaptation invasiveness

### Low / localized

OpenClaw already exposes configuration or plugin seams for:

- per-agent workspaces/state;
- model/provider choices;
- tool allow/deny;
- host exec modes;
- approvals;
- sandbox configuration;
- tool policy hooks;
- approval hooks;
- channel routing;
- memory plugins;
- UI/CLI/Gateway product surfaces.

These needs do not require a deep fork by themselves.

### Moderate

Nayá hardening requires a maintained opinionated profile:

- deny-by-default tool policy;
- explicit session visibility;
- agent-to-agent restrictions;
- plugin allowlist;
- sandbox defaults;
- hardened approval policy;
- audit assertions.

This can likely remain config + plugin + deployment topology.

### Structural

A universal generic external-effect guarantee is the main structural gap.

Because a generic `before_tool_call`/`after_tool_call` hook cannot prove whether an arbitrary external provider side effect occurred after a crash, exactly-once/reconciliation semantics require cooperation at the tool/adapter effect boundary.

Classification:

```text
PRODUCT_ADAPTATION = LOW_TO_MODERATE
NAYA_SECURITY_HARDENING = MODERATE
STRICT_THERAPY_BOUNDARY = DEPLOYMENT_TOPOLOGY_CHANGE
UNIVERSAL_GENERIC_EFFECT_DURABILITY = CROSS_CUTTING_IF_REQUIRED
CRITICAL_TOOL_ONLY_DURABILITY = LOCALIZED_IF_ADAPTER_CONTROLLED
```

---

## 7. Upstream evidence and local tests that remain

### Do not repeat locally

No new generic local benchmark is justified for:

- basic persistent conversation/session state;
- restart/recovery of accepted turns;
- subagent lifecycle persistence;
- channel outbound queue/reconciliation semantics;
- existence of approval and policy primitives.

Those properties already have upstream source/docs/test evidence at the inspected pin.

### Material local tests still required

#### OC-NAYA-001 — fail-closed authority profile

Configure the candidate with the intended Nayá policy and verify:

- unknown/high-risk tools are denied by default;
- approval is required where specified;
- cancelled/stale approval cannot authorize later work;
- effective policy remains narrow after restart;
- no implicit broadening through nested/code-mode tool calls.

#### OC-NAYA-002 — arbitrary external-action crash ambiguity

Use a controlled fake external provider with an observable side effect.

Fault point:

```text
persist intent
→ provider effect succeeds
→ crash before local terminal commit
→ restart
```

Expected behavior for any promoted high-risk adapter:

- no blind duplicate;
- outcome becomes reconciled, terminally unknown, or requires operator action;
- retry is permitted only when non-execution is proved.

This test is expected to fail for an arbitrary unmodified generic tool path unless the adapter participates in an effect protocol.

#### OC-NAYA-003 — Assistant ↔ Therapist isolation

Run Assistant and Therapist under the proposed strict topology.

Verify:

- Assistant cannot enumerate/query Therapy sessions or memory;
- Therapist cannot enumerate/query Assistant sessions or memory;
- Assistant cannot invoke Therapy internals;
- Therapist cannot invoke personal side-effect tools;
- restart does not widen authority;
- only the handoff broker can carry an explicitly allowed minimal payload.

#### OC-NAYA-004 — plugin/global-store negative test

Enable representative memory/plugin storage and prove that no supposedly per-agent store silently resolves to a shared/global backend.

This protects against treating core per-agent state separation as proof for every plugin.

#### OC-NAYA-005 — integration touchpoint count

Implement the hardening profile and one controlled external-action adapter, then record:

- changed upstream files;
- plugin/config-only changes;
- required core patches;
- maintained fork touchpoints.

This is the empirical invasiveness measurement required by ADR-002.

---


## Local-delta execution update — 2026-09-29

The generic OC-NAYA-001..005 workflow was prepared in the candidate-evaluation harness on PR #17.

GitHub Actions execution remains unavailable/observable as of this update: after enabling the candidate workflow for pull requests on `main`, the GitHub connector returned no workflow run for the rebased PR head. This is classified as infrastructure evidence, not candidate failure.

```text
OPENCLAW_NAYA_ACTIONS_EXECUTION = INFRA_BLOCKED
HARNESS_NOT_RUN != CANDIDATE_FAIL
```

### Controlled external-effect fault probe

The qualification-only adapter subprobe from OC-NAYA-002 was executable without the OpenClaw dependency graph and was run directly.

Exact PR blobs executed:

- `effect-protocol.mjs` Git blob: `5189ad624db51a7b9334ded71d1a24cfc0d834bf`
- `effect-protocol.test.mjs` Git blob: `7dbc97fd4629c2496ebe9a04aac1bbb2ab40efe5`

Local runtime used for this isolated algorithm probe:

- Node.js `v22.16.0`

Observed fault sequence:

```text
persist intent
→ provider effect succeeds
→ simulated crash before local terminal commit
→ reconstruct adapter
→ authoritative provider readback
→ persist reconciled completion
→ replay same operation id
```

Observed result:

```json
{
  "ok": true,
  "crash_point": "provider_effect_succeeded_before_local_terminal_commit",
  "recovered_without_duplicate": true,
  "provider_calls_after_reconcile": 1,
  "second_operation_completed": true
}
```

Interpretation:

```text
OC-NAYA-002.CONTROLLED_ADAPTER_FAULT_PROBE = PASS_EMPIRICAL
CONTROLLED_ADAPTER_DONOR_CORE_EDITS        = 0 (design target; full plugin validation pending)
GENERIC_TOOL_EFFECT_DURABILITY             = ARCH_RISK / NOT_PROVEN
```

This result proves only the adapter-level reconciliation algorithm. It does **not** prove that the pinned OpenClaw runtime accepts/loads the plugin, because `openclaw plugins validate` and the pinned upstream runtime tests still require an executable dependency environment.

Therefore the remaining status is:

- `OC-NAYA-001`: pending pinned-runtime execution;
- `OC-NAYA-002`: generic path remains `ARCH_RISK`; controlled adapter algorithm subprobe passed;
- `OC-NAYA-003`: pending pinned-runtime execution;
- `OC-NAYA-004`: pending pinned-runtime execution;
- `OC-NAYA-005`: donor-core touchpoint claim pending OpenClaw plugin validation/runtime execution.

No Project Point is earned by this qualification update.


## Qualification disposition

At the inspected pin:

```text
PRODUCT_MATURITY                = STRONG
PERSISTENT_ASSISTANT_FIT        = STRONG
RESTART_RECOVERY                = STRONG_EVIDENCE
STALE_AUTHORITY_DEFENSE         = STRONG_EVIDENCE
OUTBOUND_DELIVERY_DURABILITY    = STRONG_EVIDENCE
POLICY_PRIMITIVES               = STRONG
NAYA_POLICY_DEFAULT_FIT         = NEEDS_HARDENING
PER_AGENT_CORE_STATE_ISOLATION  = STRONG
STRICT_THERAPY_BOUNDARY         = SEPARATE_RUNTIME_REQUIRED
GENERIC_TOOL_EFFECT_DURABILITY  = NOT_PROVEN
LICENSE                         = MIT
STATUS                          = STRONG_CANDIDATE / STATIC_QUALIFICATION_COMPLETE
LOCAL_DELTA_TESTS               = PENDING
```

No base winner is selected by this record.

The next decision step is to execute only OC-NAYA-001 through OC-NAYA-005, then compare OpenClaw, OpenMausBot and NaIA using the same ADR-002 decision protocol.
