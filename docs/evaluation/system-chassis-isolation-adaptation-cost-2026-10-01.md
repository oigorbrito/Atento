# Isolation and adaptation-cost measurement — active mobile chassis cohort — 2026-10-01

## Scope and method

This record continues the bounded sequential chassis comparison on PR #58. It reuses existing exact-pin test runs, CI, static source reviews, and change-surface counts. No equivalent test or published benchmark was repeated.

OpenClaw is excluded from the active mobile-chassis cohort by explicit user direction because of product fit. Its previous evidence remains historical. The original discovery cohort remains 11; this active view contains the other 10 candidates.

Isolation is recorded by evidence status and scope, not as a numeric score. Cost is decomposed into observed change surface, measured engineering time, and ongoing maintenance/operations. A count from one adaptation recipe cannot be compared directly with another recipe or treated as total cost.

## Results

| Candidate | Isolation evidence already available | Isolation disposition for Atento's three-role contract | Adaptation-cost evidence already available | Cost disposition |
|---|---|---|---|---|
| NanoClaw | Hosted run 36815873223: 7/7 passed for profile-bound group/state mounts and persistence, DB ownership and cross-group lookup, direct A2A denial, per-role synthetic identity, scheduled-task ownership, and typed broker-to-mailbox handoff. Existing exact-pin CI: 513 passed, 0 failed, 3 skipped. | **PARTIAL_PASS_WITH_SCOPE**. Full system gate remains NOT_PASSED: production broker wiring, provider/gateway credential non-disclosure, real model decision, channel routing, host restart, and three-role task fire/retry/recovery remain open. | Static recipe counts: WhatsApp 4 files / 1 import / 4 dependencies; OneCLI 8 / 1 / 1 SDK; OpenCode 40 / 5 / 1 SDK plus manifest/build. These are distinct integration recipes. | Partial observed change surface only. No elapsed engineering, rework, deployed-service, lifecycle or maintenance measure. Not comparable as a total-cost value. |
| AI Butler | Exact-pin Atento Gate-2 result recorded 6/6 common assertions as PASS_WITH_SCOPE; exercised bank/vault/capability modules and the real Atento broker adapter, not the full app topology. | **BLOCK_CURRENT_PIN_ON_SECURITY**. A later scheduled security run for the same frozen pin reported seven reachable advisories; no repaired-pin requalification is recorded. The 6/6 module result does not establish Apollo or complete-system isolation. | No comparable file/change count, elapsed time, rework, lifecycle, or maintenance data found in the records checked. | **NOT_MEASURED**. |
| QwenPaw | Static review records per-agent memory/policy boundaries and fail-closed session authority; sandbox-unavailable fallback may broaden to unsandboxed ALLOW; cron authority needs hardening. Exact-pin main test status was incomplete and full nightly failed. | **HOLD_FOR_FAIL_CLOSED_PROFILE**. No complete Atento three-role runtime result. | No comparable adaptation or upkeep measurement found. | **NOT_MEASURED**. |
| MindRoom | Per-agent config/state roots exist. Pinned plan says shared-runner/local filesystem visibility is not fully agent-isolated; dedicated Kubernetes workers narrow mounts for selected scopes. | **HOLD_FOR_BACKEND_SPECIFIC_PROOF**. The safer deployment path is an architecture/deployment condition, not a demonstrated Atento pass. | No change-surface, elapsed-effort, deployment, or maintenance measurement found. | **NOT_MEASURED**. |
| Bob Labs | Exact-pin test definitions cover lab scoping, explicit memory-sharing consent, sandbox HMAC/nonce, and encrypted secrets; these definitions were inspected but not run in the reviewed evidence. | **UNRESOLVED**. Test definitions do not count as passing isolation tests; Atento role boundaries remain unproven. | No comparable measurement found. | **NOT_MEASURED**. |
| Ontheia | Namespace tests and RLS migrations are present; existing CI passes for host and WebUI. The reviewed material does not prove Atento agent/domain separation or three-role handoff authorization. | **UNRESOLVED**. | No comparable measurement found. | **NOT_MEASURED**. |
| OpenAkita | Exact-pin build passed, while Python/unit/integration/smoke/E2E jobs were skipped. Existing state/blackboard tests do not prove private role separation. | **UNRESOLVED**. | No comparable measurement found. | **NOT_MEASURED**. |
| Clawix | Exact-pin lint/typecheck/test CI passed. Reviewed multi-user repository tests use mocks; source/docs describe per-user workspace/session, Docker and mount allowlists, without an end-to-end role authorization or container-boundary result. | **UNRESOLVED**. | No comparable measurement found. | **NOT_MEASURED**. |
| Memoh | The prior screen has no frozen exact commit. | **BLOCKED_BEFORE_EXECUTION: PIN_REQUIRED**. No isolation finding transfers from README-only claims. | No pinned baseline or measured adaptation. | **NOT_MEASURED; PIN_REQUIRED**. |
| Letta Code | Historical overlay fixture at a different SHA passed bounded general/therapeutic policy isolation, RAG outage, removal and final regression checks. It is not the current full three-role topology. | **HISTORICAL_PARTIAL_EVIDENCE**. Do not transfer it as a current-pin system pass. | Historical fixture recorded 0 core imports/host-core edits and 7 sequential mutations. It did not record elapsed engineering time or upkeep. | Historical local-change evidence only; different fixture and scope, not comparable total cost. |

## Measurement summary

```text
ACTIVE_MOBILE_COHORT = 10
NEW_TESTS_OR_BENCHMARKS_RUN_FOR_THIS_MATRIX = 0
REUSED_ISOLATION_EVIDENCE = EXACT_PIN_AND_SCOPE_QUALIFIED
CANDIDATES_WITH_FULL_ATENTO_THREE_ROLE_ISOLATION_PASS = 0
CANDIDATES_WITH_ANY_COMPARABLE_TOTAL_ADAPTATION_AND_MAINTENANCE_COST = 0
CANDIDATES_WITH_PARTIAL_CHANGE_SURFACE_COUNTS = NanoClaw, historical Letta fixture
PROTOCOL_ELIGIBLE_TOP_3 = NOT_ESTABLISHED
```

No elapsed engineering hours, rework, ongoing maintenance, operational burden, or total-cost vector is available on a common basis for the active cohort. NanoClaw's three recipe counts and Letta's historical mutation count are useful planning signals, not a cost ranking. Missing or non-transferable isolation evidence is marked unresolved or blocked, never as a candidate failure.

## Evidence sources

- `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md` — exact-pin and hosted isolation evidence, including NanoClaw run 36815873223.
- `docs/evaluation/system-chassis-top10-first-sieve-2026-09-30.md` — frozen cohort order, partial change-surface counts, and total-cost evidence limits.
- `docs/evaluation/integrated-chassis-source-verification-2026-10-01.md` — source/test-definition limits for MindRoom, Bob Labs, Ontheia, OpenAkita, Clawix and other candidates.
- `docs/evaluation/system-chassis-external-benchmark-coverage-2026-10-01.md` — published capability scores and their limits; these do not replace isolation or cost measurements.
