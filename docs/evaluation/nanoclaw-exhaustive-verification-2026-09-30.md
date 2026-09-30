# NanoClaw exhaustive verification — 2026-09-30

## Scope

Candidate: `nanocoai/nanoclaw`

Frozen evaluation pin:

```
4c1eabd3ddd74cc3d71b1871da857391a9411c8d
```

This record supersedes the earlier statement that hosted execution at this exact pin had not been observed. Exact-pin GitHub Actions execution is now available and was inspected together with the frozen workflow definitions and the run-backed isolation tests.

Rules preserved:

- `UPSTREAM_SIGNAL != ATENTO_LOCAL_PROOF`
- `IMPLEMENTED != QUALIFIED`
- `VERIFIED != ACCEPTED`
- `ACCEPTED != PROMOTED`
- passing trunk/registry tests do not prove a composed NAIA/Anna profile
- registry-branch payloads are evidence only for the exact refs exercised by the workflow

No NanoClaw source was modified.

## Exact-pin core CI

Workflow:

- `CI`
- run: `36624644303`
- event: `push`
- exact head: `4c1eabd3ddd74cc3d71b1871da857391a9411c8d`
- conclusion: `success`

The frozen workflow requires both Node 22 and Node 24 matrix jobs to perform:

1. frozen dependency install;
2. host format check;
3. host TypeScript typecheck;
4. container-runner TypeScript typecheck;
5. host Vitest suite;
6. container Bun test suite.

Both observed matrix jobs finished with:

```
3 tests skipped
513 pass
0 fail
Ran 516 tests across 58 files
```

The workflow also runs `iron-front`, which fetches the exactly pinned Iron source revision declared by the skill, copies NanoClaw's front proxy into that tree, executes:

```
go test -mod=readonly -race -count=1 ./...
```

checks `gofmt`, and requires the source checkout to remain clean. That job passed.

The `ci` and `gate` aggregation jobs then required every matrix/iron dependency to be `success`; both passed.

Classification:

```ini
EXACT_PIN_CORE_CI = PASS
NODE_22 = PASS
NODE_24 = PASS
HOST_CONTAINER_TEST_SUMMARY = 513_PASS_0_FAIL_PER_MATRIX
IRON_FRONT_RACE_GATE = PASS
CORE_GATE = PASS
```

## Run-backed control-plane isolation

The exact-pin host suite includes `src/cli/dispatch.test.ts`, therefore its assertions are run-backed by both Node matrices.

Observed negative assertions include:

- `cli_scope=disabled` rejects all agent CLI requests;
- a `group`-scoped agent is auto-bound to its own agent-group identifier;
- explicit access to another group is rejected;
- explicit `agent_group_id` targeting another group is rejected;
- `cli_scope` / `cli-scope` escalation to `global` is rejected;
- non-group resources are rejected under group scope;
- `sessions get` has an ownership check rather than relying only on caller-supplied IDs;
- operator-only commands remain denied to an agent caller even when its normal scope is `global`.

Classification:

```ini
GROUP_CONTROL_PLANE_SCOPE = PASS_WITH_SCOPE
CROSS_GROUP_CLI_ACCESS = DENIED_IN_RUN_BACKED_TESTS
CLI_SCOPE_ESCALATION = DENIED_IN_RUN_BACKED_TESTS
HOST_ONLY_COMMAND_FROM_AGENT = DENIED_IN_RUN_BACKED_TESTS
```

The scope is important: these tests prove the control-plane guard behavior for the exercised command paths. They do not by themselves prove that every future module or third-party skill preserves the same boundary.

## Run-backed filesystem/container admission

The exact-pin suite includes `src/drivers/conformance.test.ts`.

Observed assertions include:

- a group-state mount that lexically escapes into another group's folder is denied;
- directly presenting another group's folder as the current group's state is denied;
- the current group's own folder is accepted;
- relative/named-volume-shaped host paths are denied where a bind path is required;
- undeclared runtime isolation tiers are rejected before runtime creation;
- a driver must validate the requested tier against its declared capabilities.

