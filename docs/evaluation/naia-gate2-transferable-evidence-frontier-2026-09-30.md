# NAIA Gate-2 transferable-evidence frontier — 2026-09-30

## Purpose

Identify which frozen candidates have enough **exact-pin executed authority/isolation evidence** to justify proceeding directly to an Atento-specific hardened composition test.

This is not a shortlist, rank or base selection.

## Admission rule

A candidate enters this frontier only when:

1. exact-pin hosted execution is observed;
2. the executed suite includes source tests directly relevant to Gate-2 authority/isolation clauses;
3. those clauses transfer unchanged to the proposed hardened Atento composition;
4. the remaining uncertainty is primarily the Atento-specific two-role topology, not generic upstream behavior.

## Frontier result

```text
TRANSFERABLE_EVIDENCE_FRONTIER = COMPLETE_V1

ADMITTED:
  AI Butler
  AgentOS

NOT_ADMITTED_YET:
  OpenClaw
  QwenPaw
  all other current technical survivors

THIS_IS_NOT = shortlist | ranking | selection
```

## AI Butler

Canonical evidence:

`docs/evaluation/aibutler-gate2-transferable-authority-closure-2026-09-30.md`

Exact-pin executed clauses include:

- memory-bank negative isolation;
- capability subset monotonicity;
- technical capability denial;
- credential broker default-deny;
- scoped scheduler capability authority;
- shell/sandbox tests.

Residual:

```text
AI_BUTLER_GATE2 = ONE_ATENTO_TWO_ROLE_COMPOSITION_RESIDUAL
```

## AgentOS

Canonical evidence:

`docs/evaluation/agentos-gate2-transferable-authority-closure-2026-09-30.md`

Exact-pin hosted CI executed on Linux and Windows:

```text
Linux   = 16774 passed
Windows = 16701 passed
frontend = 2382 passed
```

Transferable clauses include:

- session-scoped shell approval behavior;
- cross-session cached approval denial in tested path;
- hardened cron unelevated mode;
- interactive elevation not leaking into cron with cron default off;
- cron tool-profile write validation;
- sensitive host credential-path guards;
- browser policy test surface.

Residual:

```text
AGENTOS_GATE2 =
  ATENTO_TWO_ROLE_COMPOSITION
  + EXPLICIT_BROWSER_POLICY_DOMAIN
```

## Why OpenClaw is not admitted yet

Exact-pin CI is observed, but the exact push run executed only `security-fast`; the main preflight/core/QA lanes relevant to the A2A and two-runtime authority composition were skipped.

Therefore:

```text
OPENCLAW_EXACT_PIN_REPOSITORY_HEALTH = PASS_WITH_SCOPE
OPENCLAW_GATE2_TRANSFERABLE_EXECUTED_AUTHORITY = INSUFFICIENT_FOR_FRONTIER
```

This is not a candidate failure.

## Why QwenPaw is not admitted yet

Exact-pin Actions evidence includes successful E2E UI smoke, frontend/pre-commit and CodeQL, but:

```text
principal Tests workflow = WAITING
Full Tests Nightly = FAILURE
```

The observed successful workflows do not close sandbox-fallback and cron-authority clauses.

Therefore:

```text
QWENPAW_GATE2_TRANSFERABLE_EXECUTED_AUTHORITY = INSUFFICIENT_FOR_FRONTIER
```

This is not a structural elimination.

## Gate state

```text
FROZEN_UNIVERSE = 26
TECHNICAL_ELIMINATED = [SelfAgent]
TECHNICAL_SURVIVORS = 25

TRANSFERABLE_EVIDENCE_FRONTIER_COUNT = 2
TRANSFERABLE_EVIDENCE_FRONTIER = [AI Butler, AgentOS]

NEXT_EMPIRICAL_COMPOSITION_TARGET = AI Butler
SECOND_READY_COMPOSITION_TARGET = AgentOS

AUTHORITY_ISOLATION_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

Execution order is evidence-minimizing only:

- AI Butler has one residual two-role composition test;
- AgentOS has the same role-composition residual plus a separate browser-policy domain.

No comparative performance conclusion is implied.

## Next execution rule

Do not rerun broad upstream suites for either frontier candidate.

Execute only the frozen Atento composition negatives.

If local exact-pin material remains unavailable because the executor cannot resolve GitHub, preserve:

```text
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
```

and continue evidence reconciliation without claiming Gate-2 empirical PASS.
