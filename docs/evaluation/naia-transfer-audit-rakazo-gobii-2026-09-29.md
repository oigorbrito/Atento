# NAIA upstream transfer audit — Rakazo / Gobii — 2026-09-29

## Contract

This record determines which Rakazo and Gobii upstream mechanisms are reusable for NAIA without rerunning equivalent tests locally, and which properties remain Atento-specific deltas.

It does not rank, shortlist, qualify, accept or select either candidate.

```text
UPSTREAM_TEST_SOURCE != CURRENT_PIN_RUNTIME_PASS
TRANSFERABLE_WITH_CONSTRAINTS != ATENTO_ACCEPTED
CONFIGURABLE_APPROVAL != SAFE_DEFAULT
SERIALIZED_EVENT_PROCESSING != EXACTLY_ONCE_EXTERNAL_EFFECT
```

Pins:

```text
Rakazo  f4583525d632fcd8643fd6e24c7f51e3e04cb990
Gobii   c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb
```

Exact-pin CI visibility has since been re-audited.

Rakazo now has direct hosted evidence at the frozen pin. See:

`docs/evaluation/rakazo-exhaustive-verification-2026-09-30.md`

Observed Rakazo status:

```text
unit = 5504 passed / 172 skipped
postgres journeys = PASS
push web E2E = 154 passed / 1 failed
later same-pin nightly web E2E = 155 passed
```

The single browser failure is retained as mixed/flaky same-pin evidence; it is not erased by the later green run.

Gobii execution is tracked separately and should not inherit Rakazo's result.

---

## 1. Rakazo

### 1.1 Space is a real application privacy boundary

The current database migration states directly:

```text
A space is the application privacy boundary.
```

The migration carries `spaceId` across:

- bots;
- threads;
- runs;
- routines;
- external effects;
- memory documents;
- agent homes;
- browser profiles;
- computers;
- connector/MCP state;
- secrets;
- approval rules;
- artifacts;
- capability installs.

It also adds foreign keys and membership constraints around space-scoped records.

Current source in `packages/db/src/spaces.ts` enforces membership when creating a sibling Space and when creating/deleting Space content. Missing membership raises `IsolationError`.

Each new Space receives its own user memory document.

Transfer classification:

```text
SPACE_MEMBERSHIP_BOUNDARY = UPSTREAM_PROVEN_BY_SOURCE
SPACE_SCOPED_DATA_MODEL = STRONG
SPACE_SCOPED_MEMORY = PRESENT
```

This is substantially stronger evidence than the UI-only Spaces E2E.

### 1.2 Credential scope

Rakazo deliberately separates account-level model/voice credentials from data-bearing credentials.

The migration states:

- model and voice keys are account-level;
- connector, MCP, memory-provider, webhook and other data-bearing secrets remain in one Space.

Bot-secret execution additionally uses a scope containing:

```text
userId
spaceId
botId
```

Upstream conformance/integration tests verify:

- reusable secret save/reuse/rotation/revocation;
- bot-secret plaintext is injected at execution but not returned to the model;
- OAuth access/refresh/client secrets are redacted from model-visible tool results and errors;
- live rotated OAuth material is re-read;
- bot secret plaintext is absent from visible prompt/history/tool surfaces.

Transfer classification:

```text
DATA_BEARING_CREDENTIAL_SPACE_SCOPE = UPSTREAM_PROVEN_BY_SOURCE_TESTS
BOT_SECRET_EXECUTION_SCOPE = USER+SPACE+BOT
MODEL_VISIBLE_SECRET_REDACTION = UPSTREAM_PROVEN_BY_SOURCE_TESTS
```

For strict NAIA/Anna deployment, account-level model credentials may still be intentionally shared. That is not equivalent to shared data-bearing authority.

### 1.3 Approval replay binding

Rakazo's approval-effect layer binds approval envelopes to:

- connector id;
- resource id;
- tool name;
- optional resource revision;
- approved arguments.

A changed resource revision can invalidate a persisted approval replay. The source explicitly handles OAuth reauthorization as a case where stale approval must not silently authorize a newly authenticated account.

Transfer classification:

