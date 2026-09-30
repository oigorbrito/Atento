# TrustClaw contract audit — 2026-09-29

## Contract

This audit establishes the pinned TrustClaw product/runtime boundaries and the external dependencies that become part of NAIA's authority/cost model.

It does not rank candidates, create a shortlist, or treat vendor-managed execution as locally verified policy.

Source:

`ComposioHQ/trustclaw@c07410bccb916236b45b563e8c4ff76ad83d3855`

```text
MANY_TOOLS != LOCAL_AUTHORITY_PROOF
OAUTH_CONNECTION != PER_ACTION_APPROVAL
SELF_HOSTABLE_APP != FULLY_SELF_CONTAINED_RUNTIME
STATIC_SOURCE != CURRENT_PIN_RUNTIME_PASS
```

Decision state remains:

```yaml
NAIA_BASE: NOT_SELECTED
NAIA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## 1. Product completeness

TrustClaw is a complete personal-assistant product surface:

- web chat;
- Telegram;
- persistent vector memory;
- long-running context compaction;
- scheduled/cron agent work;
- OAuth-connected external tools;
- authenticated user accounts;
- self-hostable Next.js deployment.

Therefore:

```text
PRODUCT_COMPARABLE = YES
PERSISTENT_ASSISTANT_SURFACE = ESTABLISHED_SOURCE/DOCS
```

## 2. Memory isolation

The local memory implementation is explicitly scoped by `instanceId`.

Observed contracts:

- `memory_save` writes `instanceId` with every memory record;
- `memory_search` filters by the same `instanceId`;
- automatic memory retrieval for context also filters by `instanceId`;
- compaction memory flush receives the current instance and only the memory save/search tools for that instance;
- user-facing instance lookup is bound to the authenticated user.

Embeddings are generated through the AI SDK using `openai/text-embedding-3-large`.

Classification:

```text
INSTANCE_MEMORY_ISOLATION = STRONG_STATIC_EVIDENCE
CROSS_INSTANCE_MEMORY_READ = NOT_OBSERVED_IN_AUDITED_PATH
EMBEDDING_PROVIDER_DEPENDENCY = EXTERNAL
```

The memory database may be self-hosted, but embedding generation remains part of the external model-service dependency unless replaced.

## 3. External-tool authority boundary

Agent setup creates a Composio session using:

`composio.create(instance.userId, ...)`

and then imports the returned Composio tool set into the agent.

This gives a useful user-scoping anchor:

```text
COMPOSIO_SESSION_SUBJECT = instance.userId
```

The system prompt requires a service to be connected before execution and directs the agent to obtain connection URLs through Composio rather than fabricating them.

However, the audited TrustClaw repository does **not** establish a local per-action approval/allowlist policy comparable to Atento's required authority contract.

The effective authorization of Gmail/GitHub/Slack/etc. actions is materially delegated to:

- the user's Composio connections;
- the tool surface returned by the Composio session;
- Composio-managed execution/credential policy.

Therefore:

```text
USER_SCOPED_TOOL_SESSION = ESTABLISHED_SOURCE
LOCAL_PER_ACTION_APPROVAL_POLICY = NOT_ESTABLISHED
LOCAL_TOOL_ALLOWLIST_POLICY = NOT_ESTABLISHED
EXTERNAL_ACTION_AUTHORITY = COMPOSIO_DEPENDENT
```

This is not evidence that Composio is unsafe. It means the decisive external-action policy is outside the audited repository and must be qualified as a dependency rather than inferred.

## 4. Sandboxed execution boundary

Upstream documentation and product copy describe:

- remote sandboxed code execution;
- a persistent `COMPOSIO_REMOTE_WORKBENCH`;
- managed tool execution rather than local root execution.

Within the TrustClaw repository, the agent obtains those tools from `@composio/core` / `@composio/vercel`. The sandbox implementation itself is not owned by this repository.

Therefore:

```text
REMOTE_SANDBOX_PRODUCT_CONTRACT = ESTABLISHED_DOCS
REMOTE_SANDBOX_IMPLEMENTATION = EXTERNAL_DEPENDENCY
LOCAL_INDEPENDENT_SANDBOX_PROOF = NOT_ESTABLISHED
```

Any Atento qualification must test the effective Composio execution boundary, not merely inspect TrustClaw source.

## 5. Cron / recurring work

TrustClaw owns its scheduling records locally.

Observed static contracts:

- job create/list/delete scoped by `instanceId`;
- cron expression validation;
- persisted next-run state;
- production cron route requires `CRON_SECRET`;
- missing production secret fails closed;
- bearer comparison uses `timingSafeEqual`;
- execution uses a locking/fencing token (`lockedBy == invocationId`);
- rate limiting is performed per user;
- failed jobs release locks and record a generic error;
- Telegram delivery is optional after execution.

Classification:

```text
CRON_PERSISTENCE = STRONG_STATIC_EVIDENCE
CRON_AUTH = FAIL_CLOSED_STATIC
CRON_FENCING = PRESENT
USER_RATE_LIMIT = PRESENT
CRON_RUNTIME_EXECUTION_AT_PIN = NOT_OBSERVED
```

A scheduled run calls the same agent setup and therefore inherits the same Composio external-tool surface.

TrustClaw's system prompt tells scheduled runs to stay within the original intended scope, but that instruction is **prompt policy**, not an independent technical capability restriction.

```text
BACKGROUND_SCOPE_PROMPT = PRESENT
BACKGROUND_TECHNICAL_CAPABILITY_SUBSET = NOT_ESTABLISHED
```

That distinction is material for NAIA.

## 6. Deployment / provider dependency surface

The current architecture requires or strongly assumes:

- Postgres + pgvector;
- `COMPOSIO_API_KEY`;
- Composio for external tool sessions/connections;
- Vercel AI Gateway model routing in the documented architecture;
- external embedding model;
- Vercel Cron / production route model in the standard deploy path;
- optional Redis for resumable streams/abort flags.

The CLI explicitly provisions a Vercel deployment and related services.

Classification:

```text
SELF_HOSTABLE_APPLICATION_CODE = YES
FULLY_SELF_CONTAINED_RUNTIME = NO
CLOUD_PLATFORM_DEPENDENCY = MATERIAL
COMPOSIO_DEPENDENCY = MATERIAL
MODEL/EMBEDDING_EXTERNAL_DEPENDENCY = MATERIAL
```

A non-Vercel deployment may be technically possible because this is a Next.js application, but parity of cron/model/tool execution outside the standard path is not established by this audit.

## 7. Channel maturity

The concrete user-facing communication surfaces established here are:

- web;
- Telegram.

The project UI contains other channel concepts, but the audited product contract must not convert disabled/planned surfaces into current channel capability.

```text
WEB = PRESENT
TELEGRAM = PRESENT
OTHER_CHANNEL_BREADTH = NOT_CLAIMED
```

## 8. Hosted execution visibility

For exact pin:

`c07410bccb916236b45b563e8c4ff76ad83d3855`

the available GitHub connector reports:

```text
workflow_runs = []
combined_statuses = []
```

No current-pin CI/runtime pass or failure is claimed.

## 9. Current disposition

```text
TRUSTCLAW_PRODUCT_COMPARABLE = YES

