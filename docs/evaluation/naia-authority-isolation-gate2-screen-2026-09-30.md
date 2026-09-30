# NAIA authority/isolation Gate 2 screen — 2026-09-30

## Contract

This record performs the authority/isolation **screen** for every Gate-1 survivor using already-canonical exact-pin evidence.

It does not claim that Gate 2 is empirically passed, create a shortlist, rank candidates, or select `NAIA_BASE`.

Inputs:

- `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`
- `docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md`
- `docs/evaluation/naia-static-residual-disposition-2026-09-30.md`
- candidate-specific exact-pin/transfer/exhaustive verification records

Rules:

```text
VENDOR_DEFAULT != HARDENED_PROFILE
AUTHORITY_MECHANISM_PRESENT != AUTHORITY_PROPERTY_PROVEN
WORKSPACE_ISOLATION != ROLE_AUTHORITY_ISOLATION
MULTI_AGENT != BROKER_ONLY_HANDOFF
PROMPT_APPROVAL != TECHNICAL_DENIAL
BACKGROUND_AUTHORITY must be <= INTERACTIVE_AUTHORITY
AUTHORITY_CONTROL_FAILURE must FAIL_CLOSED
```

## Screen result

Gate 1 left 25 candidates.

All 25 have now been screened against the fixed authority/isolation invariants.

```text
GATE_2_SCREENED = 25_OF_25
VENDOR_DEFAULT_AUTHORITY_PASS = 0
CURRENT_PIN_AUTHORITY_ISOLATION_QUALIFIED = 0
ADDITIONAL_STRUCTURAL_STOPS_AT_STATIC_SCREEN = 0

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

This is a substantive negative result: **there is no defensible candidate that can be promoted from its current vendor/default profile directly into Gate 3.**

Every survivor requires one of:

- a frozen hardened composition;
- an exact external dependency profile;
- or one exact changed-contract upstream check before composition.

That does **not** mean all 25 need a broad runtime battery.

## Why no new candidate is eliminated yet

The architecture-first policy eliminates a candidate when the required authority/isolation invariants cannot be represented without a cross-cutting structural rewrite.

For the 25 Gate-1 survivors, the current evidence still exposes at least one bounded route through:

- an existing central policy/tool chokepoint;
- per-agent/project/profile/container separation;
- a separate runtime/store/home topology;
- a bounded browser/tool adapter;
- or an exact external dependency boundary.

Several candidates have serious unsafe defaults. Those defaults are already known and are not worth rerunning. They become elimination evidence only if the smallest hardened composition still cannot enforce the invariant without structural reconstruction.

This preserves:

```text
KNOWN_PERMISSIVE_DEFAULT != ARCHITECTURAL_IMPOSSIBILITY
COMPOSE_FIRST != PASS
COMPOSE_FIRST != FAIL
```

## Per-candidate disposition

| Candidate | Authority/isolation screen | Main unresolved invariant | Smallest allowed next proof |
|---|---|---|---|
| OpenClaw | COMPOSE_FIRST | strict NAIA/Anna authority requires separate runtime/Gateway domains; fail-closed NAIA policy must be frozen | hardened profile + two-role negative isolation |
| OpenMausBot | UPSTREAM_FIRST_THEN_COMPOSE | same-owner role isolation remains unproven; changed exact-pin auth/session evidence must be reused first | only changed-contract evidence if material, then composition |
| QwenPaw | COMPOSE_FIRST | sandbox-unavailable path must not become unsandboxed ALLOW; cron authority must not broaden | fail-closed sandbox/cron profile + role isolation |
| AI Butler | COMPOSE_FIRST | strict NAIA/Anna role/bank/channel topology not yet proven at target deployment | role/bank topology + one scheduled capability/credential path |
| NanoClaw | COMPOSE_FIRST | exact capability recipe determines actual authority and maintenance surface | one channel+gateway+provider+schedule+memory recipe |
| TrustClaw | DEPENDENCY_FIRST | effective external-effect authority and sandbox live in Composio/provider seams | freeze dependency profile, then authority/unavailability check |
| Open Assistant | COMPOSE_FIRST_HIGH_HARDENING | no local per-action gate; credential scope is global-by-service; strict role boundary absent | central effect gate + separated role stores/credentials |
| Suna | COMPOSE_FIRST | connector default allow and shared project-brain semantics must not cross roles | explicit deny/risk profile + separated projects |
| Letta Code | COMPOSE_FIRST | unrestricted defaults/shared discovery/memory and optional shell confinement must be closed | strict permissions + role-separated runtime/memory |
| PersonalJarvis | COMPOSE_FIRST | strict role credential scope remains unestablished | role credential/runtime topology + background grant parity |
| Rakazo | COMPOSE_FIRST | consequential-action default is permissive; Team Computer is not security boundary | rules + separate Spaces/Private Computers/runtime |
| Gobii | COMPOSE_FIRST | contact/email review policy and org/global grants must not create silent cross-role authority | role grants + brokered peer path |
| Octop | COMPOSE_FIRST | HITL off/tool guard warn; cron may inherit default-open connectors | fail-closed profile + explicit cron connectors + role topology |
| Agent Zero | COMPOSE_FIRST | default local/MCP allow; instance-wide plugin/OAuth/host-CUA domains sit outside project isolation | block-by-default profile + separate role projects + global-surface audit |
| Rome | COMPOSE_FIRST | approval is per-action metadata; capability autoapproval and provider-native bypass must be closed | two profiles + universal consequential-action coverage for chosen toolset |
| OpenGrokBot | COMPOSE_FIRST_HIGH_HARDENING | browser can perform outward effects without the hold gate; routines use full toolset | technical browser/shell effect mediation + narrowed routine policy |
| GoClaw | COMPOSE_FIRST | instance-global BM25/Cortex and broad ask_agent target set | separate role data/runtime + disable/broker delegation + narrow shell |
| Nebo | COMPOSE_FIRST | system-origin work auto-approves ordinary requests | background/system-origin authority parity + separate role domains |
| AutoMate | COMPOSE_FIRST | requireApproval enforcement not established; elevated shell can bypass dangerous-pattern checks; shared memory exists | deny-by-default + bounded elevation + no shared role memory |
| AgentOS | COMPOSE_FIRST | interactive and cron default to bypass; browser is outside ordinary process sandbox | narrow interactive+cron policy + explicit browser policy |
| OpenAgentd | COMPOSE_FIRST_HIGH_HARDENING | default PermissionService is AutoAllow; trusted-host shell model; strict role boundary absent | blocking ruleset + hardened shell + separate role domains |
| HubOS | COMPOSE_FIRST_HIGH_HARDENING | guard exceptions are fail-open; no-session guarded findings may execute; native collaboration is broad | fail-closed guard + background authority context + broker-only role topology |
| RustFox | COMPOSE_FIRST_HIGH_HARDENING | supervisor is not established as universal effect owner; shared USER memory and peer invocation exist | universal effect mediation + role-separated memory/grants + broker-only peer path |
| Engram | COMPOSE_FIRST_WITH_EXISTING_BOUNDED_EXECUTION | existing egress model does not cover all trusted/browser consequential effects; shared ENGRAM_HOME cannot be role boundary | separate role runtime/home + only decision-relevant effect-authority seam |
| Holt | DEPENDENCY_FIRST | selected CLI brain/provider owns effective interactive/noninteractive authority; credentials/channels are otherwise global | freeze brain/provider permission profile + separate credential/channel domains |

SelfAgent is not listed because Gate 1 already stopped it as a complete base candidate at its frozen pin.

No row is a rank, score, tier, recommendation, finalist designation or qualification.

## Structural-risk observations

The highest-hardening cases at this screen are descriptive, not eliminations:

```text
Open Assistant:
  central per-action authority absent
  + global-by-service credential scope

