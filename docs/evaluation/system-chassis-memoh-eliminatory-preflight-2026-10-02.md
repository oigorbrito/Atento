# Memoh eliminatory and bounded runtime tests — 2026-10-02

## Candidate and scope

Candidate under test: `felinics/Memoh@3d60a08aa42fdcddb218401699822741b51b52ad`, the immutable pin frozen for the system cohort. The upstream `main` head was later observed at `4f0667fa482b537a7005ec291a22a862b8e6686a`; all commands below ran against the frozen `3d60a08` checkout, not the moving head.

This is a candidate-level eliminatory preflight, not a three-role Atento integration. It reuses only scoped upstream package tests that map to Atento's hard boundaries. No project source was changed, no provider credentials were supplied, and no scheduled job was allowed to contact a provider.

## Environment and provenance

- Disposable source checkout: `/workspace/scratch/fcea454ddccb/memoh-pin`
- `git rev-parse HEAD`: `3d60a08aa42fdcddb218401699822741b51b52ad`
- Runtime: Go 1.25.7 linux/amd64, matching the repository's `go.mod`
- Go archive SHA-256: `12e6d6a191091ae27dc31f6efc630e3a3b8ba409baf3573d955b196fdf086005`; matched the official Go download metadata before extraction.
- No Docker, Podman, PostgreSQL, or Redis service is available in this executor.
- GitHub combined status for the frozen commit returned no statuses.

## Eliminatory evidence run

The following exact-pin upstream packages were run sequentially:

| Gate property | Command | Result | Observable scope |
|---|---|---|---|
| Per-bot workspace ownership and lifecycle/backoff | `go test ./internal/botworkspace` | PASS | Deterministic workspace state and retry/backoff decisions; no container was started. |
| Bot-scoped credential authorization, encryption, wrong-owner denial, exchange retry/redaction | `go test ./internal/agentcredential` | PASS | Unit tests use fakes; no real provider identity or PostgreSQL was used. |
| Schedule execution normalization and bot/session binding | `go test ./internal/schedule` | PASS | Package tests passed; no real persisted process restart or live job delivery was performed. |
| Memory boundary against foreign/missing bot scope | `go test ./internal/memory/adapters/builtin` | PASS | In-memory graph/file runtime rejects foreign and missing scope before mutation. |
| Capability/tool-context grants | `go test ./internal/contextview` | PASS | Unit-level capability and context policy tests; not an Atento handoff test. |
| Tool boundary and background-agent paths | `go test ./internal/agent/tool` | INITIAL RUN HAD 7 ENVIRONMENT-BOUND FIXTURE FAILURES | All seven were image-download tests using a TEST-NET URL and a loopback redirect seam; the executor's HTTP proxy intercepted the connection before the test dialer. The remaining tests emitted no failures in that run. |

Targeted confirmation for only the seven affected image tests, with proxy variables unset for the test process:

```text
env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy \
  go test ./internal/agent/tool -run '^(TestGenerateDashScopeImageUsesAsyncSDKProviderAndDownloadsImage|TestGenerateDashScopeQwenImageUsesProviderDefaultSizeWhenUnspecified|TestGenerateOpenAIImagesImageUsesImagesEndpointAndDownloadsURL|TestImageResultToGeneratedImageRejectsNonImageURL|TestImageResultToGeneratedImageRejectsSpoofedImageContentType|TestFetchGeneratedImageRejectsEmptyBody|TestFetchGeneratedImageTruncatesLargeErrorBody)$'

ok  github.com/felinics/memoh/internal/agent/tool  0.051s
```

This targeted confirmation passed. The full `internal/agent/tool` package was not rerun; its first-run status remains `FAIL_WITH_HARNESS_INTERFERENCE`, with the affected seven cases confirmed passing only after the test-process proxy bypass.

A further targeted application-layer run did not start because Go could not resolve/download three uncached modules (`coder/acp-go-sdk`, `redis/go-redis`, `wazero`); both module-proxy and direct-VCS attempts failed with executor DNS/network unavailable. This is `BLOCKED_ENVIRONMENT`, not a code/test failure.

## Eliminatory disposition

```text
PIN_IDENTITY = VERIFIED
BOT_WORKSPACE_BOUNDARY_TESTS = PASS_WITH_SCOPE
BOT_CREDENTIAL_BOUNDARY_TESTS = PASS_WITH_SCOPE
BOT_MEMORY_SCOPE_TESTS = PASS_WITH_SCOPE
BOT_CAPABILITY_CONTEXT_TESTS = PASS_WITH_SCOPE
SCHEDULE_UNIT_TESTS = PASS_WITH_SCOPE
TOOL_PACKAGE = FAIL_WITH_HARNESS_INTERFERENCE; 7_CASE_TARGETED_CONFIRMATION_PASS
APPLICATION_LAYER_SELECTED_TESTS = BLOCKED_ENVIRONMENT_BEFORE_TEST_START
FULL_MEMOH_STACK_E2E = BLOCKED_ENVIRONMENT (NO_DOCKER_POSTGRES_QDRANT_OR_REDIS)
ATENTO_THREE_ROLE_COMPOSITION = NOT_TESTED
NEW_STRUCTURAL_ELIMINATION = NONE
```

No tested result demonstrates that Memoh cannot represent the required bot boundaries, so this preflight does not eliminate the candidate. The passing package tests are component evidence only. They do not establish cross-bot protection through the full API/database/container topology, provider secret custody in a live model call, or NAIA-owned scheduled-task retry after the Atento host restarts.

## Smallest next falsifiable test

After a reproducible runtime environment is available, run one isolated Memoh stack at this same pin with synthetic users, bots, credentials, database, and inert tasks. Attempt cross-bot reads/updates for memory, tools, credentials, and scheduled sessions; then kill the host after a due task is claimed but before terminal acknowledgement, restart once, allow one retry, and verify bot ownership and exactly-once terminal delivery. Do not call a real model/provider. Record database rows, request/task IDs, claim/ack timestamps, logs, and process exit/restart IDs.

Required environment still missing: Go modules needed by the application package, Docker/Podman plus PostgreSQL/Qdrant/Redis, and a candidate runtime entrypoint that can be driven with a synthetic provider. Do not build an Atento production adapter just to unlock this candidate spike.

This report is on the disposable Atento branch only. PR #58 remains unchanged.
