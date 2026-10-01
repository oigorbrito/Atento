# NanoClaw follow-up preflight — runtime seam audit — 2026-10-01

## Question

Can the next bounded NanoClaw follow-up directly test Atento's real provider/gateway credential custody and role-bound scheduled-task recovery without building a broad new product runtime or repeating the passing probe?

## Read-only findings

- The Atento branch root contains .github, docs, evals, tools, README.md, roadmap.md, and AGENTS.md. It has no application source/runtime directory or deployed Atento gateway/provider service to launch.
- The only system-chassis NanoClaw workflow is .github/workflows/system-chassis-nanoclaw-probe.yml. It checks out the exact NanoClaw pin, copies in tools/system_chassis/nanoclaw.atento.test.ts, pulls a digest-pinned test utility image, and runs Vitest.
- The probe explicitly states that it exercises NanoClaw's Docker driver with inert role fixtures and does not start NanoClaw's provider/channel/application runtime.
- Its agent containers run /bin/sh -c 'sleep 600' with network: none. Profile provider/channel identifiers are seeded into test DB fixtures; no provider or messaging adapter is instantiated.
- Its credential assertion mounts role-unique synthetic material read-only in an auxiliary container and checks Docker mount metadata. It does not exercise actual gateway credentials, a live provider call, or application/model-visible context.
- Its state recovery check stops candidate-managed test containers and calls the DockerSessionDriver prepare/start path. It does not terminate/restart an Atento host application process.
- The scheduled-task assertion validates task creation, ownership, scoped reads, and denials. It does not fire the task, retry it, or recover it after host restart.

## NanoClaw mobile-client seam — exact pin source review

A follow-up read-only inspection of NanoClaw `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` found:

- `src/channels/adapter.ts` defines a host-side `ChannelAdapter` contract for inbound messages, outbound delivery, setup/teardown, and connection status.
- `src/webhook-server.ts` routes installed Chat SDK adapters and separately registered raw webhooks.
- `docs/api-details.md` describes adding channels through the adapter contract and installed channel contributions.

These are extensibility seams, not a ready mobile-app API. The inspected pin does not expose a generic authenticated mobile chat endpoint, account/session binding contract, or mobile response-stream contract. A mobile client therefore needs a new Atento-owned adapter/API that authenticates the user, fixes the NAIA role/session server-side, submits inbound messages, and returns or streams outbound replies. Client-provided role or agent-group identifiers must not select authority.

Classification:

```text
NANOCLAW_CHANNEL_EXTENSION_SEAM = PRESENT_STATIC
GENERIC_MOBILE_CHAT_API_AT_PIN = NOT_FOUND
MOBILE_AUTH_AND_NAIA_SESSION_BINDING = NOT_IMPLEMENTED_IN_ATENTO
MOBILE_ADAPTER_COST = 209_LINE_LOCAL_SPIKE (131 TEST LINES)
```

This does not establish a structural failure: NanoClaw explicitly supports channel adapters. It does establish that app connectivity is new adapter work, not an existing capability that can be counted as zero-touch. The adapter must be implemented before a mobile-client integration test can exercise the real path.

The local experiment executor has Node.js 24 but no Docker or Podman binary, and the private Atento repository is not available as a local checkout in this workspace. A disposable local NanoClaw worktree was used for the bounded channel spike below. This did not rerun or alter the prior hosted 7/7 chassi assertions and did not exercise the Atento product runtime.

## Decision

```text
NANOCLAW_CURRENT_BASE = PROVISIONAL_SELECTED
ATENTO_PRODUCT_RUNTIME_PRESENT_IN_BRANCH = NO
REAL_GATEWAY_PROVIDER_CUSTODY_SEAM = ABSENT
HOST_PROCESS_RESTART_SEAM = ABSENT
ROLE_BOUND_TASK_FIRE_RETRY_RECOVERY_SEAM = ABSENT
NEW_TESTS_RUN = 2/2 LOCAL ADAPTER TESTS PASS
BUILD = PASS
LINT = PASS
PREVIOUS_7_ASSERTIONS_REPEATED = 0
NEXT_INTEGRATED_PROBE = BLOCKED_ADAPTER
```