Classification:

```ini
CROSS_GROUP_STATE_MOUNT = DENIED_IN_RUN_BACKED_TESTS
PATH_ESCAPE_TO_OTHER_GROUP = DENIED_IN_RUN_BACKED_TESTS
RUNTIME_TIER_ADMISSION = PASS_WITH_SCOPE
```

This is directly relevant to NAIA/Anna separation because their group state can be represented as distinct group roots. It still does not prove the complete Atento composition, including every additional mount a selected recipe would install.

## Credential and MCP boundary evidence

The exact-pin suites exercise both host and container-side URL/configuration guards.

Examples observed in run-backed tests:

- `add_mcp_server` rejects insecure or credential-bearing URLs before requesting approval;
- HTTP is limited to explicit loopback/container-host exceptions rather than suffix-like hostnames;
- userinfo credentials, credential-like query keys, fragments, malformed env keys and configuration-injection-shaped env keys are rejected;
- credential material passed by reference may be represented as a mounted file path while the admission invariant forbids treating arbitrary host identity material as trusted;
- auxiliary-container material does not automatically widen the agent container's mount surface.

The architectural gateway claim remains scoped. NanoClaw core defines the credential-gateway seam; an actual gateway provider is skill-installed. Therefore:

```ini
MCP_CREDENTIAL_CONFIG_GUARDS = PASS_WITH_SCOPE
CONTAINER_ADMISSION_CREDENTIAL_BOUNDARY = PASS_WITH_SCOPE
REAL_GATEWAY_CREDENTIAL_NON_DISCLOSURE = NOT_PROVEN_BY_CORE_CI_ALONE
```

## Registry-skill composition gate

Workflow:

- `Registry skills`
- run: `36624644411`
- exact core head: `4c1eabd3ddd74cc3d71b1871da857391a9411c8d`
- conclusion: `success`

The frozen workflow resolves and freezes the core, `channels`, and `providers` refs, then executes a non-fail-fast matrix that applies/tests available registry skills. Observed passing jobs include:

- DeltaChat
- Codex
- Discord
- OpenCode
- Emacs
- Dial
- GitHub
- Linear
- Resend
- Google Chat
- Mattermost
- Signal
- Matrix
- iMessage
- Slack
- Teams
- Telegram
- Webex
- WhatsApp Cloud
- WeChat
- WhatsApp

Additional mandatory jobs passed:

- `combined-providers`
- `pre-contract-providers`
- `old-provider-refresh`
- `provider-promotion`
- `registry gate`

Thus the gate covers not only isolated application but also combined-provider composition, applying pre-contract provider payloads to the current core, and refreshing legacy provider payloads.

A representative OpenCode job performed host build, container typecheck, host provider tests, container provider tests and provider-contract verification. Its observed host-focused provider suite reported 170/170 tests passing, and container provider tests exercised auth-state safety, runtime recovery, continuation handling, configuration and memory-hook behavior.

Codex likewise built the agent image and completed the provider contract verifier with status `passed`.

Classification:

```ini
REGISTRY_SKILLS_GATE = PASS
CHANNEL_SKILL_MATRIX = PASS
PROVIDER_SKILL_MATRIX = PASS
COMBINED_PROVIDER_GATE = PASS
OLD_PROVIDER_REFRESH_GATE = PASS
PROVIDER_CONTRACT_VERIFICATION = PASS_FOR_OBSERVED_PROVIDER_JOBS
```

This materially strengthens the earlier adaptation audit. A large change surface such as OpenCode remains a maintenance-cost fact, but it is no longer merely a static recipe: the current exact-pin registry workflow exercised its application and tests successfully.

## What remains outside the registry proof

The registry matrix is not equivalent to the final Atento installation.

In particular:

- the exact NAIA recipe has not been frozen;
- a credential gateway such as OneCLI is a separate gateway skill/seam and is not equivalent to the channel/provider registry matrix;
- actual secrets have not been injected into an Atento-owned container and then probed for non-disclosure;
- NAIA and Anna have not been instantiated simultaneously and attacked across memory, mounts, CLI, tools, credentials, channels and scheduled execution;
- the selected browser/computer-use profile has not been frozen;
- Engram → adapter/browser integration has not been composed;
- handoff has not been constrained to an explicit broker and adversarially tested;
- the published Ollama skill's prior architecture-skew finding remains a separate issue until rederived against the current provider contribution seam.

## Relation to prior change-surface audit

The 2026-09-29 change-surface findings remain applicable to adaptation cost, but this line is superseded:

```
CURRENT_PIN_RUNTIME_EXECUTION = NOT_OBSERVED
```

New evidence:

```ini
CURRENT_PIN_CORE_CI = PASS
CURRENT_PIN_REGISTRY_SKILL_EXECUTION = PASS
```

No conclusion about total migration cost follows automatically:

```
TESTED_SKILL != LOW_CHANGE_SURFACE
SMALL_CORE != LOW_TOTAL_MIGRATION_COST
```

## Gate

Smallest defensible classification:

```ini
CANDIDATE = NANOCLAW
PIN = 4c1eabd3ddd74cc3d71b1871da857391a9411c8d

UPSTREAM_CORE_CI = PASS
UPSTREAM_REGISTRY_COMPOSITION_GATE = PASS
GROUP_CONTROL_PLANE_ISOLATION = PASS_WITH_SCOPE
GROUP_STATE_MOUNT_ISOLATION = PASS_WITH_SCOPE
CREDENTIAL_CONFIG_GUARDS = PASS_WITH_SCOPE

ATENTO_PROFILE = NOT_FROZEN
REAL_GATEWAY_NON_DISCLOSURE = NOT_RUN
ATENTO_CROSS_ROLE_COMPOSITION = NOT_RUN
ATENTO_ISOLATION = NOT_ESTABLISHED
NAIA_BASE = NOT_SELECTED
PROMOTION = NO
```

Unlike a candidate whose frozen pin fails its own health gate, NanoClaw remains empirically eligible for the next-stage Atento composition probe. That statement is not a preference or selection.

## Smallest next empirical probe

For NanoClaw specifically, freeze one representative Atento recipe:

```
NAIA group
+ one messaging channel
+ one selected gateway
+ one provider
+ persistent memory
+ one scheduled task
```

Then instantiate a second Anna group and adversarially test:

1. cross-group CLI reads/writes;
2. direct and traversal-based mount attempts;
3. memory/workspace reads across groups;
4. credential discovery in env, files, process args and model-visible context;
5. channel/wiring substitution;
6. scheduled-task authority versus foreground authority;
7. attempted `cli_scope` escalation;
8. cross-agent/handoff paths without the broker;
9. restart persistence and session adoption;
10. apply/reapply/update refresh while preserving the same isolation assertions.

Until that composed run exists, the pass statuses above remain mechanism-level evidence only.

## Evidence references

- core CI: https://github.com/nanocoai/nanoclaw/actions/runs/36624644303
- registry skills: https://github.com/nanocoai/nanoclaw/actions/runs/36624644411
- frozen pin: https://github.com/nanocoai/nanoclaw/commit/4c1eabd3ddd74cc3d71b1871da857391a9411c8d

## Final disposition for comparison table

```ini
NANOCLAW_FROZEN_PIN_STATUS = PASS_UPSTREAM_WITH_ATENTO_COMPOSITION_PENDING
DIRECT_ISOLATION_MECHANISM_EVIDENCE = POSITIVE_NARROW
REGISTRY_ADAPTATION_EVIDENCE = STRONG
REQUALIFICATION_BEFORE_SELECTION = REQUIRED_AT_COMPOSED_PROFILE
```