```text
APPROVAL_ARGUMENT_BINDING = STRONG
APPROVAL_RESOURCE_BINDING = STRONG
STALE_RESOURCE_REVISION_REPLAY = FAILS_CLOSED
```

Equivalent local unit tests are not justified if NAIA leaves this mechanism unchanged.

### 1.4 External-effect ambiguity

The external-effect state machine includes:

```text
intended
approved
executing
completed
denied
uncertain
```

Duplicate handling is explicit:

- completed => return persisted result;
- denied => return denial;
- approved => one claimant may execute;
- intended => remain paused;
- executing => mark/return uncertain rather than blind replay;
- uncertain => return the uncertainty result.

The user-visible uncertainty result says the earlier execution may have completed and is **not replayed to avoid a duplicate side effect**.

This is a materially stronger generic effect contract than candidates that merely persist a local idempotency token.

But it still does not establish provider reconciliation / exactly-once completion after the ambiguous window.

Transfer classification:

```text
BLIND_REPLAY_AFTER_CRASH = PREVENTED_BY_CONTRACT
AMBIGUOUS_EFFECT_STATE = EXPLICIT
GENERIC_PROVIDER_RECONCILIATION = NOT_PROVEN
GENERIC_EXACTLY_ONCE_EFFECT = NOT_CLAIMED
```

Future Atento work should test only concrete consequential adapters that need reconciliation beyond the upstream uncertain-state contract.

### 1.5 Consequential-action default

The current Rakazo Playwright E2E explicitly tests:

```text
actions run by default while optional confirmations live in advanced user settings
```

The same test then configures a rule and verifies:

- deny;
- allow once;
- always allow this tool.

Therefore:

```text
APPROVAL_MECHANISM = STRONG
DEFAULT_MATCHES_HARDENED_NAIA = NO
ATENTO_DELTA = EXPLICIT_APPROVAL_RULESET
```

NAIA must not inherit the default action posture.

### 1.6 Computer isolation

Rakazo documents two materially different computer topologies.

Team Computer:

- shared OS user/workspace;
- each bot receives a distinct display and persistent Chrome profile;
- useful concurrency and browser identity separation;
- explicitly **not** a security boundary between mutually untrusted bots.

Private Computer:

- whole workspace belongs to one bot;
- appropriate when workloads require isolation.

The computer container is the security boundary.

Therefore:

```text
TEAM_COMPUTER_BROWSER_PROFILE_SEPARATION = PRESENT
TEAM_COMPUTER_STRICT_AGENT_ISOLATION = NO
PRIVATE_COMPUTER_ISOLATION_UNIT = AVAILABLE
```

Strict NAIA/Anna composition should not place both roles inside one Team Computer merely because their browser profiles differ.

### 1.7 Routines / persistence

Current Playwright coverage includes a routine test-run that:

- creates a schedule;
- runs the routine;
- observes the durable result;
- reloads the UI;
- verifies both result and schedule remain present.

This is useful persistence evidence.

It is not a process-crash fault-injection proof by itself.

```text
ROUTINE_UI_PERSISTENCE = UPSTREAM_E2E_PRESENT
PROCESS_CRASH_RESTART_PROOF = REQUIRES_SEPARATE_EVIDENCE
```

### 1.8 Rakazo residual

```text
RAKAZO_ATENTO_DELTA:
  - explicit fail-closed/consequential approval profile
  - strict NAIA/Anna topology: separate Spaces + Private Computers or separate runtime boundary
  - broker-only cross-role handoff
  - provider-specific reconciliation only where uncertain-state handling is insufficient

LOCAL_GENERIC_NCP_NOW = NO
```

---

## 2. Gobii

### 2.1 Agent-scoped persistent state

Gobii's operational SQLite state is keyed by the persistent agent id.

The persistence/recovery tests cover:

- healthy round-trip through durable storage;
- checkpointing;
- restoration to the latest known-good checkpoint after corruption;
- quarantine of corrupt archives;
- preservation of canonical state on storage/read/upload failures;
- recovery subprocess safety.

This supports:

```text
AGENT_SQLITE_STATE_SCOPE = PER_AGENT
STATE_PERSISTENCE_RECOVERY_MECHANISM = STRONG
```

