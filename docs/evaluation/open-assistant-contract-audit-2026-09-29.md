# Open Assistant static contract audit — 2026-09-29

## Scope

Repository: open-assistant-org/open-assistant
Pinned commit: 32c55d2643f9fe38777f9212588b2eee45392514
Pinned release bump: v1.4.9
Audit mode: exact-pin static contract inspection only

This audit does not select, shortlist, qualify, accept, or promote Open Assistant.

Rules preserved:

~~~text
BENCHMARK_SIGNAL != LOCAL_PROOF
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED
HISTORICAL_EVIDENCE != CURRENT_PIN_PROOF
STATIC_SOURCE != RUNTIME_PASS
SMALL_CORE != LOW_TOTAL_MIGRATION_COST
~~~

The repository tree was inspected recursively at the exact pin and the relevant files were fetched directly. Empty code-search results were not used as evidence of absence.

## 1. Memory and persistence

The memory repository persists conversation memory in the database and scopes reads/writes by conversation_id. The memory service reconstructs context from messages, facts and long-term summaries and can auto-compact conversation history.

Established source contracts:

- persistent conversation memory;
- typed memory classes such as facts and long-term summaries;
- context reconstruction after process restart, assuming the same database is reopened;
- per-conversation memory lookup.

Boundary:

The observed storage key is conversation_id, not an independent NAIA/Anna authority identity. The audit does not establish that two bounded assistants sharing one database cannot read or influence each other's memory through higher-level routing/configuration.

~~~text
PERSISTENT_MEMORY = ESTABLISHED_SOURCE
MEMORY_SCOPE = CONVERSATION_ID
STRICT_NAIA_ANNA_MEMORY_ISOLATION = NOT_ESTABLISHED
~~~

## 2. Scheduled/background execution

Cron jobs are stored in the database. CronJobService loads enabled persisted jobs when the scheduler starts. The repository records execution history and provides an execution lock for multi-instance scheduling. Migration 052 explicitly repairs lock columns and intentionally clears stale in-flight lock state during migration/restart.

The execution path supports:

- direct pinned-tool jobs through ToolExecutor;
- prompt/recipe jobs through MessageHandler;
- persisted next-run/last-run state;
- execution timeout;
- execution status recording;
- instance locking and lock release.

This is real scheduled/background infrastructure.

However, scheduled tool jobs execute through the same ToolExecutor authority surface. No independent technical rule was found that constrains background jobs to a capability subset narrower than interactive execution.

~~~text
CRON_PERSISTENCE = ESTABLISHED_SOURCE
RESTART_RELOAD_OF_PERSISTED_JOBS = ESTABLISHED_SOURCE
EXECUTION_LOCKING = PRESENT
BACKGROUND_TECHNICAL_CAPABILITY_SUBSET = NOT_ESTABLISHED
~~~

## 3. Tool registry and authority

The registry gates integrations by settings and MessageHandler filters tools using the selected skills' configured tool lists.

Useful boundaries exist:

- disabled integrations are omitted;
- selected skills contribute explicit tool names;
- pinned sub-tasks can run with one skill;
- unknown/unavailable services fail rather than silently redirect.

Material authority limits:

- system/search meta surfaces are broadly available by registry policy;
- batch/loop meta-tools are always available;
- a generated multi-step plan can expand execution from the initially selected skills to all enabled skills;
- ToolExecutor executes registered plugin/MCP tools directly when their services are available;
- the executor has a short in-process duplicate-call cache, not durable idempotency;
- no repository-owned per-action approval/deny policy was found at the execution boundary.

Therefore skill assignment is a useful capability-selection mechanism, but it is not by itself the NAIA fail-closed authority contract.

~~~text
SKILL_TOOL_FILTERING = ESTABLISHED_SOURCE
SERVICE_ENABLE_GATING = ESTABLISHED_SOURCE
PLAN_SKILL_EXPANSION = PRESENT
LOCAL_PER_ACTION_APPROVAL_POLICY = NOT_ESTABLISHED
DURABLE_EXTERNAL_EFFECT_IDEMPOTENCY = NOT_ESTABLISHED
NAIA_TOOL_AUTHORITY_FIT = NEEDS_HARDENING
~~~

## 4. Browser and computer-use

The exact pin contains a real Playwright browser implementation with:

- Chromium launch;
- navigation;
- accessibility-tree extraction;
- click/type/scroll actions;
- screenshot support;
- persistent in-process browser session between tool calls;
- Scrapling-based fetch modes.

The browser documentation explicitly warns that the browser can access internal networks and recommends firewalling and validation of user-provided URLs. The inspected BrowserService navigation path forwards the requested URL to the browser driver; an independent URL/network allowlist was not established in this audit.

The recursive source tree did not establish a desktop-level Windows/macOS computer-use subsystem comparable to candidates that expose native screen/input automation.

