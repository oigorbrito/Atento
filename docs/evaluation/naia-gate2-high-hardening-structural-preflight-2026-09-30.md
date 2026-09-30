# NAIA Gate-2 high-hardening structural preflight — 2026-09-30

## Purpose

Resolve the five Gate-2 candidates previously marked as the highest structural-hardening risk:

- Open Assistant
- OpenGrokBot
- OpenAgentd
- HubOS
- RustFox

Question:

> Does the required NAIA authority/isolation hardening already imply a cross-cutting structural rewrite, or does an existing bounded execution/policy seam remain available?

This is not a qualification or ranking exercise.

## Result

```text
HIGH_HARDENING_PREFLIGHT = COMPLETE_V1
CANDIDATES_SCREENED = 5_OF_5
NEW_STRUCTURAL_ELIMINATIONS = 0
LOCALIZED_OR_BOUNDED_HARDENING_PATH = 5_OF_5

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

The result is deliberately conservative: serious unsafe defaults are not converted into structural failure when the exact pin still exposes a bounded authority owner or a clean separate-runtime composition.

## Open Assistant

Pin:

`open-assistant-org/open-assistant@32c55d2643f9fe38777f9212588b2eee45392514`

Exact source exposes a central `ToolExecutor.execute_tool()` path used to route:

- registered integration tools;
- plugin tools;
- MCP tools;
- browser/service tools;
- scheduled pinned-tool execution through the same ToolExecutor authority surface.

The current pin lacks a repository-owned per-action approval/deny policy, and credentials are global by `service_name`.

However, a technical policy middleware can be inserted at `ToolExecutor.execute_tool()` before plugin/MCP/service dispatch. Strict NAIA/Anna memory and credential separation can be obtained through separate process/database/credential-store composition rather than rewriting the executor architecture.

```text
CENTRAL_EFFECT_EXECUTOR = PRESENT
BACKGROUND_PINNED_TOOL_REUSES_EXECUTOR = YES_BY_CURRENT_AUDIT
PER_ACTION_AUTHORITY = ABSENT_BY_DEFAULT
ROLE_STORE_SCOPE = GLOBAL_IN_ONE_RUNTIME

REPAIR_CLASS = LOCALIZED_EXECUTOR_MIDDLEWARE + SEPARATE_RUNTIME_STORE
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
OPEN_ASSISTANT = SURVIVES_STRUCTURAL_PREFLIGHT
```

## OpenGrokBot

Canonical candidate preflight:

`docs/evaluation/opengrokbot-gate2-authority-preflight-2026-09-30.md`

Exact source routes ordinary computer effects through:

`runTurn -> execToolCall -> execComputerTool`

and routines reuse the same turn/tool dispatch.

```text
KNOWN_BROWSER_APPROVAL_BYPASS = YES
CENTRAL_EFFECT_CHOKEPOINT = PRESENT
ROUTINES_SHARE_CHOKEPOINT = YES

REPAIR_CLASS = LOCALIZED_REPAIR_OR_COMPONENT_MIDDLEWARE
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
OPENGROKBOT = SURVIVES_STRUCTURAL_PREFLIGHT
```

## OpenAgentd

Pin:

`TBNRFPS01/OpenAgent@b2acf236f4e9e6b503281f2364e9915a60158376`

Exact source shows:

- a real blocking `PermissionService` with allow/deny/ask rules;
- the shipped default falls back to `AutoAllowPermissionService`;
- all run tools are executed through a single per-run tool-chain:
  `build_tool_chain(combined_hooks, make_tool_executor(...))`;
- every tool dispatch invokes that chain through `_run_tool(..., tool_chain)`.

Therefore the default permission mode is unsafe for NAIA, but a blocking authority hook can be composed into the universal run-local tool chain without rewriting each individual tool implementation.

Strict NAIA/Anna separation should use separate authority/runtime domains instead of the native lead/member collaboration topology.

```text
BLOCKING_PERMISSION_ENGINE = PRESENT
DEFAULT_PERMISSION = AUTO_ALLOW
UNIVERSAL_RUN_TOOL_CHAIN = PRESENT
HOOKABLE_PRE_EXECUTION_BOUNDARY = PRESENT

