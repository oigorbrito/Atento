# TrustClaw exhaustive verification — 2026-09-30

## Scope

Candidate: `ComposioHQ/trustclaw`

Frozen evaluation pin:

```
c07410bccb916236b45b563e8c4ff76ad83d3855
```

The frozen pin remains the current default-branch head.

This record continues the prior static contract audit and establishes the strongest executable evidence currently available without inventing a functional pass.

Rules preserved:

- `STATIC_SOURCE != RUNTIME_PASS`
- `CODEQL_PASS != FUNCTIONAL_PASS`
- `MANY_TOOLS != LOCAL_AUTHORITY_PROOF`
- `OAUTH_CONNECTION != PER_ACTION_APPROVAL`
- `SELF_HOSTABLE_APP != FULLY_SELF_CONTAINED_RUNTIME`
- external Composio/Vercel behavior is not promoted to local Atento proof

No TrustClaw source was modified.

## Exact-pin hosted execution

The exact SHA has repeated GitHub-managed scheduled CodeQL runs. The reviewed current run is:

- run: `36133477273`
- exact head: `c07410bccb916236b45b563e8c4ff76ad83d3855`
- job: `Analyze (javascript-typescript)`
- conclusion: `success`

The job successfully completed checkout, CodeQL initialization and JavaScript/TypeScript analysis.

The exact commit exposes no combined commit-status contexts through the available connector.

Classification:

```ini
CODEQL_AT_EXACT_PIN = PASS
FUNCTIONAL_CI_AT_EXACT_PIN = NOT_OBSERVED
COMMIT_STATUS_CONTEXTS = NONE_OBSERVED
```

A successful CodeQL job is retained as static/security-analysis evidence only.

## Upstream functional harness inventory

The frozen root `package.json` exposes:

- `build`
- `build:local`
- `check`
- `format:check`
- `lint`
- `typecheck`

It exposes no `test`, `test:*`, Vitest or Jest script.

The CLI package exposes only build/dev/prepublish compilation scripts.

Repository code search at the current default branch found no `.test.ts`, `.spec.ts`, Vitest or Jest surface. Matches for text such as `describe(`, `it(` or `test(` were ordinary application/schema code, not test files.

No repository-owned push/PR workflow that runs build, lint, typecheck or functional tests was found for the frozen pin. The observed Actions history at that SHA is GitHub-managed CodeQL and dependency automation, not a product regression suite.

Classification:

```ini
UPSTREAM_FUNCTIONAL_TEST_HARNESS = NOT_FOUND
UPSTREAM_PRODUCT_REGRESSION_WORKFLOW = NOT_FOUND
BUILD_SCRIPT_EXISTS = YES
TYPECHECK_SCRIPT_EXISTS = YES
BUILD_TYPECHECK_EXECUTED_UPSTREAM_AT_PIN = NOT_ESTABLISHED
```

## Attempted local reproducibility

A clean local checkout of the exact public revision was attempted for the minimum reproducible `pnpm check` / build path.

The executor failed before checkout because its network namespace could not resolve `github.com`:

```
fatal: unable to access 'https://github.com/ComposioHQ/trustclaw.git/':
Could not resolve host: github.com
```

Classification:

```ini
LOCAL_CHECKOUT = BLOCKED_BY_EXECUTOR_NETWORK
LOCAL_BUILD = NOT_RUN
LOCAL_TYPECHECK = NOT_RUN
CANDIDATE_FAILURE_INFERRED_FROM_LOCAL_BLOCK = NO
```

This is an environment block, not a TrustClaw failure. It also means no local functional pass may be claimed.

## Reused static contract evidence

The prior source audit remains the current mechanism-level record:

`docs/evaluation/trustclaw-contract-audit-2026-09-29.md`

Its bounded findings remain applicable at the same frozen head.

### Instance-scoped memory

Static source establishes that memory save/search and automatic retrieval are scoped by `instanceId`, and authenticated user lookup binds the user to an instance.

```ini
INSTANCE_MEMORY_ISOLATION = STRONG_STATIC_EVIDENCE
CROSS_INSTANCE_MEMORY_RUNTIME_PROBE = NOT_RUN
```

### Cron

Static source establishes persisted jobs, `instanceId` scoping, cron validation, fail-closed production `CRON_SECRET`, timing-safe secret comparison, execution locking/fencing and per-user rate limiting.