There is no existing Atento application seam to attach a narrow test to. Adding another test around the same driver, fake sleep containers, synthetic credential file, or fixture DB would repeat or rename existing evidence and would not close the decision-relevant gaps. Do not dispatch the existing workflow again for this purpose.

## Smallest concrete prerequisite

Implement or expose the actual narrow Atento host adapter that owns the provider/gateway grant and receives scheduled work, with a test mode that can run against synthetic credentials and inert tasks. It must expose one host-process lifecycle boundary. Only then run one focused delta:

1. Verify a role cannot observe/use another role's gateway credential through the actual adapter path.
2. Queue one inert role-bound task per role.
3. Stop/restart the host process once and allow one bounded retry.
4. Verify each task resumes under the same role and cross-role state/credential reads remain denied.

This prerequisite is product runtime implementation work; the current comparison PR and probe harness do not contain that runtime. Until it exists, retain NanoClaw as the provisional direction and report its composition gate as NOT_PASSED, with this follow-up BLOCKED_ADAPTER. Do not count this missing seam as a NanoClaw failure or as a test pass.

## Evidence inspected

- Atento branch root listing: https://github.com/oigorbrito/Atento/tree/codex/atento-bounded-sequential-chassis-test-20261001
- Existing NanoClaw probe: [nanoclaw.atento.test.ts](../../tools/system_chassis/nanoclaw.atento.test.ts)
- Existing workflow: [system-chassis-nanoclaw-probe.yml](../../.github/workflows/system-chassis-nanoclaw-probe.yml)
- Frozen three-role profile: [system_chassis_nanoclaw_v1.json](../../evals/config/system_chassis_nanoclaw_v1.json)
- Existing 7/7 hosted evidence and scope: [Gate 2 continuation](system-chassis-gate2-continuation-2026-10-01.md)
- User-directed provisional selection: [provisional NanoClaw chassis direction](../decisions/provisional-system-chassis-nanoclaw-2026-10-01.md)


## Bounded local mobile-adapter spike — 2026-10-01

On the pinned NanoClaw checkout, a disposable local-only spike registered an opt-in `atento-mobile` ChannelAdapter and exercised it through NanoClaw's real webhook server and channel-delivery registry. The spike contains 209 implementation lines, 131 test lines, and one import line in the channel barrel (340 added lines total). It is not committed to NanoClaw or Atento and is not a production integration.

Results:

- Focused Vitest: 2/2 passed. It verified bearer-token rejection, server-fixed owner identity, rejection of client-supplied role/group selection, inbound message routing, and a simulated agent response returned to an open long-poll request.
- `pnpm run build`: passed.
- ESLint on the changed files: passed.
- During initialization, the unrelated CLI adapter logged `listen EPERM` when attempting to bind its Unix socket in this sandbox. The HTTP webhook and mobile adapter still started, and both focused tests passed.

Scope limits:

- The bearer secret was synthetic and shared; no user/account authentication or production credential custody was tested.
- The “agent” response was a test callback using NanoClaw's real delivery registry, not a model/provider invocation.
- Pending responses live only in process memory and require an open poll. There is no durable queue, reconnect delivery, mobile session binding, host-restart recovery, or hosted Docker run.
- Docker and Podman are absent in this executor. The PR's existing hosted 7/7 chassi evidence was not repeated.

Updated classification:

```text
MOBILE_ADAPTER_SEAM = PROTOTYPE_LOCAL_PASS
MOBILE_ADAPTER_COST = 209_IMPLEMENTATION_LINES + 131_TEST_LINES + 1_REGISTRATION_LINE
MOBILE_PRODUCTION_AUTH_AND_SESSION_BINDING = NOT_TESTED
MOBILE_DURABLE_DELIVERY_AND_RESTART_RECOVERY = NOT_IMPLEMENTED
ATENTO_PRODUCT_INTEGRATION = NOT_PRESENT
NANOCLAW_COMPOSITION_GATE = NOT_PASSED
```

The spike reduces uncertainty about whether NanoClaw's channel seam can carry a basic authenticated HTTP mobile path: it can. It does not qualify NanoClaw for the product. The next decision-relevant step is to move this narrow adapter behind Atento's actual user/session and credential boundary, add durable response delivery, then run the hosted integration test including one process restart.
