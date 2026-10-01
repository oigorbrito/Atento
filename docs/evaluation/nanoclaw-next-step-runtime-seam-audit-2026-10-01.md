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

## Decision

```text
NANOCLAW_CURRENT_BASE = PROVISIONAL_SELECTED
ATENTO_PRODUCT_RUNTIME_PRESENT_IN_BRANCH = NO
REAL_GATEWAY_PROVIDER_CUSTODY_SEAM = ABSENT
HOST_PROCESS_RESTART_SEAM = ABSENT
ROLE_BOUND_TASK_FIRE_RETRY_RECOVERY_SEAM = ABSENT
NEW_TESTS_RUN = 0
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