It does not by itself prove all non-SQLite product state survives arbitrary process crashes.

### 2.2 Event-processing serialization and redelivery

Gobii uses per-agent event-processing locking.

Unit tests cover:

- lock-busy => persist agent in pending set + schedule a later drain;
- already-scheduled drain => no redundant drain scheduling;
- stale lock => clear and reacquire;
- lock-release failure => preserve locked-index evidence;
- redelivered agent work has explicit stale-lock handling.

This is strong evidence that duplicate workers are serialized and pending work is not simply dropped when a lock is busy.

Transfer classification:

```text
PER_AGENT_PROCESSING_SERIALIZATION = UPSTREAM_PROVEN_BY_SOURCE_TESTS
LOCK_BUSY_PENDING_DRAIN = UPSTREAM_PROVEN_BY_SOURCE_TESTS
STALE_LOCK_RECOVERY = UPSTREAM_PROVEN_BY_SOURCE_TESTS
ARBITRARY_EXTERNAL_EFFECT_EXACTLY_ONCE = NOT_PROVEN
```

Do not reinterpret queue/lock durability as exactly-once external side effects.

### 2.3 Secure credential delegation

Gobii has a particularly useful real-harness eval family for credential delegation.

The scenario:

- does not support simulation;
- runs through the real agent harness;
- requires discovery/enabling of secure credential delegation;
- requires `secure_api_request`;
- rejects ordinary HTTP/browser retrieval as an acceptable path;
- passes sensitive values as opaque delegated references;
- installs the resolved secret into the intended child agent/domain/key;
- verifies plaintext does not appear in tool outputs.

Gobii also has explicit secret scopes:

- Gobii-scoped;
- global user;
- organization;
- system-skill profile.

Transfer classification:

```text
OPAQUE_SECURE_VALUE_DELEGATION_PROTOCOL = STRONG
CHILD_AGENT_SECRET_ASSIGNMENT_SCOPE = DIRECTLY_TESTED
PLAINTEXT_TOOL_OUTPUT_LEAK = TESTED_NEGATIVE
LIVE_EVAL_RESULT_AT_CURRENT_PIN = NOT_OBSERVED
```

Because the scenario source is present but no committed live-result artifact was observed, the protocol is reusable evidence but not a current-pin behavioral PASS.

### 2.4 Contact authorization vs email review

Gobii has separate gates that must not be conflated.

#### Contact gate

The `PersistentAgent.contact_approval_mode` database default is:

```text
require_approval
```

Tests confirm the settings payload defaults to required approval.

The default whitelist behavior for a user-owned agent allows outbound email to the verified owner and blocks an unknown external recipient.

An explicit `AUTO_APPROVE_EMAIL` mode can add new email contacts automatically. SMS remains approval-controlled.

Therefore:

```text
NEW_EXTERNAL_CONTACT_DEFAULT = FAILS_CLOSED
CONTACT_AUTO_APPROVAL = OPT_IN
```

#### Review-before-send gate

Email content review is a different policy layer.

The code supports:

- `review_all_external`;
- `review_new_contacts`;
- `send_automatically`.

A migration deliberately pinned legacy/new non-pilot workspace defaults to `send_automatically` while preserving stricter pilot defaults.

Organization policy can impose a stricter minimum mode.

Critically, tests establish that changing email sending mode to `send_automatically` **does not enable contact auto-approval**.

Therefore:

```text
CONTACT_AUTHORIZATION != EMAIL_CONTENT_REVIEW
DEFAULT_UNKNOWN_EXTERNAL_RECIPIENT = BLOCKED_BY_CONTACT_GATE
DEFAULT_EMAIL_CONTENT_REVIEW = MAY_BE_AUTOMATIC_BY_WORKSPACE_POLICY
```

For NAIA, these must be configured independently:

- who may be contacted;
- whether exact outbound content requires review.

### 2.5 Scheduled work / eval protocol

Gobii's `scheduled_work_cycles` real-harness eval verifies:

- a scheduled wake through the real agent harness;
- consultation of owned SQLite work state;
- no message-history polling as a freshness mechanism;
- empty queue => quiet completion;
- one ready item => one exact peer dispatch.