~~~text
BROWSER_AUTOMATION = ESTABLISHED_SOURCE
BROWSER_SESSION_REUSE = PRESENT
BROWSER_NETWORK_POLICY = REQUIRES_HARDENING/DEPLOYMENT_CONTROL
DESKTOP_COMPUTER_USE = NOT_ESTABLISHED
~~~

## 5. Credential handling

CredentialsRepository encrypts credential payloads using Fernet and requires an encryption key from SECURITY_ENCRYPTION_KEY or ENCRYPTION_KEY. The database lookup key is service_name.

This establishes encrypted-at-rest credential storage, but the observed repository does not bind stored credentials to an agent, profile or user identity. A shared process/database therefore needs an additional boundary if NAIA and Anna must not share credential authority.

~~~text
CREDENTIAL_ENCRYPTION = ESTABLISHED_SOURCE
ENCRYPTION_KEY_REQUIRED = YES
CREDENTIAL_SCOPE = SERVICE_NAME_GLOBAL
PER_AGENT_CREDENTIAL_ISOLATION = NOT_ESTABLISHED
~~~

## 6. Provider portability

The LLM client has explicit provider/base-URL configuration and source/docs for:

- OpenRouter;
- Anthropic;
- Groq;
- Ollama;
- vLLM;
- OpenAI-compatible/custom base URLs.

Ollama and vLLM are treated as local single-model providers. This is useful static evidence for provider replaceability, but it is not a runtime proof for the target NAIA model/provider combination.

~~~text
PROVIDER_ABSTRACTION = PRESENT
LOCAL_PROVIDER_PATHS = [OLLAMA, VLLM]
TARGET_PROVIDER_RUNTIME_PROOF = NOT_ESTABLISHED
~~~

## 7. Channels and external integrations

The exact source tree contains concrete WhatsApp, Slack, Outlook/calendar and browser integrations. These establish implementation surface, not equal maturity or current-pin runtime proof for every integration.

No broad channel benchmark is warranted at this stage.

## 8. Exact-pin hosted execution visibility

For 32c55d2643f9fe38777f9212588b2eee45392514, the available GitHub evidence returned:

~~~text
workflow_runs = []
combined_statuses = []
~~~

Therefore:

~~~text
CURRENT_PIN_HOSTED_EXECUTION = NOT_OBSERVED
CODE_PASS = NOT_CLAIMED
CODE_FAIL = NOT_CLAIMED
~~~

Absence of a hosted run is not treated as a code failure.

## 9. License boundary

The repository LICENSE is Business Source License 1.1 and expressly limits current licensed use to personal non-commercial use and free academic/research/educational use, while prohibiting commercial use until the Change Date unless separate permission applies.

This is a legal/adoption boundary separate from technical quality.

~~~text
LICENSE = BSL_1_1
TECHNICAL_AUDIT_ALLOWED = YES
LEGAL_ADOPTION_CLEARED = NO
COMMERCIAL_ADOPTION_WITH_CURRENT_TERMS = NOT_CLEARED
LEGAL_REVIEW_REQUIRED = YES
~~~

Atento must not infer adoption permission from technical suitability.

## 10. Current disposition

~~~text
OPEN_ASSISTANT_STATIC_CONTRACT_AUDIT = COMPLETE
OPEN_ASSISTANT_STATIC_RESULT = PASS_WITH_SCOPE
OPEN_ASSISTANT_PRODUCT_COMPARABLE = YES

STRONG_STATIC:
  - persistent conversation memory
  - persisted cron jobs and restart reload
  - execution history and locking
  - skill/service tool filtering
  - real Playwright browser automation
  - encrypted credential storage
  - multi-provider/local-provider abstraction

MATERIAL_GAPS:
  - no independent per-action approval/deny policy established
  - plans can expand to all enabled skills
  - background technical capability subset not established
  - credential store is global by service_name
  - strict NAIA/Anna memory/tool/credential isolation not established
  - browser network/URL authority needs hardening
  - desktop computer-use not established
  - durable arbitrary external-effect semantics not established
  - exact-pin runtime execution not observed

OPEN_ASSISTANT_CURRENT_PIN_QUALIFIED = NO
OPEN_ASSISTANT_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
LEGAL_ADOPTION_CLEARED = NO
~~~

## 11. Smallest next evidence

Do not run a broad Open Assistant suite.

Because the technical static audit is complete and the adoption license is unresolved, runtime work should remain evidence-only and bounded. Before any adoption-oriented qualification, resolve the legal-use boundary for the intended Atento use.

If a technical runtime probe is later authorized, the minimum useful profile is:

~~~text
persistent memory
+ restart
+ one scheduled action
+ one messaging channel
+ one browser action
+ one denied external action
+ encrypted credential path
+ one target LLM provider
~~~

Acceptance must prove that restart/background execution does not broaden tool or credential authority and must record adaptation touchpoints, tokens/calls, wall time and raw evidence.

No winner is selected by this audit.
