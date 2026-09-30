# AI Butler exhaustive verification — 2026-09-30

## Scope

Candidate: `LumabyteCo/aibutler`

Frozen evaluation pin:

```
c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c
```

The repository's current default-branch head is still this exact commit. This record combines exact-pin CI execution, the repeated scheduled security scan on the same SHA, and run-backed assertions relevant to Atento memory and scheduled authority boundaries.

Rules preserved:

- `UPSTREAM_SIGNAL != ATENTO_LOCAL_PROOF`
- `LOCAL_PASS != PERFORMANCE_PROOF`
- `IMPLEMENTED != QUALIFIED`
- `VERIFIED != ACCEPTED`
- `ACCEPTED != PROMOTED`
- narrow passing mechanisms do not imply complete NAIA/Anna isolation

No candidate source was modified.

## Exact-pin functional CI

Push CI run:

- run: `28973914814`
- exact head: `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`
- conclusion: `success`

Observed successful jobs:

- Lint
- Test (race detector)
- Desktop Tier 4 (Linux live)
- Accessibility Tier 3 (Linux AT-SPI live)
- builds for Linux amd64/arm64/riscv64, Windows amd64, Darwin amd64/arm64
- Integration & Security

The race-detector job executed `go test` over the repository and reported successful packages including:

- `internal/memory`
- `internal/permissions`
- `internal/plugin/sandbox`
- `internal/schedule`
- `internal/security`
- `internal/session`
- `internal/shell/sandbox`
- `internal/tool`
- `internal/vault`

The same run also generated package coverage; examples directly relevant to the Atento boundary include approximately 53.9% for `internal/memory`, 94.7% for `internal/permissions`, 90.9% for `internal/plugin/sandbox`, 73.7% for `internal/schedule`, and 100% for `internal/security`. Coverage percentages are not isolation scores; they only describe executed source coverage in that run.

Classification:

```ini
FUNCTIONAL_CI = PASS
RACE_DETECTOR = PASS
MULTIPLATFORM_BUILD = PASS
INTEGRATION_SECURITY_JOB = PASS
```

## Run-backed memory-bank isolation

The frozen pin contains `internal/memory/bank_isolation_test.go`. Because the exact-pin race job ran the `internal/memory` package successfully, these assertions are run-backed at the evaluated SHA.

Observed tests include:

- `TestBankIsolationAcrossStores`
- `TestDefaultBankBackCompat`
- `TestVectorBankStamping`
- `TestBackfillPreservesSourceBank`
- `TestTranscriptFTSBankIsolation`
- `TestIdAddressedOpsRefuseCrossBank`

The directly checked source assertions establish, with scope:

- a worker bank cannot retrieve a primary-bank thought through full-text search;
- same-key worker facts do not supersede the primary bank's fact;
- entity lookup/save is bank-scoped;
- transcript FTS does not cross banks;
- asynchronous vector writes retain the source bank;
- ID-addressed mutation attempts from the worker bank cannot forget, pin, correct, or delete objects belonging to the primary bank.

The test explicitly exercises a primary context and a separate `swarm` bank rather than relying only on different keys.

Classification:

```ini
MEMORY_BANK_ISOLATION = PASS_WITH_SCOPE
CROSS_BANK_FTS_DENIAL = PASS
CROSS_BANK_ID_MUTATION_DENIAL = PASS
SAME_KEY_FACT_SEPARATION = PASS
VECTOR_BANK_STAMPING = PASS
```

Important boundary: the bank is carried in context and the package contract says cross-bank access is possible when a caller is explicitly handed another bank's scope. These tests therefore prove store/query enforcement for distinct scopes; they do **not** prove that an Atento role cannot forge, acquire, or be mis-bound to another role's scope. NAIA/Anna identity-to-bank binding remains a composition problem.

## Run-backed scheduled capability scoping

The frozen pin also contains `internal/schedule/builtin_test.go::TestTickUsesScopedCapabilities`, and the exact-pin race job reported the `internal/schedule` package passing.

The assertion creates a scheduled job with:

```
["memory.read", "memory.write"]
```

and verifies:

- the capability list survives persistence;
- scheduler execution uses the capability-scoped runner;
- the default-capability path is not used;
- the runner receives exactly the declared list.

The scheduler implementation also contains a fail-closed branch for a schedule declaring capabilities when the available runner cannot scope them: it records an error rather than silently running with the full default set.

Classification:

```ini
SCHEDULE_CAPABILITY_SUBSET = PASS_WITH_SCOPE
DECLARED_CAPS_DEFAULT_PATH_BYPASS = DENIED_IN_TEST
UNSCOPABLE_DECLARED_CAPS = FAIL_CLOSED_IN_SOURCE
```

Residual limit: schedules without an explicit capability list can use the default capability set. An Atento profile would therefore have to freeze explicit capability lists for every background task and verify equivalence with foreground authority policy.

