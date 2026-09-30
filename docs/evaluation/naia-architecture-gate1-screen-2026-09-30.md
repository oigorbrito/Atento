# NAIA architecture-first Gate 1 screen — 2026-09-30

## Contract

This record closes the first architecture/chassis screen defined by:

- `docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md`
- `docs/adr/ADR-003-evidence-first-engineering-decision-policy.md`
- `docs/adr/ADR-002-assistant-base-selection.md`
- `docs/evaluation/naia-static-residual-disposition-2026-09-30.md`
- `docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md`

It does not rank candidates, create a shortlist, qualify a current pin, or select `NAIA_BASE`.

The screen asks only whether existing exact-pin evidence already shows that the candidate can proceed to an authority/isolation composition without requiring multiple known cross-cutting structural rewrites.

```text
ARCHITECTURE_SCREEN_PASS != AUTHORITY_PASS
ARCHITECTURE_SCREEN_PASS != ISOLATION_PASS
ARCHITECTURE_SCREEN_PASS != QUALIFIED
ARCHITECTURE_SCREEN_PASS != SHORTLISTED
```

## Decision rule

Advance when the required structural properties can still be represented through existing candidate boundaries, configuration, supported extension seams, separate runtime/store composition, or one bounded dependency seam.

Stop as a complete NAIA base candidate when exact-pin evidence already requires several core architectural repairs before the candidate can even represent the required Atento contract.

Material code-change gaps continue to use:

```text
LOCALIZED_REPAIR
COMPONENT_REPLACEMENT
CROSS_CUTTING_STRUCTURAL_REWRITE
```

A separate runtime/store deployment is recorded as a topology/composition cost; it is not automatically treated as a core rewrite when the candidate can be deployed that way without replacing its internal architecture.

## Gate 1 result

