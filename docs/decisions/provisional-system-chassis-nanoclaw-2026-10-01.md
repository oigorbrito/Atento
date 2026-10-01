# Provisional chassis direction — NanoClaw — 2026-10-01

## Decision

At the user's direction, select **NanoClaw** as the provisional Atento chassis/base to advance into the next implementation and qualification phase.

This is a project direction decision based on the strongest currently recorded, positive exact-pin and Atento-specific evidence among the active mobile shortlist, combined with the current blockers on the other frozen pins. It is not a claim that NanoClaw won a comparable end-to-end cost or performance benchmark.

## Evidence basis

- Frozen candidate pin: `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`.
- Exact-pin upstream CI recorded: 513 passed, 0 failed, 3 skipped.
- Atento hosted probe 36815873223 recorded 7/7 scoped three-role assertions passing: selected group/state mounts, DB/session ownership and cross-group lookup denial, unbrokered A2A denial, role-unique synthetic identities, scheduled-task ownership, and typed broker-to-mailbox requests.
- Additional exact-pin candidate tests cover lifecycle claims/release, delivery-attempt state across restart, container restart/orphan paths, task recurrence, host sweep, and scheduling scripts. These prove component behavior within their stated test scope, not full Atento recovery.
- AI Butler's frozen pin is blocked by a scheduled scan reporting seven reachable advisories. Its scoped scheduler and module tests do not override this pin-level security block.
- QwenPaw's frozen pin remains on hold because sandbox-unavailable fallback can broaden authority and background/cron authority needs hardening; passing Atento three-role runtime recovery evidence is absent.
- Existing published functional/safety scores and external cost studies are retained within their own protocols. They do not produce a common three-candidate operational-cost or complete-system rank.
- NanoClaw's remaining system blockers include production Atento gateway/provider wiring and credential custody, host-process restart, and role-bound scheduled task fire/retry/recovery. Its current system profile gate is not passed.

## Decision classification and limits

```text
USER_DIRECTED_PROVISIONAL_CHASSIS = NanoClaw
DECISION_BASIS = STRONGEST_CURRENT_POSITIVE_PIN_AND_ATENTO_SCOPE_EVIDENCE + ALTERNATIVE_PIN_BLOCKERS
SELECTION_TYPE = PROVISIONAL_PROJECT_DIRECTION
FULL_ATENTO_THREE_ROLE_GATE = NOT_PASSED
PRODUCTION_QUALIFICATION = NOT_ESTABLISHED
COMPARABLE_THREE_CANDIDATE_OPERATIONAL_COST_RANK = NOT_ESTABLISHED
MISSING_DATA_ALONE_USED_AS_ELIMINATION = NO
```

The phrase “by elimination and lack of data” is not recorded as a test conclusion: the frozen protocol treats missing or non-transferable evidence as unresolved, not failed. AI Butler is blocked on its current pin by an observed security gate; QwenPaw is held on its current profile due to a known fail-open/background-authority gap. These dispositions are pin/profile-specific and can change after remediation and requalification.

The selection authorizes treating NanoClaw as the current base for bounded follow-up work. It does not imply deployment approval, security acceptance, completed three-role composition, or a measured cost advantage. Keep all passing tests and external benchmark runs as already done; do not rerun them. Continue only with the uncovered NanoClaw integration/recovery deltas and record any repaired competing pin as a new, separately requalified candidate.

## Next bounded work

1. Continue from the NanoClaw pin and existing passing Atento harness.
2. Close the production gateway/provider credential-custody and wiring seam with synthetic credentials and inert effects.
3. If the runtime seam supports it, run one bounded three-role scheduled task across one host-process restart and one retry, confirming that authority remains bound to the original role.
4. Capture the implementation/change footprint and operational assumptions separately; do not claim cost savings without comparable measurements.
5. Reopen the comparative choice only if NanoClaw hits a hard-gate failure or an alternative receives a repaired frozen pin with directly comparable evidence.

## References

- [Gate 2 continuation and NanoClaw probe](system-chassis-gate2-continuation-2026-10-01.md)
- [Isolation residual](system-chassis-top3-isolation-residual-2026-10-01.md)
- [Reliability and recovery block](system-chassis-top3-reliability-recovery-2026-10-01.md)
- [Latency block](system-chassis-top3-latency-2026-10-01.md)
- [Operational-cost block](system-chassis-top3-operational-cost-2026-10-01.md)
