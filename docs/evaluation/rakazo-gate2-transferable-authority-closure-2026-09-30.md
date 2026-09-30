# Rakazo Gate-2 transferable authority closure — 2026-09-30

## Candidate

`elie222/rakazo@f4583525d632fcd8643fd6e24c7f51e3e04cb990`

## Exact-pin hosted execution

The exact-pin CI workflow is globally red because the Web E2E job has one failing onboarding UX test.

Other exact-pin jobs are green:

```text
Typecheck = SUCCESS
Lint = SUCCESS
Production builds = SUCCESS
Postgres journeys = SUCCESS
Unit tests = SUCCESS
Web E2E = FAILURE (1 failing test)
```

The sole observed Web E2E failure is:

```text
new-bot-ux.spec.ts
later bot waits before showing the focus card; sending cancels it
expected focus card count 0, observed 1
```

This is an onboarding timing/UI failure, not an authority/isolation failure.

## Run-backed Gate-2 evidence inside the same exact-pin E2E run

The same executed Web E2E job records successful tests for:

- durable approval resume;
- consequential-action behavior;
- MCP approval card persistence;
- screen-proxy isolation;
- Spaces invisibility/default isolation;
- chat creation requiring approval;
- browser-auth flow;
- failed computer-control recovery.

In particular:

```text
approval input resumes durable work = PASS
consequential-approval scenario = PASS
MCP approval card persists after remount = PASS
screen response isolation = PASS
spaces invisible by default = PASS
chat creation requires approval = PASS
```

The exact-pin unit and Postgres journey jobs are independently green.

Therefore the overall red workflow must not erase individually executed passing authority evidence.

## Transferable Gate-2 clauses

Combined with the existing transfer audit:

```text
APPROVAL_RESUME_PATH = PASS_UPSTREAM_EXACT_PIN
SCREEN_PROXY_ISOLATION = PASS_UPSTREAM_EXACT_PIN
SPACE_PRIVACY_BOUNDARY = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
APPROVAL_UI/PERSISTENCE_SURFACE = EXECUTED
POSTGRES_JOURNEYS = PASS
UNIT_TESTS = PASS
```

The default consequential-action policy remains permissive unless explicit confirmation rules are configured. That is a known hardening residual, not contradicted by the passing E2E.

## Remaining Atento-specific residual

```text
consequential-action confirmation rules = explicit hardened policy
NAIA and Anna = separate Spaces / Private Computers / credential scopes
Team Computer = forbidden as security boundary
peer/handoff path = explicit Atento broker only
background/routine authority <= interactive hardened authority
external-effect uncertain-state/reconciliation retained
```

## Gate-2 disposition

```text
RAKAZO_EXACT_PIN_AUTHORITY_EVIDENCE = PASS_WITH_SCOPE
RAKAZO_GLOBAL_CI = RED_DUE_TO_UNRELATED_ONBOARDING_E2E
RAKAZO_GATE2_RESIDUAL = HARDENED_RULES + ROLE_COMPOSITION
RAKAZO_FRONTIER_ELIGIBLE = YES

RAKAZO_CURRENT_PIN_QUALIFIED = NO
```

No broad Rakazo rerun is justified for Gate 2.