```ini
CRON_PERSISTENCE = STRONG_STATIC_EVIDENCE
CRON_AUTH_FENCING = STRONG_STATIC_EVIDENCE
CRON_RUNTIME_EXECUTION = NOT_ESTABLISHED
```

### External-tool authority

The agent creates a Composio session under `instance.userId`, giving a user-scoping anchor for returned tools.

However, the repository still does not establish a local per-action technical approval/allowlist contract equivalent to Atento's required authority boundary.

```ini
COMPOSIO_SESSION_SUBJECT = USER_SCOPED_STATIC
LOCAL_PER_ACTION_APPROVAL = NOT_ESTABLISHED
LOCAL_TOOL_ALLOWLIST = NOT_ESTABLISHED
REMOTE_SANDBOX_IMPLEMENTATION = EXTERNAL_COMPOSIO_DEPENDENCY
```

### Background authority

Scheduled execution uses the same agent/tool setup. The prompt tells scheduled runs to stay within intended scope, but no independent technical capability subset was identified.

```ini
BACKGROUND_SCOPE_PROMPT = PRESENT
BACKGROUND_TECHNICAL_CAPABILITY_SUBSET = NOT_ESTABLISHED
```

For Atento, prompt-only authority restriction is insufficient.

## Dependency boundary

The standard TrustClaw runtime materially depends on external seams:

- Composio tool sessions / credentials / managed execution;
- Vercel AI Gateway or equivalent external model route;
- external embedding model;
- Postgres + pgvector;
- Vercel-oriented cron/deployment in the standard path;
- optional Redis for streaming/abort/rate-limit support.

Therefore the decisive next evidence cannot be manufactured from the repository alone. It requires a dependency-aware runtime composition.

## Gate

Smallest defensible classification:

```ini
CANDIDATE = TRUSTCLAW
PIN = c07410bccb916236b45b563e8c4ff76ad83d3855

CODEQL = PASS
UPSTREAM_FUNCTIONAL_HARNESS = NOT_FOUND
UPSTREAM_FUNCTIONAL_RUNTIME_PASS = NOT_ESTABLISHED
LOCAL_RUNTIME_ATTEMPT = BLOCKED_BY_EXECUTOR_NETWORK

INSTANCE_MEMORY_ISOLATION = STRONG_STATIC_ONLY
CRON_AUTH_FENCING = STRONG_STATIC_ONLY
COMPOSIO_USER_SCOPE = STATIC_ONLY
BACKGROUND_CAPABILITY_SUBSET = NOT_ESTABLISHED

ATENTO_DEPENDENCY_PROBE = NOT_RUN
ATENTO_CROSS_ROLE_COMPOSITION = NOT_RUN
ATENTO_ISOLATION = NOT_ESTABLISHED
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

This is an **evidence insufficiency gate**, not a functional FAIL verdict.

## Residual probe if this candidate reaches composition

The existing residual classification remains `DEPENDENCY_FIRST`.

A bounded TrustClaw probe must distinguish local chassis from externally controlled authority:

1. create two isolated test identities/instances representing NAIA and Anna;
2. use one low-risk connected Composio action and one deliberately unavailable/disallowed action;
3. prove memory cannot cross instance boundaries;
4. prove scheduled execution stays attached to the same identity/connection set;
5. determine whether a destructive action can be technically denied/approved independently of prompt wording;
6. simulate Composio unavailability and record fail/degrade behavior;
7. preserve evidence of credential visibility or non-visibility;
8. restart and verify memory/cron continuity;
9. record calls, cost and wall time;
10. keep Composio/Vercel results separate from local TrustClaw results.

Until that external dependency composition exists, broad product claims cannot close the Atento authority gate.

## Evidence references

- CodeQL exact-pin run: https://github.com/ComposioHQ/trustclaw/actions/runs/36133477273
- frozen pin: https://github.com/ComposioHQ/trustclaw/commit/c07410bccb916236b45b563e8c4ff76ad83d3855
- prior Atento contract audit: `docs/evaluation/trustclaw-contract-audit-2026-09-29.md`

## Final disposition for comparison table

```ini
TRUSTCLAW_FROZEN_PIN_STATUS = INSUFFICIENT_FUNCTIONAL_EVIDENCE
STATIC_PRODUCT_CONTRACT = MATERIAL
EXTERNAL_DEPENDENCY_BOUNDARY = MATERIAL
DEPENDENCY_RUNTIME_QUALIFICATION_REQUIRED = YES
```
