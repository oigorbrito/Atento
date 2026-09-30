# NAIA Gate-2 empirical composition execution block — 2026-09-30

## Scope

Attempted to start the frozen common composition harness:

`NAIA-GATE2-COMPOSITION-V1`

Initial execution targets:

1. AI Butler
2. OpenMausBot
3. NanoClaw

## Environment observation

The current executor cannot acquire exact upstream pins.

Direct shell probe:

```text
git ls-remote https://github.com/LumabyteCo/aibutler.git HEAD
fatal: unable to access ...
Could not resolve host: github.com
```

A local filesystem scan found no preloaded checkout for:

- Atento
- AI Butler
- OpenMausBot
- NanoClaw

The GitHub connector remains sufficient for source/CI inspection and repository documentation, but it does not provide an executable repository archive into this runtime.

## Classification

```text
EXECUTOR_GITHUB_DNS = BLOCKED
EXACT_PIN_RUNTIME_ACQUISITION = BLOCKED
LOCAL_PRELOADED_CHECKOUT = ABSENT

AI_BUTLER_COMPOSITION = BLOCKED_ENVIRONMENT
OPENMAUSBOT_COMPOSITION = BLOCKED_ENVIRONMENT
NANOCLAW_COMPOSITION = BLOCKED_ENVIRONMENT
```

Because all twelve frontier candidates require exact-pin runtime material for the common composition harness, the same infrastructure precondition blocks execution of the remaining frontier in this executor.

Do **not** duplicate this environmental block twelve times as candidate evidence.

```text
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
BLOCKED_ENVIRONMENT != FAIL_LOCALIZED
BLOCKED_ENVIRONMENT != FAIL_STRUCTURAL
```

## Gate consequence

```text
COMMON_COMPOSITION_HARNESS = FROZEN_V1
COMMON_COMPOSITION_EXECUTION = BLOCKED_ENVIRONMENT
GATE2_EMPIRICAL_PASS = 0

TECHNICAL_CANDIDATE_STATE_CHANGE = NONE
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## Resume condition

Resume composition execution only when at least one of these is true:

1. this executor can resolve/access `github.com` and clone the exact frozen pins;
2. exact candidate checkouts are mounted/preloaded locally;
3. another authorized executable environment exposes the exact pin with reproducible command/log/artifact capture.

On resume, start mechanically at:

```text
NEXT_EXECUTION_TARGET = AI Butler
HARNESS = NAIA-GATE2-COMPOSITION-V1
```

Do not restart upstream evidence reconciliation or broad candidate testing.


## Canonical blocker record

```text
blocker_id = NAIA-G2-EXEC-INFRA-2026-09-30-01
type = executor_network
blocked_operation = exact_pin_runtime_acquisition_for_gate2_composition
impact = 12 frontier candidates blocked from local composition execution
work_continuable = YES
unblock_condition =
  github.com DNS/access restored
  OR exact checkouts preloaded
  OR another authorized executable exact-pin environment is available
```

Machine-readable resume queue:

`docs/evaluation/naia-gate2-composition-execution-queue-v1-2026-09-30.yaml`

The queue freezes exact repository, SHA, execution order, candidate-specific add-ons and `BLOCKED_ENVIRONMENT` status for all twelve frontier candidates. No candidate state changes because of this blocker.


## Hosted-runner attribution

A repository-hosted workaround was attempted for AI Butler:

```text
workflow = NAIA Gate2 AI Butler Composition
run_id = 36789543149
job_id = 110138936806
runner_id = 0
steps = []
duration ≈ 1 second
conclusion = failure
```

Because no runner was assigned and no steps started:

```text
HOSTED_RUNNER_AVAILABLE = NO_FOR_OBSERVED_RUN
CANDIDATE_CODE_EXECUTED = NO
HARNESS_ASSERTIONS_EXECUTED = 0
```

This strengthens the infrastructure-block classification. It is not AI Butler evidence.

Typed result artifact:

`evals/results/naia_gate2_aibutler_blocked_2026-09-30.json`

The evaluation harness now also contains a strict result validator:

- `evals/atentoeval/composition.py`
- `evals/config/naia_gate2_composition_v1.json`
- `evals/tests/test_composition.py`

The validator rejects:

- wrong repo/SHA;
- mismatched profile/policy hashes;
- static or synthetic evidence presented as runtime PASS;
- missing candidate-specific add-ons;
- `ISO-6` PASS backed only by a synthetic broker fixture;
- structural FAIL without a structural reason;
- environment BLOCK without a blocker id.

Therefore the current injected AI Butler test's synthetic broker echo cannot, by itself, close `ISO-6`.
