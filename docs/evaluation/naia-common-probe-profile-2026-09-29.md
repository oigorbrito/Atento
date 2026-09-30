# NAIA common empirical probe profile v1 — 2026-09-29

## Purpose

Freeze the smallest comparable empirical profile for the later local-delta phase. The candidate universe has since expanded; this profile is retained but local execution is gated by discovery and upstream-evidence reconciliation.

This is not a benchmark leaderboard and does not create a shortlist or winner.

~~~text
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
CROSS_AGENT_TOPOLOGY = NOT_SELECTED
~~~

Existing sufficient evidence must be reused. Only missing material deltas are executed.

Current phase gate:

~~~text
CANDIDATE_UNIVERSE_COMPLETE = false
EXTERNAL_EVIDENCE_PREFLIGHT_REQUIRED = YES
LOCAL_COMMON_PROBE_PHASE = NOT_STARTED
~~~

Before any NCP execution, consult:

- `docs/evaluation/naia-persistent-agent-discovery-2026-09-29.md`
- `docs/evaluation/naia-external-evidence-preflight-2026-09-29.md`

A candidate must have its exact pin, upstream implementation contract, relevant upstream tests/evals, available CI/run evidence and one-sentence Atento delta recorded first.

## 1. Frozen capability profile

Every candidate is mapped against the same target capability profile:

~~~text
persistent memory
+ restart continuity
+ scheduled/background work
+ one messaging channel
+ browser/web action
+ external-effect authority
+ credential handling
+ provider replaceability
+ strict NAIA/Anna isolation boundary
+ adaptation touchpoint count
+ runtime cost / token cost / wall time
~~~

Desktop computer-use is not a universal first-pass requirement. It is an additional deployment probe only when the target NAIA deployment requires native desktop control.

## 2. Common empirical probes

The minimum cross-candidate set is four probes. A candidate skips a probe or sub-check only when existing evidence already proves the same contract at the relevant pin/boundary.

### NCP-01 — state + restart continuity

Create a small deterministic state bundle:

- one memory item;
- one scheduled job;
- one execution/audit marker.

Restart the candidate runtime and verify:

- the memory remains readable only by the expected authority;
- the scheduled job remains registered;
- stale/in-flight work is not silently duplicated;
- restart does not broaden authority.

Acceptance:

~~~text
MEMORY_SURVIVES_RESTART = YES
SCHEDULE_SURVIVES_RESTART = YES
DUPLICATE_EXTERNAL_EFFECT = NO_OBSERVED_DUPLICATE
AUTHORITY_AFTER_RESTART <= AUTHORITY_BEFORE_RESTART
~~~

Do not rerun this where equivalent current evidence is already sufficient.

### NCP-02 — authority consistency

Use one low-risk external effect and one intentionally disallowed effect.

Exercise both interactive and scheduled/background paths and verify:

- disallowed action fails closed;
- allowed action executes only with the expected capability/approval;
- background execution does not receive a broader tool/credential set;
- planning/delegation cannot silently expand authority;
- raw credentials do not appear in agent-visible context/logs/artifacts.

Acceptance:

~~~text
DENIED_ACTION = DENIED_TECHNICALLY
ALLOWED_ACTION = BOUND_TO_EXPECTED_AUTHORITY
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
CREDENTIAL_LEAK = NOT_OBSERVED
PROMPT_ONLY_POLICY = INSUFFICIENT
~~~

### NCP-03 — NAIA/Anna isolation composition

Instantiate the smallest supported topology that claims to preserve the fixed product boundary.

Verify independently:

- memory store separation;
- credential separation;
- tool authority separation;
- channel/session separation;
- no silent cross-agent read or tool invocation;
- any handoff requires an explicit brokered path.

If the candidate cannot provide this within one runtime safely, a two-runtime/two-store topology is valid and its deployment/change cost is measured rather than treated as a failure by default.

Acceptance:

~~~text
NAIA_CAN_READ_ANNA_MEMORY = NO
ANNA_CAN_READ_NAIA_MEMORY = NO
NAIA_CAN_USE_ANNA_CREDENTIALS = NO
ANNA_CAN_USE_NAIA_CREDENTIALS = NO
SILENT_ROLE_DRIFT = NO
EXPLICIT_HANDOFF_ONLY = YES
~~~

### NCP-04 — frozen adaptation + cost envelope

Starting from the exact upstream pin, compose only the frozen NAIA profile and preserve the pre/post diff.

Measure:

