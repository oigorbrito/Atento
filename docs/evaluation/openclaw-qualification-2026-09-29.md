# OpenClaw qualification — 2026-09-29

> **HISTORICAL EVIDENCE / DECISION RESET:** todos os pins, achados e limitações deste documento são preservados. Qualquer linguagem de “finalist”, “next decision step” ou prioridade de `OC-NAYA-*` está **inativa** até OpenClaw ser reenquadrado na nova enumeração comparável da **NAIA**. Os IDs `OC-NAYA-*` são identificadores históricos e não definem a nomenclatura atual do produto.

## Contract

Este registro preserva a qualificação técnica histórica do OpenClaw como possível chassis de assistente persistente. Ele não concede shortlist ou prioridade atual para a NAIA.

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

A universal NAIA guarantee for arbitrary external actions would require one of:

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

This is compatible with NAIA, but the defaults are not the NAIA target.

OpenClaw documents `auto` as the recommended default for coding agents. NAIA's required operational posture is narrower:

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
NAIA_POLICY_FIT = CONFIGURABLE_BUT_NOT_DEFAULT
```

A NAIA deployment should define an explicit hardening profile rather than inherit general-purpose defaults.

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

Therefore two agents inside one Gateway are not sufficient evidence for the stronger NAIA invariant "Therapy remains completely outside Assistant authority".

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

Material OpenClaw assumptions that NAIA must not inherit silently:

1. the Gateway is primarily a trusted-operator boundary;
2. session ownership/visibility are not security boundaries;
3. cross-agent access can be enabled broadly by default;
4. a workspace is not a hard sandbox by itself;
5. native plugins run in the Gateway process and must be trusted;
6. host execution can be configured to broad authority and some trusted-host modes intentionally skip ordinary approval paths.

These are not defects relative to OpenClaw's documented model, but they differ from NAIA's intended compartmentalization.

Required NAIA adjustments:

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

NAIA hardening requires a maintained opinionated profile:

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
NAIA_SECURITY_HARDENING = MODERATE
STRICT_THERAPY_BOUNDARY = DEPLOYMENT_TOPOLOGY_CHANGE
UNIVERSAL_GENERIC_EFFECT_DURABILITY = CROSS_CUTTING_IF_REQUIRED
CRITICAL_TOOL_ONLY_DURABILITY = LOCALIZED_IF_ADAPTER_CONTROLLED
```

---

## 7. Evidence transfer and the one remaining pre-selection delta

### Upstream evidence accepted with audit

The following properties have directly relevant implementation/tests at the inspected pin and should not be reimplemented as Atento tests merely to obtain another pass:

- persistent operator approval state, including reopen/recovery behavior;
- terminal/CAS approval semantics and stale-resolution defenses;
- restart/recovery mechanisms already exercised upstream;
- outbound delivery queue/reconciliation semantics;
- per-agent core state separation;
- explicit cross-agent/session policy surfaces.

This is not blind trust in donor documentation. Reuse requires that the claim be tied to code and tests at the pinned SHA. Hosted CI status for the exact pin was not observable through the available GitHub interface, so no "CI green" claim is made.

### Transfer constraints

Some upstream evidence transfers only when NAIA preserves the relevant boundary:

- policy evidence transfers only if NAIA uses the supported policy/config hooks rather than bypassing them;
- per-agent state isolation does not prove isolation for every plugin-owned global store;
- same-Gateway multi-agent controls do not satisfy ADR-001's strict Assistant ↔ Therapist authority boundary;
- outbound-message durability does not generalize to arbitrary external tool effects.

### OC-NAYA-001 — minimal NAIA hardening/profile probe

This was the **historical pre-selection probe** proposed before the decision reset. It is now inactive unless OpenClaw re-enters the comparable NAIA candidate set.

If OpenClaw is reselected for audit, implement the smallest NAIA profile using supported OpenClaw seams and prove:

- the authored configuration is valid;
- effective exec/tool policy is fail-closed for the intended Assistant deployment;
- cross-agent/session reach is narrowed as required;
- sandbox/isolation settings required by the Assistant profile are expressible without a core fork;
- restart/reload does not broaden the effective policy;
- the adaptation can be maintained as config/plugin/deployment glue, or any required core patch is explicitly counted.

Record as part of the same probe:

- Atento files added/changed;
- OpenClaw upstream files patched, if any;
- config/plugin-only touchpoints;
- whether the candidate remains upstream-trackable.

Do **not** rewrite OpenClaw's stale-approval/restart test suite. If this probe is reactivated, reuse upstream evidence for unchanged mechanisms and test only material NAIA deltas.

### Reclassified work

The previously proposed candidate-local tests are moved to the blocks that own the real adaptation:

- **generic external-action crash ambiguity** → Block J / external-action adapter. The unmodified OpenClaw generic tool path is already documented as not providing universal exactly-once effects. The useful empirical test is the real Atento high-risk adapter after it implements idempotency/readback/reconciliation.
- **Assistant ↔ Therapist isolation** → ADR-001 composition/deployment. Test separate runtime/Gateway authority plus the explicit broker once that composition exists.
- **plugin/global-store isolation** → the concrete plugin/memory integration that selects the store. Do not test an arbitrary plugin before one is adopted.
- **integration touchpoint count** → measurement inside OC-NAYA-001 rather than a separate test.

This preserves empirical engineering while avoiding duplicate suites and context/test debt.

---

## Qualification disposition

At the inspected pin:

```text
PRODUCT_MATURITY                = STRONG
PERSISTENT_ASSISTANT_FIT        = STRONG
RESTART_RECOVERY                = STRONG_EVIDENCE
STALE_AUTHORITY_DEFENSE         = STRONG_EVIDENCE
OUTBOUND_DELIVERY_DURABILITY    = STRONG_EVIDENCE
POLICY_PRIMITIVES               = STRONG
NAIA_POLICY_DEFAULT_FIT         = NEEDS_HARDENING
PER_AGENT_CORE_STATE_ISOLATION  = STRONG
STRICT_THERAPY_BOUNDARY         = SEPARATE_RUNTIME_REQUIRED
GENERIC_TOOL_EFFECT_DURABILITY  = NOT_PROVEN
LICENSE                         = MIT
STATUS                          = EVIDENCE_PRESERVED / SELECTION_RESET
LOCAL_PRESELECTION_DELTA        = INACTIVE_UNLESS_RESELECTED
```

No base winner is selected by this record.

**Current decision state:** no OpenClaw-specific execution step is required. First re-enumerate comparable persistent-assistant chassis for NAIA. Reuse this qualification if OpenClaw remains relevant; execute `OC-NAYA-001` only if a material unresolved delta still matters after that comparison.
