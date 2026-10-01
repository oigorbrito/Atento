# Isolation block — residual evidence for mobile shortlist — 2026-10-01

## Scope

This is the next metric block after external functional-quality and safety reconciliation. It reuses exact-pin upstream CI, Atento runtime evidence, and source audits for NanoClaw, AI Butler, and QwenPaw. No equivalent test was rerun. OpenClaw remains excluded from the mobile-focused view by user direction.

The target contract is three independent role identities, sessions, private memory/state, tools and credentials for NAIA, Anna, and Apollo; only explicit typed handoff can cross roles, with authorization at the receiving role. Scheduled, retry, recovery and restart work must preserve equal-or-narrower role authority.

## Reused NanoClaw evidence

Frozen candidate pin: `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`.

Existing exact-pin CI is recorded as 513 passed, 0 failed, 3 skipped. The relevant existing upstream tests include:

| Exact-pin test file | Existing property exercised | Transfer limit |
|---|---|---|
| `src/gateway-read-policy.test.ts` | Allows configured gateway reads and rejects hosts/methods outside policy or malformed configuration. | Generic configured-host behavior; not the Atento three-role provider/gateway wiring. |
| `src/gateway-connections.test.ts` | Rejects malformed destinations, unknown groups, unsafe URLs, and extra adapter fields; checks that an adapter `secret` field is not exposed. | Sanitization and response-shape tests; not proof of real credential custody or model-visible non-disclosure in a deployed gateway. |
| `src/container-runner.claims.test.ts` | Exercises adoption claims, claim incarnation changes, failed stop/release behavior, and host replacement while a container survives. | Candidate runtime lifecycle unit/integration evidence; not an Atento role-bound restart run. |
| `src/delivery-attempts-authority.test.ts` | Exercises delivery-attempt state across restart and bounded permanent failure behavior. | Delivery retry state only; not three-role scheduled-task firing/retry/recovery. |
| `src/container-restart.test.ts`, `src/container-runner.orphans.test.ts` | Existing container restart/orphan lifecycle paths. | Do not establish the frozen Atento topology by themselves. |

Atento hosted run [36815873223](https://github.com/oigorbrito/Atento/actions/runs/36815873223) has 7/7 passing assertions with scope. It exercises the real NanoClaw DockerSessionDriver for three profile-bound state mounts, selected DB/session ownership and cross-group lookup denials, unbrokered A2A denial, role-unique synthetic identity mounts, scheduled-task ownership, and typed broker-to-mailbox requests. The broker adapter and profile-body checks are in the injected Atento harness; it does not start the deployed Atento app, gateway/provider, or an LLM.

### NanoClaw disposition

```text
EXACT_PIN_UPSTREAM_CI = 513_PASS / 0_FAIL / 3_SKIP
ATENTO_THREE_ROLE_PROFILE = 7_PASS / 0_FAIL, PASS_WITH_SCOPE
ISOLATION_STATUS = PARTIAL_PASS_WITH_SCOPE
FULL_SYSTEM_ISOLATION_GATE = NOT_PASSED
```

Still unproven: actual Atento gateway/provider credential custody and model-visible secrecy; production service wiring; a host-process restart with the frozen three-role profile; and scheduled-task fire/retry/recovery under that profile. The current harness uses inert local fixtures and explicitly disallows production credentials/live provider calls, so repeating its credential-mount test would not answer those questions. Closing them requires the missing integrated Atento runtime seam; mark that residual `BLOCKED_ADAPTER` until a bounded testable seam exists, not candidate failure.

## Reused evidence for the other two candidates

| Candidate | Reused isolation/security evidence | Current isolation disposition |
|---|---|---|
| AI Butler | Exact-pin Atento ISO-1..ISO-6 run passed with scope at module/broker-adapter level; it does not cover full three-role app, Apollo, scheduler/restart composition. Same frozen pin's scheduled security run 36426287353 reports seven reachable advisories. | `BLOCK_CURRENT_PIN_ON_SECURITY`. Do not repeat the six passing module checks on the unchanged pin; a repaired/refrozen pin needs requalification. |
| QwenPaw | Exact-pin source review finds per-agent memory/policy seams and fail-closed session authority, but sandbox-unavailable fallback can broaden to unsandboxed ALLOW and cron authority needs hardening. Existing exact-pin main tests were incomplete and full nightly failed. | `HOLD_FOR_FAIL_CLOSED_PROFILE`. No full Atento three-role isolation pass. |

These are candidate-specific test scopes and cannot be added as if each covers the same assertions. In particular, first-party test-definition presence and static source claims are not passing Atento runtime evidence.

## Gate result and next action

```text
MOBILE_SHORTLIST = [NanoClaw, AI Butler, QwenPaw]
NEW_ISOLATION_TESTS_RUN = 0
EQUIVALENT_TESTS_REPEATED = 0
FULL_ATENTO_THREE_ROLE_ISOLATION_PASSES = 0
IMMEDIATE_ADVANCE = NanoClaw only, with residual adapter blocker
AI_BUTLER = PIN_BLOCKED_BY_SECURITY
QWENPAW = HOLD_FAIL_CLOSED_PROFILE
OVERALL_ISOLATION_RANK = NOT_ESTABLISHED
```

The next decisive isolation probe, if the Atento runtime seam is available, is one primary hosted run using synthetic role-specific gateway grants: attempt read/use from the wrong role through the real host gateway path, then stop/restart the host with a pending inert role-bound task and verify that recovery preserves the same role authority. Keep the already-passing seven checks out of that run. If the gateway path still requires constructing a broad Atento product runtime, record `BLOCKED_ADAPTER` and continue the frozen comparison with the next applicable metric; do not build an open-ended adapter or treat missing proof as failure.

## Source records

- Existing system-gate results and NanoClaw run scope: `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md`.
- Cost and shortlist evidence: `docs/evaluation/system-chassis-isolation-adaptation-cost-2026-10-01.md`.
- Frozen isolation/authority assertions: `evals/config/system_chassis_nanoclaw_v1.json`.
- Pinned source tests: [gateway-read-policy](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/gateway-read-policy.test.ts), [gateway-connections](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/gateway-connections.test.ts), [container-runner claims](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/container-runner.claims.test.ts), and [delivery attempts](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/delivery-attempts-authority.test.ts).
