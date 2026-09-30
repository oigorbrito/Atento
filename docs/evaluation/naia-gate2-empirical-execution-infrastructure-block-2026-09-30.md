# NAIA Gate-2 empirical execution infrastructure block — 2026-09-30

## Purpose

Record one shared infrastructure block for the frozen Gate-2 composition harness so candidate state is not polluted by executor failures.

## Attempted execution

Target:

`AI Butler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

Atento workflow:

`.github/workflows/naia-gate2-aibutler-composition.yml`

Atento head:

`f5ea26ac9e9b3d9deb7382fffb49a9ce2fbec3f1`

GitHub Actions run:

`36789543149`

## Observed result

Local executor:

```text
git ls-remote https://github.com/... = Could not resolve host: github.com
LOCAL_MATERIALIZATION = BLOCKED_DNS
```

Hosted executor:

```text
workflow accepted = YES
job created = YES
job conclusion = FAILURE
job steps = []
candidate checkout = NOT_RUN
Go setup = NOT_RUN
composition assertions = NOT_RUN
```

The hosted job failed before any workflow step was recorded.

Therefore:

```text
AI_BUTLER_COMPOSITION_RESULT = BLOCKED_ENVIRONMENT
AI_BUTLER_GATE2 = NOT_FAILED
AI_BUTLER_GATE2 = NOT_PASSED
```

No candidate behavior was executed.

## Shared consequence

The twelve frontier candidates use the same external materialization requirement. Repeating the same mechanism candidate-by-candidate while the executor cannot start would create redundant infrastructure failures, not candidate evidence.

```text
FRONTIER_EXECUTION_INFRA = BLOCKED
BLOCK_PROPAGATION_SCOPE = EXECUTOR_ONLY
CANDIDATE_FAIL_PROPAGATION = FORBIDDEN
```

Affected planned executions:

- AI Butler
- OpenMausBot
- NanoClaw
- AgentOS
- Rome
- Suna
- Rakazo
- Letta Code
- Octop
- QwenPaw
- RustFox
- Engram

This does not invalidate their transferable upstream evidence.

## Resume condition

Resume empirical Gate-2 composition when any one of these becomes true:

1. local exact-pin materialization works;
2. a GitHub-hosted runner executes at least the checkout step;
3. another reproducible executor can materialize the exact candidate pin and preserve raw artifacts.

Do not weaken the exact-pin requirement to work around the infrastructure block.
