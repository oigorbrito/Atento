# OpenMausBot current-pin delta audit — 2026-09-29

## Contract

This record audits only the material delta from the **last Atento-reviewed comparison pin** to the current observed OpenMausBot head.

It does not re-run the historical qualification, create a shortlist or select the NAIA base.

```text
HISTORICAL_EVIDENCE != CURRENT_PIN_PROOF
TEST_SOURCE_PRESENT != TEST_EXECUTED
STATIC_TRANSFER != RUNTIME_TRANSFER
```

Candidate:

`milind-soni/OpenMausBot`

Last Atento-reviewed comparison pin:

`56ac27a01a2ceb27d44c3ef0cf8d63f692f68cb8`

Current observed head:

`6005b1bf5883a7ffa639c07e729321f89b9532e1`

Git delta:

```text
ahead = 4 commits
behind = 0
```

## 1. Material delta

The four-commit delta is concentrated in Cloud-home/lending memory, session/auth and workspace surfaces.

Material changed paths include:

- `server/lending-memory.ts` + unit tests;
- `server/cloud-lending-memory.e2e.test.ts`;
- `server/cloud-lending.ts`;
- `server/cloud-home.ts` + tests;
- `server/request-auth.ts` + tests;
- `server/sessions.ts` + tests;
- `server/memory-upkeep.ts` + tests;
- `server/routes/bot-memory.ts`;
- workspace/memory UI and related tests.

This is decision-relevant because prior Atento evidence already identified authority and shared-computer/memory boundaries as material.

## 2. Lending-memory hardening

At the current pin, `server/lending-memory.ts` adds a persistent fingerprint record over memory and instruction files that can influence a bot turn.

Observed static contracts:

- fingerprints `MEMORY.md`, memory topics/logs and working-folder instruction files;
- tracks turns not provably written by the owner as `pending`;
- if relevant files change while such a turn is pending, marks the bot `flagged`;
- a flagged bot's lent-Mac access remains blocked until owner review;
- review is bound to the exact current fingerprint/token;
- a stale review token is rejected;
- damaged/linked/oversized tracker state fails closed by flagging unknown bot state;
- owner/harness-trusted writes have a separate adoption path;
- symlinks are fingerprinted by target rather than silently dereferenced.

The module itself states a residual limitation: a foreign write racing a trusted write in the same moment cannot always be distinguished, and a full-access guest that already controls the Cloud machine is outside this protection.

Classification:

```text
LENDING_MEMORY_GUARD = PASS_STATIC
FAIL_CLOSED_RECORD_HANDLING = PASS_STATIC
OWNER_REVIEW_TOKEN_BINDING = PASS_STATIC
RACE_EDGE_CASE = DOCUMENTED_LIMIT
```

## 3. Real-server E2E wiring evidence

`server/cloud-lending-memory.e2e.test.ts` is not a mock-only unit test.

The test source:

- starts the real `server/index.ts` with `OMB_CLOUD_ROLE=home`;
- pairs an owner and a client/guest session;
- creates a real computer-sharing connector fixture;
- injects a foreign memory write;
- observes that computer enumeration/use becomes unavailable;
- checks the Memory review API;
- rejects review by a guest;
- rejects review from an untrusted local Cloud process;
- requires the owner's exact review token;
- restores Mac access only after owner review;
- covers room/guest conversation leakage and symlink-related cases.

Therefore the new guard is **wired into an intended real-server E2E path in source**.

However:

```text
E2E_SOURCE_WIRING = PASS_STATIC
E2E_EXECUTION_AT_CURRENT_PIN = UPSTREAM_CI_PASS
```

This was superseded by the all-events exact-head run query: CI run `36647214650` checked out the exact frozen SHA and succeeded. The four focused changed-contract tests were visible in the Ubuntu shard logs and passed; see the `OpenMausBot changed-contract tests` section in `candidate-upstream-ci-pin-audit-2026-09-30.md`.

## 4. Request/auth delta

Current `request-auth.ts` / tests preserve or add explicit authority boundaries.

Observed static contracts include:

- default-deny scope mapping: unlisted endpoints fall back to `admin`;
- client sessions cannot access admin computer/config/credential-style operations;
- public/remote companion mutations require the companion capability;
- loopback mutation authority can require packaged-desktop capability;
- requests that came through a proxy never inherit loopback-owner trust merely from a localhost Host header;
- session cookies require same-origin use;
- revoked/over-scoped sessions do not silently fall back to loopback ownership;
- rejected requests do not renew session TTL.

Classification:

```text
REQUEST_AUTH_DEFAULT_DENY = PASS_STATIC
REMOTE_CLIENT_ADMIN_SEPARATION = PASS_STATIC
LOOPBACK_PROXY_CONFUSION_DEFENSE = PASS_STATIC
CURRENT_PIN_CHANGED_CONTRACT_CI = PASS_WITH_SCOPE
ATENTO_COMPOSED_RUNTIME = NOT_RUN
```

## 5. Historical evidence transfer

### Evidence strengthened by the delta

The old shared-computer/memory concern is materially better characterized at the current pin.

```text
SHARED_COMPUTER_MEMORY_BOUNDARY:
  previous = NEEDS_REINFORCEMENT / historical concern
  current = STRONGER_STATIC_EVIDENCE
  current_runtime = UPSTREAM_CI_PASS_WITH_SCOPE
```

This does not by itself make the whole candidate qualified.

### Evidence that transfers unchanged

The four-commit delta does not invalidate the already established product surface:

- persistent assistant product;
- routines/background work;
- computer/browser capabilities;
- model/provider surface;
- user-facing desktop/mobile/product integration.

These remain historical evidence unless an adaptation changes them.

### Historical gaps not closed by this delta

No new proof in this four-commit delta closes:

```text
GENERIC_EXTERNAL_EFFECT_DURABILITY = NOT_PROVEN
INTERRUPTED_TURN_RECOVERY_EQUIVALENCE = NOT_PROVEN
NAIA_GENERAL_AUTHORITY_MODEL = STILL_REQUIRES_ATENTO_AUDIT
STRICT_ANNA_BOUNDARY = MUST_BE_ENFORCED_BY_ATENTO_COMPOSITION
```

The changed `sessions.ts` / request-auth surfaces are authentication/session-authority concerns and must not be reinterpreted as proof of interrupted LLM-turn recovery.

The old provider/delegation authority findings are not promoted merely because request auth improved.

## 6. Current-pin disposition

```text
OPENMAUS_CURRENT_PIN = 6005b1bf5883a7ffa639c07e729321f89b9532e1
PRODUCT_COMPARABILITY = ESTABLISHED
HISTORICAL_EVIDENCE_REUSE = YES
DELTA_STATIC_AUDIT = COMPLETE
DELTA_STATIC_RESULT = PASS_WITH_SCOPE
CURRENT_PIN_CHANGED_CONTRACT_EXECUTION = PASS_WITH_SCOPE
ATENTO_COMPOSED_RUNTIME_TRANSFER = PENDING
CURRENT_PIN_QUALIFIED = NO
SHORTLIST = NOT_SELECTED
WINNER = NOT_SELECTED
```

`PASS_WITH_SCOPE` here means only that the inspected delta adds/retains defensible static contracts; it is not a candidate qualification state.

## 7. Remaining decision-relevant boundary

The current-pin **upstream changed-contract test gate is closed**; do not rerun those files locally merely to repeat an already observed exact-pin CI result.

If OpenMausBot remains decision-relevant after the broader NAIA candidate set is narrowed by evidence, the next work is the Atento-specific composed authority/isolation boundary. It requires a frozen NAIA/Anna topology and must distinguish two bots belonging to one owner from the owner/guest boundary tested upstream.

Until that composition is frozen and its result can change the candidate decision:

```text
CURRENT_PIN_CHANGED_CONTRACT_CI = PASS_WITH_SCOPE
ATENTO_COMPOSED_RUNTIME = NOT_RUN
NAIA_BASE = NOT_SELECTED
```
