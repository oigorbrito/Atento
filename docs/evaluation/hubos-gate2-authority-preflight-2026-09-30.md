# HubOS Gate-2 authority preflight — 2026-09-30

## Question

Do HubOS's known authority gaps require a cross-cutting structural rewrite, or can they be closed through its existing central pre-tool guard?

Candidate pin:

`hubos-ai/HubOS@7c14b14ed1d26c3d1b597cc213cf97ddfbb7cdcb`

## Exact-pin finding

HubOS already owns a central pre-execution interception path:

```text
HubOSAgent -> ToolGuardMixin._acting -> ReActAgent._acting
```

The mixin serializes the guard decision before delegating to the parent execution path.

Known unsafe behavior at the exact pin:

1. exceptions in `_decide_guard_action` are logged as non-blocking and then execution falls through;
2. findings require a `session_id` to enter the approval path; without one, execution may fall through;
3. the default guardian model is risk/finding based, not a universal consequential-effect policy.

But these failures occur at the same central interception layer rather than in many independent adapters.

The engine already supports:

- guarded tool sets;
- denied tool sets;
- pluggable guardians;
- global enablement;
- exact approval replay;
- unconditionally denied tools.

Therefore the smallest hardened implementation can be tested at one authority owner:

```text
ToolGuardMixin._acting / _decide_guard_action
```

rather than rewriting every downstream tool.

## Classification

```text
CENTRAL_PRE_TOOL_GUARD = PRESENT
FAIL_OPEN_ON_GUARD_EXCEPTION = YES
SESSIONLESS_FINDING_CAN_FALL_THROUGH = YES
UNIVERSAL_EFFECT_POLICY = NOT_DEFAULT

REPAIR_CLASS = LOCALIZED_REPAIR_OR_GUARD_POLICY_COMPONENT
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
ELIMINATE_AS_COMPLETE_BASE = NO
HUBOS_GATE2 = NOT_CLOSED
```

## Smallest next empirical test if still decision-relevant

Freeze one hardened ToolGuard policy and prove:

1. guard exception -> technical deny;
2. no-session/background finding -> technical deny or bounded pre-authorized path;
3. one consequential tool with no regex finding still requires the configured authority;
4. denied tool cannot execute through cron/heartbeat/delegation;
5. background authority is no broader than interactive authority;
6. native multi-agent dispatch cannot cross the NAIA/Anna broker boundary.

If these require bypass-specific patches outside the central guard/runner boundary, reclassify the repair as structural and stop.