OpenGrokBot:
  outward browser effect can bypass approval discipline
  + routines inherit full toolset

OpenAgentd:
  AutoAllow default
  + trusted-host shell model

HubOS:
  guard-decision exceptions fail open
  + headless/no-session approval path can fall through

RustFox:
  supervisor not proven universal effect owner
  + shared install-wide USER memory
```

For these candidates, the first composition check is decisive: if the hardened profile requires touching multiple independent execution paths rather than one chokepoint/adapter, classify the result as `CROSS_CUTTING_STRUCTURAL_REWRITE` and stop immediately.

## Gate 2 execution rule

The static screen is complete, but empirical Gate 2 is intentionally not marked PASS.

A candidate may close Gate 2 only when its exact hardened composition/dependency proves the relevant subset of:

```text
DENIED_ACTION = DENIED_TECHNICALLY
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
DELEGATION_AUTHORITY <= CALLER_AUTHORITY
CREDENTIAL_BOUNDARY = TECHNICALLY_ENFORCED
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED

CROSS_MEMORY_READ = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

Existing exact-pin tests can close individual clauses when the Atento composition does not alter the relevant boundary.

## State after screen

```text
AUTHORITY_ISOLATION_STATIC_SCREEN = COMPLETE_V1
AUTHORITY_ISOLATION_SCREENED = 25_OF_25
AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
ADDITIONAL_GATE_2_STOPS = 0

GENERIC_VENDOR_DEFAULT_RETEST = FORBIDDEN_AS_LOW_VALUE
GENERIC_25_CANDIDATE_RUNTIME_BATTERY = NOT_JUSTIFIED

NEXT_WORK =
  freeze only decision-relevant hardened compositions/dependencies;
  reuse exact-pin clauses already proved;
  execute the smallest missing negative authority/isolation checks;
  stop immediately if the composition reveals cross-cutting structural authority repair.
```