```text
FROZEN_CANDIDATE_UNIVERSE_V1 = 26
ARCHITECTURE_SCREENS_COMPLETE = 26
ADVANCE_TO_GATE_2 = 25
STOP_COMPLETE_BASE_AT_GATE_1 = 1

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The single Gate-1 stop is **SelfAgent as a complete NAIA base candidate at the frozen pin**.

That result is based on the conjunction already established in exact-pin source evidence:

- consequential-action confirmation metadata exists but is not consumed by the central execution path;
- scheduled raw shell bypasses the ordinary terminal/registry authority path;
- persisted scheduler state is not wired to startup reload/re-arm;
- strict NAIA/Anna isolation additionally requires separate runtime/store composition.

Closing those first three properties requires changes across the central execution authority path, background execution path, and scheduler lifecycle rather than a bounded profile or one replaceable component. For the complete-base question this is a `CROSS_CUTTING_STRUCTURAL_REWRITE` burden.

This does not make SelfAgent useless. It remains admissible as reference/donor evidence and may be reconsidered at a materially changed upstream pin.

## Per-candidate Gate 1 disposition

| Candidate | Gate 1 chassis status | Structural/change-cost finding | Evidence scope | Next gate |
|---|---|---|---|---|
| OpenClaw | ADVANCE | product chassis is mature; strict role boundary can be expressed with separate runtime/Gateway authority domains; ordinary product hardening is bounded | exact-pin/current-delta + historical executed evidence | authority/isolation composition |
| OpenMausBot | ADVANCE_WITH_UNRESOLVED_COMPOSITION | broad product chassis and exact-pin CI are established; same-owner NAIA/Anna isolation remains unproven rather than architecturally impossible | exact-pin CI + exhaustive verification | upstream-changed-contract reuse, then authority/isolation |
| QwenPaw | ADVANCE | per-Agent state and policy primitives exist; fail-open sandbox fallback and cron defaults require bounded hardening/profile work | exact-pin static contract | hardened authority/isolation profile |
| AI Butler | ADVANCE | per-bank memory, fail-closed shell, credential broker and persistent scheduler provide usable structural seams | exact-pin static contract | role/bank topology + scheduled authority |
| NanoClaw | ADVANCE | per-group/container isolation and credential gateway are native; integration cost is profile-dependent rather than a core-chassis absence | exact-pin audit + exact-pin CI | freeze one representative composition |
| TrustClaw | ADVANCE_DEPENDENCY_FIRST | local memory/cron chassis is viable but external action/sandbox authority is materially owned by Composio/Vercel/provider seams | exact-pin static + partial hosted evidence | freeze dependency authority boundary |
| Open Assistant | ADVANCE_WITH_HIGH_HARDENING_COST | persistence/scheduler/provider/browser chassis is real; role/credential separation and per-action authority require a composed hardening layer, but unavoidable multi-core rewrite is not yet established | exact-pin static + exact-pin CI | authority/isolation composition; legal gate separate |
| Suna | ADVANCE | per-agent grants, triggers, sandbox/session runtime and release-gate architecture exist; explicit risk policy and role topology remain composition work | exact-pin transfer evidence | hardened authority/isolation composition |
| Letta Code | ADVANCE | long-lived identity/memory, scheduler and permission seams exist; unrestricted defaults/shared modes must be constrained | exact-pin transfer evidence | strict permission/runtime composition |
| PersonalJarvis | ADVANCE | persistent routines, namespaced memory and scheduled preauthorization exist; credential/runtime separation remains bounded composition work | exact-pin transfer evidence | role credential/runtime topology |
| Rakazo | ADVANCE | Space/private-computer boundaries plus approval/replay contracts provide usable chassis primitives | exact-pin transfer evidence | fail-closed authority + strict role composition |
| Gobii | ADVANCE | durable agent state, secret delegation, schedules and eval protocol exist; org/global grants and peer messaging need exact role policy | exact-pin transfer + eval evidence | authority/isolation composition |
| Octop | ADVANCE | multi-user/multi-agent product chassis is real; permissive HITL/tool defaults and connector inheritance are hardening residuals | exact-pin transfer + exhaustive verification | hardened authority/isolation profile |
| Agent Zero | ADVANCE | project-scoped memory/settings and scheduler/browser runtime exist; plugins/OAuth/host-CUA remain separate authority domains | exact-pin transfer evidence | role/profile authority composition |
| Rome | ADVANCE | explicit profile data isolation and approval state machine exist; autoapproval/provider-native bypass require constraint | exact-pin transfer evidence | authority composition including provider seam |
| OpenGrokBot | ADVANCE | per-bot container/workspace is a strong structural boundary; browser/routine effect mediation remains an authority residual | exact-pin transfer evidence | consequential-effect + brokered handoff composition |
| SelfAgent | STOP_COMPLETE_BASE | central approval absent, scheduler bypasses registry, startup re-arm absent; combined repair spans core authority + background + lifecycle | exact-pin admission audit | donor/reference only at this pin; reconsider only after material upstream change |
| GoClaw | ADVANCE | sessions/workspaces and per-agent tool policy are native; global memory/Cortex can be avoided with separate runtime/data domains | exact-pin admission audit | separate memory/runtime + delegation authority |
| Nebo | ADVANCE | one-companion chassis can be composed as separate runtime/data domains; OriginSystem authority is a bounded policy residual | exact-pin admission audit | background parity + role isolation |
| AutoMate | ADVANCE | per-agent memory/session dirs, scheduler reload and policy engine exist; shared memory/elevation/approval enforcement require hardening | exact-pin secondary + transfer audit | deny-by-default + role isolation |
| AgentOS | ADVANCE | persistent product, scheduler and sandbox policy exist; bypass defaults and out-of-sandbox browser need a narrow frozen profile | exact-pin secondary + transfer audit | authority profile + browser boundary |
| OpenAgentd | ADVANCE | persistent product and allow/deny/ask engine exist; AutoAllow/trusted-host defaults require hardening; missing browser is peripheral | exact-pin secondary + transfer audit | blocking ruleset + role domains |
| HubOS | ADVANCE | ToolGuard/approval mechanics and persistent product chassis exist; guard-error/background/default-open surfaces remain hardening residuals | exact-pin secondary + transfer audit | fail-closed authority + role isolation |
| RustFox | ADVANCE | scheduler restore, supervisor policy and SecretBridge provide structural seams; universal effect ownership/role-separated grants remain composition work | exact-pin secondary + transfer audit | authority/isolation composition |
| Engram | ADVANCE_WITH_SCOPE | taint/egress/autonomy/scheduler architecture is structurally useful; separate ENGRAM_HOME/runtime solves shared-home role boundary without rewriting core; browser effect authority remains open | exact-pin transfer + bounded execution | no more execution until a decision-relevant authority residual is named |
| Holt | ADVANCE_DEPENDENCY_FIRST | workspace memory and OS scheduling are viable; effective authority belongs to selected external CLI brain/provider and global credential/channel seam | exact-pin secondary + transfer audit | freeze dependency + separate credential/channel domains |

No row is a rank, score, tier, recommendation or finalist designation.

## Why only one candidate stops here

The architecture-first rule is fail-closed, but it must not convert a configurable unsafe default into an architectural impossibility.

Across the other 25 candidates, existing evidence still shows at least one defensible path using:

- native per-agent/project/profile/container boundaries;
- supported policy/configuration seams;
- separate runtime/store/home deployment;
- a bounded external dependency profile;
- or a replaceable adapter/component.

Those paths may fail Gate 2 or Gate 3. They are not promoted by surviving Gate 1.

SelfAgent is different at the frozen pin because the missing authority and lifecycle properties are not only permissive defaults: the execution and scheduler paths themselves lack the required enforcement/recovery wiring.

## Gate 2 entry classes

Gate 2 must not treat all 25 survivors identically.

```text
UPSTREAM_FIRST:
  OpenMausBot

DEPENDENCY_FIRST:
  TrustClaw
  Holt

COMPOSE_FIRST:
  all other Gate-1 survivors

ADAPT_FIRST:
  SelfAgent  # stopped as complete base at Gate 1
```

The smallest authority/isolation proof remains candidate-specific. Do not run a generic 25-candidate runtime battery.

## State after Gate 1

```text
ARCHITECTURE_GATE_1 = COMPLETE_V1
ARCHITECTURE_SCREENED = 26_OF_26
ARCHITECTURE_SURVIVORS = 25
COMPLETE_BASE_STOPS = [SelfAgent]
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED

NEXT_GATE = AUTHORITY_ISOLATION
NEXT_WORK =
  reuse exact-pin evidence,
  freeze only decision-relevant hardened compositions/dependencies,
  stop immediately on structural authority failure,
  and preserve adaptation cost during the same work.
```