- files added/copied;
- existing files modified;
- dependency changes;
- configuration-only vs core patch;
- update/apply idempotency where the candidate has an extension mechanism;
- one messaging path;
- one browser/web path;
- one target provider path;
- wall time;
- LLM calls;
- input/output tokens when observable;
- external monetary cost when observable.

Acceptance is descriptive, not a score:

~~~text
PROFILE_EXECUTABLE = YES|NO
CORE_PATCH_REQUIRED = YES|NO
TOUCHPOINTS = OBSERVED_COUNT
DEPENDENCY_DELTA = OBSERVED
WALL_TIME = OBSERVED
LLM_CALLS = OBSERVED
TOKENS = OBSERVED_OR_NOT_AVAILABLE
MONETARY_COST = OBSERVED_OR_NOT_AVAILABLE
~~~

SMALL_CORE does not imply low total migration cost.

## 3. Evidence-reuse map

### OpenMausBot

Do not redo the redundant branch work. Existing evidence is canonical on main.

Execute only a missing NCP sub-check if the frozen profile exposes a contract not already covered by canonical evidence.

### OpenClaw

Reuse restart/interrupted-turn, stale-authority lifecycle and durable channel-outbound evidence.

Primary missing work:

~~~text
NCP-02 = hardened effective policy
NCP-03 = strict NAIA/Anna deployment boundary
NCP-04 = adaptation touchpoints/cost
~~~

Do not rerun unchanged historical restart/channel tests.

### QwenPaw

Primary missing work:

~~~text
NCP-01 = restart + scheduled-state proof at hardened profile
NCP-02 = sandbox-unavailable deny + cron authority + approvals
NCP-03 = strict NAIA/Anna boundary
NCP-04 = hardened-profile touchpoints/cost
~~~

Managed browser and signed-in-user browser are separate authority profiles.

### AI Butler

Reuse static fail-closed shell, credential broker and scheduler contracts.

Primary missing work:

~~~text
NCP-01 = runtime restart continuity
NCP-02 = one capability-scoped scheduled + credential-gated action
NCP-03 = profile/bank boundary as NAIA/Anna composition
NCP-04 = ready-surface adaptation/cost
~~~

Windows Tier 3/4 computer-use is an optional target-deployment delta, not a universal first probe.

### NanoClaw

Freeze one exact recipe before execution.

Primary missing work:

~~~text
NCP-01 = composed memory/schedule restart
NCP-02 = credential-gateway/background authority
NCP-03 = group/runtime isolation for NAIA/Anna
NCP-04 = skill composition + update/idempotency + total touchpoints
~~~

Do not apply the pinned Ollama skill blindly; rederive it against the current provider-contribution seam first if Ollama is selected for the profile.

### TrustClaw

Primary missing work:

~~~text
NCP-01 = local memory/cron restart
NCP-02 = Composio authority + background subset + unavailability behavior
NCP-03 = instance/user separation mapped to NAIA/Anna
NCP-04 = dependency/call/cost envelope
~~~

Keep local chassis results separate from Composio/Vercel dependency results.

### Open Assistant

Static contract audit is complete.

License/adoption metadata remains separate, but per the current technical-discovery instruction it is not used to exclude or defer technical evidence collection.

If a runtime probe is eventually justified by an unproven material Atento delta, map it to NCP-01..04 rather than inventing a separate suite.

## 4. Execution order

No candidate ranking is implied.

Run work in the order that minimizes repetition:

~~~text
0. expand the candidate universe and keep CANDIDATE_UNIVERSE_COMPLETE=false until same-protocol admission is sufficient
1. freeze exact candidate pin/profile
2. locate upstream implementation contracts, tests/evals and available run/CI artifacts
3. classify evidence as UPSTREAM_PROVEN / TRANSFERABLE_WITH_CONSTRAINTS / ATENTO_DELTA / UNPROVEN
4. state the remaining Atento delta in one sentence
5. execute NCP-02 only if authority remains materially unproven
6. execute NCP-01 only where restart/state evidence remains materially unproven
7. execute NCP-03 only where isolation composition remains materially unproven
8. collect NCP-04 from real adaptation work rather than a hypothetical patch
9. compare raw evidence only after decision-relevant gaps are closed
~~~

## 5. Decision rule

A future decision may compare observed evidence, but this document does not rank candidates.

~~~text
BENCHMARK_SIGNAL != LOCAL_PROOF
STATIC_SOURCE != RUNTIME_PASS
IMPLEMENTED != QUALIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED
~~~

The next work item is not a local NCP. It is candidate-universe expansion plus upstream/external evidence reconciliation. NCP execution begins only after a material local delta remains.
