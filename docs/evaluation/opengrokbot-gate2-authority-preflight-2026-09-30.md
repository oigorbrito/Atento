# OpenGrokBot Gate-2 authority preflight — 2026-09-30

## Question

Does the known browser/outward-action approval bypass require a cross-cutting structural rewrite, or can it be closed at a bounded execution chokepoint?

Candidate pin:

`wolfqing/OpenGrokBot@43ba51fc0487b7adbb23861a1062a113390833d9`

## Exact-pin finding

The exact source confirms the documented gap:

```text
hold_for_approval = workflow discipline
browser can click/type directly
routines use full toolset
```

However, the execution architecture has a central dispatch path:

`runTurn -> execToolCall -> execComputerTool`

The exact `execToolCall()` path receives all computer tools including:

- shell
- browser_goto
- browser_click
- browser_type
- browser_press
- write_file

and routines execute through the same `runTurn` tool dispatch.

Therefore a technical effect-authority gate can be inserted at this central boundary without first modifying every browser adapter, every routine implementation, and every channel independently.

## Classification

```text
KNOWN_APPROVAL_BYPASS = YES
PROMPT_ONLY_POLICY = INSUFFICIENT
CENTRAL_EFFECT_CHOKEPOINT = PRESENT
ROUTINES_SHARE_CHOKEPOINT = YES

REPAIR_CLASS = LOCALIZED_REPAIR_OR_COMPONENT_MIDDLEWARE
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
ELIMINATE_AS_COMPLETE_BASE = NO
OPEN_GROKBOT_GATE2 = NOT_CLOSED
```

This does not prove that the repair works. It only prevents an unsupported architectural elimination.

## Smallest next evidence if still decision-relevant

Implement/freeze one technical policy wrapper at `execToolCall` and prove:

1. browser read/navigation remains allowed as configured;
2. browser click/type classified as consequential is denied or held technically;
3. shell/write effects follow the same authority owner;
4. routine/background invocation cannot bypass the wrapper;
5. approval-control failure denies rather than executes;
6. per-bot workspace/browser isolation remains unchanged.

If this cannot be achieved without branching policy into multiple independent execution paths, reclassify to `CROSS_CUTTING_STRUCTURAL_REWRITE` and eliminate.
