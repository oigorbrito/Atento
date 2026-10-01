# NAIA Gate-2 hosted-runner execution block — 2026-09-30

## Scope

This record attributes the failed hosted AI Butler composition workflow.

Workflow:

`NAIA Gate2 AI Butler Composition`

Run:

```text
run_id = 36789543149
head_sha = f5ea26ac9e9b3d9deb7382fffb49a9ce2fbec3f1
```

Two attempts were observed.

### Attempt 1

```text
job_id = 110138936806
runner_id = 0
steps = []
started_at = 2026-09-30T23:08:57Z
completed_at = 2026-09-30T23:08:58Z
conclusion = failure
```

### Attempt 2

```text
job_id = 110147437098
runner_id = 0
steps = []
started_at = 2026-09-30T23:39:19Z
completed_at = 2026-09-30T23:39:20Z
conclusion = failure
```

## Attribution

No workflow step executed in either attempt.

Therefore the failed run provides no evidence about:

- AI Butler checkout;
- exact-pin verification;
- Go setup;
- test compilation;
- ISO-1..ISO-6;
- any candidate property.

```text
HOSTED_RUNNER_PROVISIONING = BLOCKED
WORKFLOW_STEPS_EXECUTED = 0
AI_BUTLER_ASSERTIONS_EXECUTED = 0

RUN_FAILURE_CLASS = BLOCKED_ENVIRONMENT
AI_BUTLER_FAIL = NOT_CLAIMED
HARNESS_FAIL = NOT_CLAIMED
```

The earlier local executor block and this hosted-runner block are distinct infrastructure failures:

```text
LOCAL_EXECUTOR:
  github.com DNS unavailable

GITHUB_ACTIONS:
  runner_id = 0
  no steps scheduled/executed
```

## Consequence

```text
AI_BUTLER_GATE2_COMPOSITION = BLOCKED_ENVIRONMENT
GATE2_EMPIRICAL_PASS = 0
CANDIDATE_STATE_CHANGE = NONE
```

Do not repair candidate code or the injected Go test based on this run because the test never executed.

## Harness implementation progress

The common result-classification logic now exists as executable AtentoEval code:

- `evals/atentoeval/gate2_composition.py`
- `evals/tests/test_gate2_composition.py`

It enforces:

```text
PASS_WITH_SCOPE
FAIL_LOCALIZED
FAIL_STRUCTURAL
BLOCKED_ENVIRONMENT
INVALID_EVIDENCE
```

and preserves the rule:

```text
environment block != candidate failure
```

The module requires full candidate identity, exact 40-character upstream SHA, policy/profile identity and all six common ISO assertions before a PASS is possible.

## Resume condition

Resume the hosted AI Butler workflow only when a GitHub Actions runner is actually assigned.

Acceptance prerequisite before interpreting candidate evidence:

```text
runner_id != 0
steps != []
exact-pin checkout step executed
go test step executed
```

Until then, rerunning the same workflow is infrastructure retry only and cannot change candidate status.
