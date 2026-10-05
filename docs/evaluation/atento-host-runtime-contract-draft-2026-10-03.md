# Atento host-runtime contract — draft

- Status: `PROPOSED; NOT_IMPLEMENTED; NOT_ACCEPTED`
- Scope: runtime boundary needed to execute the complete NAIA/Anna/Apollo system-chassis profile against a real Atento host.
- Authority: subordinate to `docs/adr/ADR-001-naya-product-composition.md` and `docs/adr/ADR-003-evidence-first-engineering-decision-policy.md`.
- Decision: this draft makes the test seam concrete. It does not select a deployment topology or chassis and does not claim a passing implementation.

## Decision record

```text
ATENTO_PRODUCT_HOST_IMPLEMENTATION = ABSENT_IN_REVIEWED_TREE
TRUSTED_IDENTITY_ISSUER = UNDECIDED
PROCESS_LIFECYCLE_OWNER = UNDECIDED
HANDOFF_TRANSPORT = REFERENCE_BROKER_ONLY; PRODUCT_WIRING_ABSENT
RTO = TBD_BY_PRODUCT_OWNER
RPO = TBD_BY_PRODUCT_OWNER
HOST_CONTRACT_STATUS = BLOCKED_UNTIL_ADOPTED_AND_IMPLEMENTED
```

`RTO` and `RPO` are required product objectives, not values an evaluator may infer. Until they are approved for each state class below, recovery assertions that depend on them remain `BLOCKED/UNRESOLVED`. A value of “a definir” is not a zero-minute/zero-loss objective and cannot pass SYS-STATE-01.

## 1. Trusted role identity

The host MUST obtain role identity from an authenticated, host-controlled execution binding. The user request, prompt text, channel display name, model output, environment variable writable by the agent, or caller-supplied role string alone MUST NOT establish authority.

At execution start, the host binds an immutable tuple:

```text
ExecutionIdentity = {
  principal_id,
  role_id: NAIA | ANNA | APOLLO,
  session_id,
  run_id,
  generation,
  granted_capability_set,
  issued_at,
  expires_at,
  issuer,
  integrity_proof
}
```

Requirements:

- `issuer` is a trusted Atento control-plane component or an explicitly approved authenticated channel-to-role mapping; the specific issuer and mapping store remain undecided.
- The binding is authenticated and integrity-protected end-to-end to the runtime/adapter boundary. The adapter MUST reject missing, invalid, expired, revoked, or mismatched role/session/run bindings.
- Each role resolves only its own private state root, credentials, and capability set. A role name in a path or request body is not authorization.
- Identity is revalidated at each handoff, delayed/retried dispatch, and consequential tool boundary. A child run receives an explicit equal-or-narrower grant; it does not inherit ambient authority.
- Logs and traces record identity references and authorization decisions, never credential values or private cross-role payloads.

Unresolved product decision: name the trusted issuer, enrollment/mapping authority, revocation path, and the mechanism by which the host proves the binding to each candidate adapter.

## 2. Process and run lifecycle

The host, not the candidate process or model, owns process supervision, cancellation, durable run state, retry scheduling, and terminal delivery. Each run has a unique `run_id` and monotonic `generation`; stale generations cannot resume, acknowledge, or recreate authority.

Minimum lifecycle:

```text
ACCEPTED -> CLAIMED -> RUNNING -> EFFECT_PENDING -> ACKED
                         |              |
                         +-> RETRY_WAIT <-+ (only if retry policy permits)
                         +-> FAILED_TERMINAL
                         +-> CANCELLED
```

The durable host record MUST bind run ID, generation, role identity reference, session reference, state version, attempt count, idempotency key (where supported), lease/claim owner, timestamps, and terminal result reference. Transitions use compare-and-set or an equivalent atomic conditional update. Acknowledgement is accepted only from the current claim/generation after the required effect/result is durably recorded. A stale worker cannot ack or overwrite a newer run.

After process death between claim and ack, the host MUST detect lease expiry/revocation, preserve the prior attempt as an auditable nonterminal attempt, and make exactly one policy-authorized retry eligible under a freshly validated identity. Whether a side effect may be retried depends on that adapter's idempotency/readback/reconciliation contract; generic exactly-once effects are not implied. Exhaustion or a non-retryable error yields one terminal failure delivery. Duplicate terminal deliveries MUST be deduplicable by stable run/result identity.

This draft fixes the lifecycle semantics needed by the test; it does not choose a process manager, queue, database, lease duration, retry backoff/count, or delivery transport. Those are implementation/profile inputs to freeze before execution.

## 3. State classes and recovery objectives

For each class, the implementation MUST declare its authoritative store, durability boundary, backup/replication behavior, and recovery test. Product owner must set the maximum RTO and RPO for each class (or explicitly approve a shared bound):

