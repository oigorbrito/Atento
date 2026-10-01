# Reliability and recovery block — mobile chassis shortlist — 2026-10-01

## Scope and method

This is the reliability/recovery block after isolation in the frozen evaluation sequence. It reuses exact-pin CI, already-run Atento hosted evidence, and the existing candidate audits. No tests or scans were run for this note, and no previously passing equivalent tests were repeated.

The Atento contract is that scheduled work, retries, process/container restarts, and recovery preserve the same role identity, private state, tools, credentials, and equal-or-narrower authority. A candidate-level lifecycle test is useful evidence, but it does not by itself prove the composed three-role Atento system.

## Evidence matrix

| Candidate | Existing evidence reused | Reliability/recovery disposition | Decisive Atento gap |
|---|---|---|---|
| NanoClaw | Exact-pin upstream CI: 513 passed, 0 failed, 3 skipped. Existing src/container-runner.claims.test.ts covers claim adoption/incarnation, failed stop/release, and host replacement; src/delivery-attempts-authority.test.ts covers persisted bounded delivery attempts across restart; src/container-restart.test.ts and src/container-runner.orphans.test.ts cover candidate container lifecycle paths. Atento hosted run 36815873223 passed 7/7 with scope and includes scheduled-task ownership, but not actual scheduled fire/retry/recovery with a host-process restart. | **PARTIAL_PASS_WITH_SCOPE** at candidate lifecycle level; **BLOCKED_ADAPTER** for the composed Atento profile. | Run a bounded role-bound scheduled task through the integrated Atento runtime, induce one host restart/retry, then verify persisted ownership and authority. Existing harness does not start the production Atento gateway/provider/app. |
| AI Butler | Exact-pin race CI run 28973914814 passed, including internal/schedule; TestTickUsesScopedCapabilities verifies declared capability persistence and scoped execution. Source has a fail-closed branch when a schedule declares capabilities but no scoped runner is available. | **PASS_WITH_SCOPE** for narrow scheduler capability behavior; overall current pin is **BLOCK_CURRENT_PIN_ON_SECURITY** because scheduled scan 36426287353 found seven reachable advisories. No reliability requalification should be inferred from the old CI. | Freeze explicit capability lists for every Atento background task and prove foreground/background authority parity through restart/recovery on a remediated, requalified pin. Current pin is security-blocked. |
| QwenPaw | Existing static contract audit documents per-Agent workspace/session boundaries and identifies sandbox-unavailable fallback that can broaden authority; cron/background authority needs hardening. The audit records incomplete main-test evidence and a failed full nightly. Expected restart/approval assertions are not evidence of a passing frozen-pin runtime run. | **HOLD_FOR_FAIL_CLOSED_PROFILE**; runtime reliability/recovery qualification not established. | Harden fail-closed sandbox and cron behavior, then provide passing exact-pin runtime evidence that restart does not broaden approvals and background authority is no broader than interactive authority. |

## Gate result

```text
NEW_TESTS_OR_SCANS_RUN = 0
EQUIVALENT_TESTS_REPEATED = 0
NANOCLAW_CANDIDATE_LIFECYCLE = PARTIAL_PASS_WITH_SCOPE
NANOCLAW_ATENTO_ROLE_BOUND_RECOVERY = BLOCKED_ADAPTER
AI_BUTLER_SCOPED_SCHEDULER = PASS_WITH_SCOPE
AI_BUTLER_CURRENT_PIN = BLOCKED_BY_SECURITY
QWENPAW_RELIABILITY_RECOVERY = NOT_ESTABLISHED / HOLD_FOR_FAIL_CLOSED_PROFILE
FULL_ATENTO_THREE_ROLE_RECOVERY_PASSES = 0
OVERALL_RELIABILITY_RECOVERY_RANK = NOT_ESTABLISHED
```

Do not convert missing integration evidence into a candidate failure or assign a numeric score. AI Butler's current security block remains a hard gate independent of its narrow scheduler result. No candidate has a full three-role Atento recovery pass.

## Bounded next action

The smallest useful follow-up is one integrated NanoClaw run, only if the existing Atento runtime seam can execute the real scheduled-task path: enqueue one inert synthetic task per role, allow one controlled host restart and one bounded retry, then inspect that each task resumes under its original role and cannot read another role's state. Exclude the seven already-passing assertions from run 36815873223. If the runtime seam is still absent, record BLOCKED_ADAPTER and advance to the next metric instead of constructing an unbounded harness.

For AI Butler, do not spend test time on the unchanged security-blocked pin. For QwenPaw, first require a fail-closed fix and frozen runtime test path; source inspection alone does not qualify recovery.

## Source records

- Atento isolation residual and NanoClaw hosted run scope: [system-chassis-top3-isolation-residual-2026-10-01.md](system-chassis-top3-isolation-residual-2026-10-01.md)
- AI Butler exact-pin CI, schedule test, and later security failure: [aibutler-exhaustive-verification-2026-09-30.md](aibutler-exhaustive-verification-2026-09-30.md)
- QwenPaw source contract and runtime evidence limits: [qwenpaw-contract-audit-2026-09-29.md](qwenpaw-contract-audit-2026-09-29.md)
- NanoClaw pinned lifecycle tests: [container-runner claims](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/container-runner.claims.test.ts), [delivery attempts authority](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/delivery-attempts-authority.test.ts), [container restart](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/container-restart.test.ts), [container orphans](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/container-runner.orphans.test.ts)
- AI Butler exact-pin CI: https://github.com/LumabyteCo/aibutler/actions/runs/28973914814
- AI Butler scheduled security scan: https://github.com/LumabyteCo/aibutler/actions/runs/36426287353
