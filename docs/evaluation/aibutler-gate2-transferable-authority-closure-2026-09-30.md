# AI Butler Gate-2 transferable authority closure — 2026-09-30

## Candidate

`LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`

## Correction to prior evidence

The earlier audit recorded no observable exact-pin CI. A direct Actions query by `head_sha` now establishes:

```text
CI run 28973914814 = SUCCESS
Security run 28973914736 = SUCCESS
```

Relevant CI jobs on the exact pin:

```text
Test (race detector) = SUCCESS
Integration & Security = SUCCESS
Desktop Tier 4 (Linux live) = SUCCESS
Accessibility Tier 3 (Linux AT-SPI live) = SUCCESS
Build windows/amd64 = SUCCESS
```

The main test job executed:

`go test ./... -race -count=1 -timeout=10m`

and completed successfully.

## Gate-2 clauses closed by exact-pin executed tests

### Memory isolation

`internal/memory/bank_isolation_test.go` is part of `internal/memory`, which passed in the exact-pin race run.

The test directly proves:

- worker bank cannot list primary-bank thoughts;
- FTS cannot retrieve primary-bank content from worker bank;
- facts with identical keys do not supersede across banks;
- entities do not cross banks;
- vector KNN/hydration do not cross banks;
- transcript FTS is bank scoped;
- id-addressed mutation refuses cross-bank targets.

```text
MEMORY_BANK_NEGATIVE_ISOLATION = PASS_UPSTREAM_EXACT_PIN
```

### Capability monotonicity / delegation

`internal/capability/subset_test.go` is part of `internal/capability`, which passed.

Executed tests prove a child capability set cannot acquire a resource absent from the parent and that subset validation rejects missing capabilities.

```text
DELEGATION_CAPABILITY <= CALLER_CAPABILITY = PASS_UPSTREAM_EXACT_PIN_WITH_SCOPE
```

This transfers only when Atento uses the native capability-subset path unchanged.

### Denied actions / shell scope

`internal/capability/engine_test.go` passed as part of the same package and includes:

- no capability -> denied;
- command outside declared scope -> denied;
- path traversal -> denied;
- expired TTL -> denied;
- max calls exceeded -> denied;
- unmatched resource/domain/device -> denied.

The exact race run also passed the shell and shell/sandbox packages.

```text
DENIED_CAPABILITY_ACTION = DENIED_TECHNICALLY
CAPABILITY_SCOPE_BROADENING = NOT_ALLOWED_BY_ENGINE_TESTS
```

### Credential boundary

`internal/vault/broker_test.go` is part of `internal/vault`, included by `go test ./...`.

Executed source tests prove:

- an unapproved stored credential is denied;
- denied response omits the credential value;
- deny-list wins over auto-approval;
- missing credential denies;
- granted/denied requests are audited with agent/key context.

```text
CREDENTIAL_DEFAULT_DENY = PASS_UPSTREAM_EXACT_PIN
DENIED_CREDENTIAL_VALUE_LEAK = NO_IN_TESTED_BROKER_PATH
```

### Background authority

The exact source at `internal/schedule/schedule.go` refuses a scoped schedule when the runner cannot enforce the declared capability profile rather than silently running with the full default set.

`internal/schedule/builtin_test.go` directly asserts:

`scoped schedule must not use the default-capability run path`

and checks that the schedule's capability list is delivered to the scoped runner.

The package is included in the successful exact-pin race run.

```text
SCOPED_BACKGROUND_JOB_USES_DECLARED_CAPABILITIES = PASS_UPSTREAM_EXACT_PIN
SCOPED_JOB_UNSUPPORTED_RUNNER = FAIL_CLOSED_BY_SOURCE
BACKGROUND_AUTHORITY_BROADENING_FOR_SCOPED_SCHEDULE = NOT_OBSERVED
```

## Remaining Atento-specific residual

The upstream evidence does **not** close strict NAIA/Anna composition because Atento requires isolated memory, tool, credential and silent-invocation authority domains between two product roles.

AI Butler has native bank isolation, but the vault itself is not established as bank-scoped in the current evidence.

Therefore Atento must use a topology such as:

```text
NAIA runtime / memory bank / vault / channel config
             |
       explicit Atento broker
             |
Anna separate runtime / memory bank / vault / channel config
```

and execute one negative two-role composition probe.

Required residual only:

```text
CROSS_MEMORY_READ = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

## Gate-2 disposition

```text
AIBUTLER_EXACT_PIN_CI = PASS
AIBUTLER_AUTHORITY_CLAUSES_TRANSFERRED = PASS_WITH_SCOPE
AIBUTLER_MEMORY_ISOLATION = PASS_UPSTREAM_EXACT_PIN
AIBUTLER_CREDENTIAL_DEFAULT_DENY = PASS_UPSTREAM_EXACT_PIN
AIBUTLER_SCOPED_BACKGROUND_AUTHORITY = PASS_UPSTREAM_EXACT_PIN
AIBUTLER_DELEGATION_SUBSET = PASS_UPSTREAM_EXACT_PIN

ATENTO_TWO_ROLE_COMPOSITION = NOT_RUN
AIBUTLER_GATE2 = ONE_RESIDUAL_COMPOSITION_TEST_REMAINING
AIBUTLER_CURRENT_PIN_QUALIFIED = NO
```

No broad AI Butler runtime battery is justified before that one residual topology test.