| State class | Minimum recovery property | Objective |
|---|---|---|
| Role-private memory and files | Restore only to its owning role; no cross-role visibility after recovery | RTO/RPO `TBD` |
| Sessions and conversation pointers | Resume the correct role/session without importing another role's transcript | RTO/RPO `TBD` |
| Run/claim/retry/ack ledger | Reconcile an interrupted claim; no stale ack or broadened grant; bounded loss/duplication per adapter contract | RTO/RPO `TBD` |
| Handoff requests and receipts | Preserve sender, intended recipient, minimal payload reference, consent/authorization decision, and terminal status | RTO/RPO `TBD` |
| Credential and capability references | Reconstitute only by trusted secret/capability services; never recover secret values into another role's state | RTO/RPO `TBD` |
| Audit/security events | Preserve enough integrity-protected evidence to reconstruct identity and authorization decisions | RTO/RPO `TBD` |

RPO applies to recoverable state, not permission to replay a potentially completed external side effect. If provider outcome is ambiguous, use adapter-specific reconciliation or stop for a safe terminal/held state according to the effect policy.

## 4. Required adapter seam

Any candidate adapter bound to the Atento host MUST implement an interface equivalent to:

```text
startRun(authenticatedExecutionIdentity, inputRef) -> runHandle
claim(runHandle, expectedGeneration) -> claimLease | denied
dispatch(runHandle, claimLease, inputRef) -> resultRef | retryableError | terminalError
ack(runHandle, claimLease, resultRef) -> terminalReceipt | staleOrUnauthorized
cancel(runHandle, expectedGeneration, reason) -> cancellationReceipt
recover(runId) -> recoveredState | notFound | integrityFailure
```

The host retains authority over identity resolution, grant evaluation, durable state transitions, retry eligibility, and terminal delivery. Candidate-specific code may execute a task but MUST NOT self-assign another role, skip the broker, or mutate the host ledger outside this seam. Exact transport/schema may be refined by an implementation ADR, while preserving these invariants.

## 5. Decisive integration test once a real host exists

Use inert synthetic role identities, isolated temporary stores, and a deterministic fault injector; do not use production credentials or external side effects.

1. Resolve a run for NAIA, Anna, and Apollo from the trusted host issuer; reject caller/prompt role spoofing and invalid/revoked identities.
2. Prove private store, tool grant, and credential-reference separation for all role pairs.
3. Create a typed Anna→NAIA and Apollo→NAIA handoff; reject wrong recipient, untyped/overbroad payload, and authority-bearing fields; authorize again under NAIA identity.
4. Claim one NAIA task, terminate the worker after claim and before ack, then restart the **host process** and recover from the durable ledger.
5. Demonstrate one authorized retry under a fresh valid NAIA claim; reject stale-generation ack and cross-role retry; inject a duplicate delivery and verify deduplication.
6. Complete and persist one successful terminal delivery; separately exhaust/reject a run and verify one terminal failure delivery.
7. Measure outage-to-service and lost durable state against the approved per-class RTO/RPO; retain logs/artifacts and check for unauthorized cross-role access.

Acceptance: every mandatory assertion passes on the complete Atento composition; zero unauthorized cross-role access; no assertion passes only as `PASS_WITH_SCOPE`; recovery meets the approved RTO/RPO. If the host seam, approved objectives, or observable boundary is absent, record `BLOCKED/UNRESOLVED`, never a zero score or implicit pass.

## Reconciliation with current repository evidence

- `docs/adr/ADR-001-naya-product-composition.md` selects NanoClaw as the reference runtime for three isolated role groups and an Atento typed handoff. Production deployment topology, trusted identity issuer, and product host wiring remain undecided; this contract does not silently resolve those implementation choices.
- `docs/evaluation/system-chassis-gate2-continuation-2026-10-01.md` records that no Atento product host/runtime was found to bind the NanoClaw mailbox adapter to. The probe uses a test-harness broker and is explicitly `PASS_WITH_SCOPE`.
- `docs/evaluation/system-chassis-selection-metric-2026-10-02.md` requires persisted role state to meet predeclared RTO/RPO before eligibility. No product limits are approved; therefore this gate remains open.
- `evals/config/system_chassis_nanoclaw_v1.json` and `tools/system_chassis/nanoclaw.atento.test.ts` describe a candidate-facing profile/probe, not the missing Atento product host.

Current disposition:

```text
HOST_CONTRACT = DRAFTED_FOR_REVIEW
HOST_IMPLEMENTATION = ABSENT
RTO_RPO = UNSET
REFERENCE_RUNTIME = NANOCLAW
REFERENCE_TOPOLOGY = THREE_ISOLATED_ROLE_GROUPS + ATENTO_TYPED_HANDOFF
NANOCLAW_SYSTEM_GATE = NOT_PASSED
PRODUCTION_ELIGIBILITY = BLOCKED_UNRESOLVED
QUALIFIED_SYSTEM_CHASSIS_WINNER = NONE
```

The next implementation decision is to accept/revise this contract, choose the trusted identity issuer and lifecycle owner, and obtain product-owner RTO/RPO objectives. Once those are present in a real host implementation, run the decisive integration test above against frozen candidate pins. No candidate result is changed by this draft.