STRONG_LOCAL_STATIC:
  - instance-scoped memory
  - local persistent cron records
  - cron auth/fencing
  - authenticated user/instance binding

EXTERNALIZED_CONTRACTS:
  - external tool execution/credentials = Composio
  - remote execution sandbox = Composio-managed
  - model routing = cloud/provider dependent
  - embeddings = external model
  - standard production scheduling/deploy = Vercel-oriented

MATERIAL_NAIA_GAPS:
  - no local per-action external-effect approval policy established
  - no local technical capability subset for background jobs established
  - external dependency/cost/availability boundary not measured
  - generic browser/computer-use is not established as a local product surface
  - exact-pin runtime execution not observed

TRUSTCLAW_CURRENT_PIN_QUALIFIED = NO
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## 10. Smallest next probe

If TrustClaw remains decision-relevant, avoid a broad tool-count test.

Execute a dependency-aware probe:

1. create one isolated test user/instance;
2. connect one low-risk external service through Composio;
3. save/retrieve memory and restart the app;
4. create one scheduled job;
5. prove scheduled execution remains bound to the same user/connection;
6. attempt an unconnected external action and preserve the denial/failure evidence;
7. determine whether a dangerous/destructive tool can require a technical human approval or only model/prompt discretion;
8. measure external calls, monetary cost and wall time;
9. simulate Composio unavailability and observe whether local assistant/memory/scheduling degrade safely;
10. preserve raw evidence.

Acceptance must separate:

```text
LOCAL_CHASSIS_PASS
COMPOSIO_DEPENDENCY_PASS/FAIL
BACKGROUND_AUTHORITY_PASS/FAIL
COST_OBSERVED
```

Until then:

```text
TRUSTCLAW_RUNTIME_TRANSFER = PENDING
```
