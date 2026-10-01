# System chassis first-sieve execution status — 2026-10-01

## Decision and scope

This record applies the bounded sequential protocol in `atento-system-architecture-chassis-rescreen-2026-09-30.md` and `harness.md`. It records what was executable in this session, reuses existing evidence, and does not convert absent evidence into a pass or failure.

The user requested a mobile-focused chassis view retaining AI Butler, NanoClaw, and QwenPaw while treating OpenClaw as too large for that view. This is a focus cohort, not a measured rank or a chassis selection. OpenClaw remains in the fixed 11-candidate system comparison cohort; this note does not silently remove it from that protocol.

## Execution outcome

```text
LOCAL_ATENTO_CHECKOUT_AVAILABLE = NO
CANDIDATE_NEUTRAL_RUNNER = NOT_IMPLEMENTED (per frozen protocol record)
NEW_CANDIDATE_TESTS_EXECUTED = 0
EXISTING_EVIDENCE_REUSED = YES, WITH_SCOPE_LIMITS
STATUS = BLOCKED_BEFORE_EXECUTION
BLOCKED_CANDIDATE_COUNT = 11
COMPARABLE_SYSTEM_CHASSIS_COST_MEASUREMENTS = 0
```

The current workspace did not contain an Atento checkout. The frozen protocol also records that the candidate-neutral runner is not implemented. Therefore no candidate could be executed serially here. No upstream suite, external benchmark, or already-recorded Atento test was repeated. This is an execution blocker, not a candidate failure.

The protocol permits at most one primary run and one targeted confirmation per candidate, after evidence reconciliation. When execution infrastructure is available, continue in the frozen cohort order and capture only uncovered Atento deltas. Do not rerun published benchmarks or equivalent applicable tests.

## Reused evidence for the mobile-focused cohort

| Candidate | Existing evidence reused | What it does not establish for the chassis comparison |
|---|---|---|
| AI Butler | Exact-pin CI and bank/scheduler evidence; earlier Atento Gate 2 result was 6/6 common assertions, marked `PASS_WITH_SCOPE`; exact-pin live eval is 4/7 on its own seven-task suite. | The 6/6 result is not the full three-role system composition. A later scheduled scan records seven reachable advisories at this pin, with no repaired-pin regression recorded. The live eval is not comparable to PawBench. No comparable total adaptation/maintenance cost. |
| NanoClaw | Exact-pin core CI: 513 passed, 0 failed, 3 skipped; existing Atento hosted run: 7/7 assertions with scope; partial static touchpoint counts exist for WhatsApp, OneCLI, and OpenCode. | The hosted result is not a full three-role acceptance run. Recipe touchpoints are partial static change-surface evidence, not elapsed or lifecycle cost. No comparable total cost. |
| QwenPaw | Reuse PawBench v1.0 mean 73.7 for the published release; existing exact-pin source/CI review is retained with its recorded status. | PawBench is a capability benchmark, not a chassis-cost or Atento-isolation result. The inspected sandbox fallback and cron authority gaps remain unresolved for this comparison. No comparable total cost. |

Scores and test results remain on their own scales and exact pins. They do not become a composite chassis score.

## Requested Top 3 and protocol-eligible Top 3

The requested mobile-focused comparison group is recorded as:

| Focus group | Candidate | Current chassis-cost evidence | Protocol status |
|---:|---|---|---|
| A | AI Butler | No comparable three-role adaptation/maintenance cost | Not eligible for a measured Top 3 |
| B | NanoClaw | Partial static touchpoints only; no comparable total cost | Not eligible for a measured Top 3 |
| C | QwenPaw | No comparable three-role adaptation/maintenance cost | Not eligible for a measured Top 3 |

These labels preserve the user's requested focus; they are not rank positions. Under the frozen rule, a provisional Top 3 may contain only completed hard-gate passes with comparable cost evidence. Current eligible count is zero:

```text
REQUESTED_MOBILE_FOCUS_GROUP = [AI Butler, NanoClaw, QwenPaw]
PROTOCOL_ELIGIBLE_CANDIDATES = 0
PROVISIONAL_CHASSIS_TOP_3 = NOT_ESTABLISHED
CHASSIS_WINNER = NONE
```

OpenClaw is excluded from the mobile-focused view by user direction because it is considered too large for that objective. No proportional size measurement was captured here, so this is a recorded product constraint, not an independently measured size finding. Its published PawBench score remains reusable only for PawBench and its fixed-cohort system comparison slot is unchanged.

## Next executable step

Before claiming a Top 3, make the candidate-neutral runner available or provide an equivalent execution environment, then run the frozen protocol serially. Start each candidate with the missing cost dimensions, reuse exact-pin evidence, and execute only uncovered Atento-specific assertions. Keep `BLOCKED` distinct from `FAIL`; do not fabricate a total-cost scalar. A candidate enters the provisional Top 3 only after it has both comparable cost evidence and completed applicable hard gates.