## Current exact-pin security failure

The same SHA has continued to receive scheduled `Security` workflow runs after the original push. The most recent reviewed run is:

- run: `36426287353`
- date: 2026-09-28
- exact head: the same frozen pin
- job: `govulncheck (CVE scan)`
- conclusion: `failure`

The scanner reports that candidate code has reachable call paths to seven vulnerabilities:

1. `GO-2026-6218` — `net/url@go1.26.5`; fixed in Go 1.26.6; trace through OIDC refresh.
2. `GO-2026-6090` — `crypto/tls@go1.26.5`; fixed in Go 1.26.6; traces through server, backup, CLI and offline transport paths.
3. `GO-2026-6089` — `net/http@go1.26.5`; fixed in Go 1.26.6; server/webchat paths.
4. `GO-2026-6088` — `encoding/xml@go1.26.5`; fixed in Go 1.26.6; remote S3 list decoding.
5. `GO-2026-5972` — `encoding/asn1@go1.26.5`; fixed in Go 1.26.6; WebAuthn key parsing.
6. `GO-2026-5970` — `golang.org/x/text@v0.38.0`; fixed in `v0.39.0`; stop-phrase normalization.
7. `GO-2026-5026` — HTTP/IDNA path reported against Go 1.26.5; fixed in Go 1.26.6; OIDC/CLI/offline HTTP paths.

Scanner summary:

```
Your code is affected by 7 vulnerabilities from 1 module and the Go standard library.
```

It separately reports six additional dependency/package findings for which it did not find a call path.

The frozen `go.mod` pins:

```
toolchain go1.26.5
golang.org/x/text v0.38.0
```

The scheduled security workflow is specifically designed to catch newly disclosed CVEs. It succeeded on the original 2026-07-08 push, then later scheduled executions on the unchanged SHA became red as advisories were published. This is expected temporal behavior for a security gate, not evidence that the original CI was fabricated.

Classification:

```ini
CURRENT_SECURITY_SCAN = FAIL
REACHABLE_VULNERABILITIES_REPORTED = 7
FIXED_VERSIONS_IDENTIFIED_UPSTREAM = YES
REPAIR_EXECUTED_AT_CANDIDATE_HEAD = NO
CURRENT_HEAD_EQUALS_FROZEN_PIN = YES
```

The fixed-version metadata suggests a small dependency/toolchain treatment is plausible, but no patched candidate revision and no post-treatment regression run exist in the repository. Therefore the fix must not be assumed.

## Atento interpretation

AI Butler supplies unusually relevant positive primitives for the Atento problem:

- run-backed memory bank isolation across multiple retrieval/mutation paths;
- run-backed scheduled capability subsets;
- tested permissions and sandbox packages;
- race-enabled broad CI.

Those facts reduce uncertainty about mechanism availability. They do not establish the composed requirements:

- NAIA and Anna permanently bound to distinct, non-forgeable memory scopes;
- separate credentials, tool registries and channel authority;
- broker-only handoff between roles;
- denial of role drift;
- foreground/background authority equivalence under every scheduled path;
- selected browser/computer-use profile;
- Engram → adapter/browser integration.

The current frozen SHA additionally fails its own security workflow against seven reachable advisories.

## Gate

Smallest defensible status:

```ini
CANDIDATE = AI_BUTLER
PIN = c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c

FUNCTIONAL_CI = PASS
MEMORY_BANK_ISOLATION = PASS_WITH_SCOPE
SCHEDULE_CAPABILITY_SCOPING = PASS_WITH_SCOPE
CURRENT_SECURITY_GATE = FAIL

UPSTREAM_GENERAL_HEALTH_GATE = FAIL_SECURITY
ATENTO_ISOLATION = NOT_ESTABLISHED
ATENTO_COMPOSITION = NOT_RUN
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

A requalification would require at minimum a treated toolchain/dependency revision, rerunning the security workflow and functional/race suite, then freezing an Atento identity-to-bank and capability profile before adversarial composition tests.

## Evidence references

- exact-pin CI: https://github.com/LumabyteCo/aibutler/actions/runs/28973914814
- current scheduled security failure on the same SHA: https://github.com/LumabyteCo/aibutler/actions/runs/36426287353
- frozen pin: https://github.com/LumabyteCo/aibutler/commit/c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c

## Final disposition for comparison table

```ini
AIBUTLER_FROZEN_PIN_STATUS = FAIL_SECURITY
FUNCTIONAL_BASELINE = PASS
DIRECTLY_RELEVANT_MEMORY_EVIDENCE = STRONG_NARROW
DIRECTLY_RELEVANT_SCHEDULE_EVIDENCE = POSITIVE_NARROW
REPAIR_REQUIRED = YES
REQUALIFICATION_REQUIRED_AFTER_REPAIR = YES
```