This is a high-value product behavior protocol.

No exact-pin live eval artifact was observed, so:

```text
SCHEDULED_WORK_PROTOCOL = STRONG
LIVE_CURRENT_PIN_RESULT = NOT_OBSERVED
```

### 2.6 Peer handoff / data minimization

The structured handoff eval suite verifies:

- exact record-field preservation;
- record-batch boundaries;
- one intended persisted handoff;
- file handoff to the intended peer;
- no manufacturing of structured data for a prose-only question;
- a scoped handoff that preserves operational fields while forbidding unrelated sensitive context.

This maps well to an eventual explicit NAIA/Anna broker contract, but Gobii's native peer link is not automatically the Atento broker.

```text
STRUCTURED_PEER_HANDOFF_PROTOCOL = STRONG
SENSITIVE_CONTEXT_MINIMIZATION_SCENARIO = PRESENT
ATENTO_BROKER_EQUIVALENCE = NOT_ESTABLISHED
```

### 2.7 Strict NAIA / Anna isolation

Gobii exposes strong per-agent state/secrets and native peer links.

However it also intentionally supports wider secret scopes and organization-level collaboration.

The strict Atento requirement is therefore not merely “two Gobiis exist”; it is a deployment/configuration statement:

```text
NAIA secret scope = agent-specific where role-specific
ANNA secret scope = agent-specific where role-specific
shared/global/org secrets = explicitly audited, not inherited
peer communication = explicit broker/allowlisted route only
memory/state = separate agent UUID/storage
```

A later local composition test is justified only if Gobii reaches the shortlist and the exact topology above cannot be proven fully from source/upstream tests.

### 2.8 Gobii residual

```text
GOBII_ATENTO_DELTA:
  - freeze NAIA-specific contact + email-review policy
  - audit any global/org secret grants crossing NAIA/Anna roles
  - map native peer messaging onto the explicit Atento handoff boundary
  - provider-specific external-effect reconciliation where queue serialization is insufficient
  - live/current-pin eval only if decision-critical behavior remains unproven after upstream artifacts are exhausted

LOCAL_GENERIC_NCP_NOW = NO
```

---

## 3. Transfer summary

| Property | Rakazo | Gobii |
|---|---|---|
| persistent state scope | Space/Bot-scoped product model | per-agent SQLite + persistent models |
| credential isolation | data-bearing secrets Space-scoped; bot secrets include bot scope | Gobii-scoped secrets + explicit broader scopes |
| plaintext secret exposure | negative conformance tests | opaque delegation protocol + negative output check |
| approval default | consequential actions permissive unless rules configured | external contact default fails closed; email content review is separate and can be automatic |
| approval binding | connector/resource/tool/revision + args | request/contact/outbox/change-specific gates |
| ambiguous external effect | explicit `uncertain`, no blind replay | queue/lock durability strong; generic effect reconciliation not established |
| scheduled work | persisted routine E2E | real-harness scheduled-work eval protocol |
| strict multi-agent isolation | separate Space + Private Computer needed for strongest boundary | per-agent state strong; broader org/global scopes must be constrained |
| current-pin hosted runtime result | unit/Postgres green; one push E2E red, later same-pin 155/155 nightly green | tracked separately; see subsequent verification records |

No row is a score or ranking.

## 4. Consequence for NCP

Rakazo and Gobii both eliminate several generic local probes because directly relevant upstream mechanisms already exist.

Future local work, if either candidate reaches a shortlist, should be restricted to **composition deltas**:

```text
Rakazo:
  hardened approval rules
  + separate Space/private-computer role topology
  + explicit broker
  + only adapter-specific ambiguous-effect reconciliation

Gobii:
  hardened contact/content-review policy
  + strict secret-scope topology
  + explicit broker mapping
  + only adapter-specific ambiguous-effect reconciliation
```

Do not rerun upstream secret redaction, state recovery, lock serialization, approval replay binding or scenario source tests merely to duplicate them.

```text
TRANSFER_AUDIT_RAKAZO_GOBII = COMPLETE_V1
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