REPAIR_CLASS = LOCALIZED_POLICY_HOOK + SEPARATE_RUNTIME_DOMAIN
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
OPENAGENTD = SURVIVES_STRUCTURAL_PREFLIGHT
```

## HubOS

Canonical candidate preflight:

`docs/evaluation/hubos-gate2-authority-preflight-2026-09-30.md`

The exact pin exposes:

`HubOSAgent -> ToolGuardMixin._acting -> ReActAgent._acting`

Known gaps — non-blocking guard exceptions, sessionless findings falling through, and risk/finding-based rather than universal effect policy — all occur at the same central pre-tool interception layer.

```text
CENTRAL_PRE_TOOL_GUARD = PRESENT
FAIL_OPEN_GAPS = PRESENT
BACKGROUND_SESSIONLESS_GAP = PRESENT

REPAIR_CLASS = LOCALIZED_GUARD_POLICY_REPAIR
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
HUBOS = SURVIVES_STRUCTURAL_PREFLIGHT
```

## RustFox

Pin:

`chinkan/RustFox@6e24388d36d1c6fac399039d8cab07cd9cb8264b`

Exact source distinguishes two execution domains:

1. ordinary agent tools through central `ToolRegistry.execute()`;
2. supervisor jobs through the supervisor policy/orchestrator/backend path.

The supervisor already supports configurable approval thresholds, while ordinary tools currently lack the same universal effect-authority contract.

This is more than a one-line config delta, but it is still representable with bounded authority owners:

- add/freeze policy at `ToolRegistry.execute()`;
- tighten existing supervisor policy;
- use separate RustFox homes/runtimes for NAIA and Anna;
- disable or broker peer invocation.

No evidence yet requires patching every tool, scheduler, provider and channel independently.

```text
ORDINARY_TOOL_CHOKEPOINT = ToolRegistry.execute
SUPERVISOR_POLICY_OWNER = PRESENT
TWO_EFFECT_DOMAINS = YES
SEPARATE_RUNTIME_ROLE_BOUNDARY = AVAILABLE_AS_COMPOSITION

REPAIR_CLASS = TWO_BOUNDED_AUTHORITY_OWNERS + SEPARATE_RUNTIME
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
RUSTFOX = SURVIVES_STRUCTURAL_PREFLIGHT
```

RustFox carries higher composition complexity than a single-chokepoint candidate, but this document does not rank candidates and does not treat complexity alone as elimination.

## Consequence

The high-hardening label is now resolved as a structural-preflight concern, not an elimination status.

```text
HIGH_HARDENING != STRUCTURAL_FAIL
UNSAFE_DEFAULT != STRUCTURAL_FAIL
MULTIPLE_BOUNDED_COMPONENTS != CROSS_CUTTING_REWRITE
```

The only technical structural elimination in the frozen universe remains SelfAgent at its frozen pin.

License remains out of scope for technical selection.

## Gate-2 state

```text
FROZEN_UNIVERSE = 26
TECHNICAL_GATE1_ELIMINATED = [SelfAgent]
TECHNICAL_GATE2_SURVIVORS = 25

HIGH_HARDENING_STRUCTURAL_PREFLIGHT = COMPLETE_V1
HIGH_HARDENING_STRUCTURAL_STOPS = 0

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## Next evidence rule

Do not spend broad runtime budget on these five candidates.

Their next test, only if decision-relevant, is the smallest hardened composition proving the authority owner actually denies the relevant negative cases:

- authority-control failure;
- background/sessionless execution;
- cross-role memory/credential/tool access;
- silent peer invocation;
- restart authority broadening.

If a candidate's bounded hardening implementation later fans out into multiple independent execution paths beyond the owners identified here, reclassify at that point as `CROSS_CUTTING_STRUCTURAL_REWRITE` and eliminate.
