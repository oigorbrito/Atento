# Gate 2 continuation — authority and isolation — 2026-10-01

## Decision question

The user directed the comparison to continue until one chassis/composition remains. This gate advances candidates using existing exact-pin evidence only. It does not rerun benchmarks or create an aggregate score.

Selection requirements are the Atento product contract: separate chat/session identity, memory, tools, credentials, persistent state, and role-preserving background work for NAIA, Anna, and Apollo; cross-role work uses an explicit minimal auditable handoff and recipient-side authorization.

## Current gate outcome

```text
UNIQUE_FINAL_CHASSIS = NOT_ESTABLISHED
SINGLE_CANDIDATE_ADVANCED_TO_NEXT_RESIDUAL_PROBE = NanoClaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d
OTHER_CANDIDATES = UNRESOLVED_OR_PIN_BLOCKED; NOT_ALL_ELIMINATED
ATENTO_SYSTEM_ASSERTION_EXECUTION = PARTIAL_PASS_WITH_SCOPE
NEW_BENCHMARKS = NONE
SYNTHETIC_SCORE = NONE
```

NanoClaw is the only Top-10 pin whose current record combines exact-pin upstream CI with run-backed isolation mechanisms and is explicitly eligible for a next-stage Atento composition probe. That makes it the **only immediate advance**, not the winning chassis. Its credential gateway non-disclosure and the full three-role composition remain unproven.

## Candidate dispositions at this gate

| Candidate | Existing evidence relevant to authority/isolation | Gate 2 disposition |
|---|---|---|
| NanoClaw | Exact-pin core/registry CI passes; group control-plane and state-mount isolation plus credential configuration guards are PASS_WITH_SCOPE. Real gateway credential non-disclosure and Atento cross-role composition are NOT_RUN. | **ADVANCE_TO_ONE_RESIDUAL_COMPOSITION_PROBE** |
| AI Butler | Atento Gate-2 workflow now has successful exact-pin runs 36801774567 (push) and 36801793397 (pull request), both checking candidate pin `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`; uploaded artifact records ISO-1..ISO-6 as PASS_WITH_SCOPE. Review of the injected test shows module-level memory-bank, vault and capability checks plus the real Atento broker adapter, not the full three-role app, scheduler or restart composition. Existing upstream bank/scheduler evidence remains scoped. The same frozen pin's latest scheduled security workflow, run 36426287353, still fails with seven reachable advisories. | **BLOCK_CURRENT_PIN_ON_SECURITY**; a repaired, refrozen pin would require requalification. The new run strengthens scoped NAIA/Anna evidence but does not establish the product-wide chassis. |
| OpenClaw | Strong per-agent core-state and policy mechanisms. Cross-agent session isolation is not default; strict therapy boundary requires separate runtime/Gateway. | **HOLD_AS_SEPARATE-RUNTIME COMPOSITION**; one shared Gateway is insufficient. |
| QwenPaw | Strong static per-agent memory/policy seams; sandbox-unavailable fallback can broaden to unsandboxed ALLOW and cron controls need hardening. Exact-pin hosted test state includes a failed nightly and no completed passing main Tests result. | **HOLD_FOR_FAIL-CLOSED PROFILE**; current posture does not pass the required default authority. |
| MindRoom | Agent scopes and persistent roots are configurable, but the pinned plan explicitly records incomplete agent-isolated filesystem visibility in shared-runner/local paths; a narrower dedicated-worker seam exists. | **HOLD_FOR_BACKEND-SPECIFIC ISOLATION PROOF**. |
| Bob Labs | Test definitions cover lab scoping, explicit memory-sharing confirmation, sandbox HMAC and secret encryption, but no hosted Actions run was found for this exact pin. | **UNRESOLVED**; source test definitions are not run evidence. |
| Ontheia | Exact-pin host and WebUI CI pass; namespace tests and session RLS policies exist. The inspected evidence does not prove Atento agent/domain isolation. | **UNRESOLVED**; role mapping and negative cross-role assertions absent. |
| OpenAkita | Exact-pin build passed; Python/unit/integration/smoke/E2E jobs were skipped. The inspected state/blackboard tests do not prove private role separation. | **UNRESOLVED**. |
| Clawix | Exact-pin lint/typecheck/test CI passed. The inspected multi-user repository tests use mocks and do not demonstrate end-to-end role authorization or isolation. | **UNRESOLVED**. |
| Memoh | Exact commit not frozen. | **PIN_REQUIRED**; not eligible for this gate yet. |

“Hold” and “unresolved” do not mean candidate failure. The only pin explicitly blocked by a current upstream hard-gate failure here is AI Butler. The others remain in the cohort unless a structural contradiction is demonstrated.

## Why the comparison is not yet down to a final winner

The latest AI Butler Atento workflow does not change this: its injected exact-pin tests exercise candidate memory-bank, vault and capability modules and call the Atento broker adapter; they do not run the full product topology or Apollo. The artifact is retained as `PASS_WITH_SCOPE`, while the separate security failure remains a hard block for that pin. The current evidence has different scopes: some results test user/tenant separation, some test agent-local memory/state, and some test a bounded runtime mechanism. None records all Atento role boundaries together. OrchBench provides external signal about orchestration-plan quality and information transfer, but it is a simulation benchmark and does not test identity authorization, credential secrecy, or role isolation. BenchLM provides model/agent capability results (including tool-use benchmarks), but those model-level scores also do not test chassis fit, Atento role boundaries, or three-role composition.

Therefore, declaring a final winner now would turn missing system evidence into an unsupported pass. The defensible narrowing is one candidate for the **next probe** plus a parked unresolved cohort, not a final selection.

## Next decisive probe — NanoClaw only

The machine-readable **system-level three-role** profile is now frozen at `evals/config/system_chassis_nanoclaw_v1.json` (topology SHA-256 `c6e815289488daace646e7d9123b2638c6f245eaf4ef4dff357d6b3c50c1d289`; policy SHA-256 `02de0f5540c1c638c0553dc8261cfd0e53ffb4727a0636a50a4653d2e15a7132`). The earlier `NAIA-GATE2-NANOCLAW-COMPOSITION-V1` profile (`evals/config/naia_gate2_nanoclaw_v1.json`) covers only NAIA and Anna; it cannot establish Apollo or complete-system qualification. The new profile reuses the exact NanoClaw/channel/provider/gateway pins, adds an independent Apollo group/state/identity, requires role-unique synthetic grants and inert effects, and prohibits live provider calls, real channel accounts, and production credentials. Reuse applicable two-role evidence, then run the three-role system assertions against the remaining transfer boundary:

1. Bind three independent identities to NAIA, Anna, and Apollo runtime/state roots.
2. Exercise SYS-CHAT-01 and SYS-MEM-01 negative cases, including restart and retrieval/traces.
3. Exercise SYS-TOOL-01 and SYS-CRED-01 across roles; verify no credential or tool authority crosses by ambient environment, files, process args, logs, or model-visible context.
4. Route an explicit typed handoff through the proposed Atento broker; deny untyped, overbroad, and wrong-recipient transfers; reauthorize the action at the receiving role.
5. Exercise SYS-BG-01 for scheduled/retry/recovery work and verify grants remain equal or narrower.
6. Record the same run's changes, dependencies, runtime/store boundaries, deployment services, and active engineering effort separately; do not turn these into an overall score.

Acceptance requires every non-negotiable assertion to pass. Any blocker must be classified as localized repair, replaceable component, or cross-cutting chassis rewrite. If NanoClaw fails structurally or exceeds the declared replacement threshold, resume with the unresolved cohort in existing priority order; do not treat a missing result as failure.

## Execution state — hosted runtime probe — 2026-10-01

The exact NanoClaw pin ran on the GitHub-hosted Docker runner at nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d. The test reads `evals/config/system_chassis_nanoclaw_v1.json` directly and asserts the frozen upstream SHA, topology hash `c6e815289488daace646e7d9123b2638c6f245eaf4ef4dff357d6b3c50c1d289`, policy hash `02de0f5540c1c638c0553dc8261cfd0e53ffb4727a0636a50a4653d2e15a7132`, and the three exact agent-group IDs. Channel instances, providers, and synthetic effects are derived from that profile for the DB and runtime fixtures. The profile IDs are `atento-naia` / `telegram-naia-test` / `codex`, `atento-anna` / `telegram-anna-test` / `codex`, and `atento-apollo` / `telegram-apollo-test` / `codex`; each role uses its own configured canary effect.

Run [36815873223](https://github.com/oigorbrito/Atento/actions/runs/36815873223) completed successfully at Atento harness commit `a5dca9401fa6f24022b6b7f8daed50505516a309`. Its JUnit artifact records 7 tests, 7 passed, 0 failed. It exercised (a) each profile-bound group state fixture through NanoClaw's real DockerSessionDriver, (b) state surviving a driver-managed stop/prepare cycle, (c) migrated SQLite group/session ownership, profile provider binding, scoped lookup, and negative cross-group lookup, (d) native direct NAIA/Anna/Apollo A2A sends denied without a destination grant, (e) role-unique synthetic identity mounted only into each auxiliary container, (f) profile-bound scheduled-task ownership and foreign-group CLI denials, and (g) a test-harness Atento broker adapter using the real Python reference broker and NanoClaw mailbox APIs. For (g), both Anna→NAIA and Apollo→NAIA typed requests were validated against the frozen role map, delivered through NanoClaw's `writeSessionMessage` into NAIA's real isolated mailbox, and checked for sender-session correlation; untyped bodies, wrong recipients, and authority-bearing fields were rejected. Native direct A2A from each specialist remained denied. The attempted follow-up task was denied when invoked under the sender identity and accepted only when dispatched under NAIA's group identity.

This proves a bounded host-side composition seam using the reference broker and NanoClaw's existing mailbox/CLI code. The broker adapter and typed-body/profile checks live in the injected Atento test harness, not in a deployed Atento runtime; the receiver action was dispatched under NAIA's identity without starting an LLM/provider. It does not prove production service wiring, a real model decision, a real channel adapter, provider/gateway custody, host-process restart, or task firing/retry/recovery in the three-role profile.

This is a bounded system-profile-derived runtime probe, not full application composition. The hosted job used the digest-pinned utility image `node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1`, inert local fixtures, no live provider calls, no real channel accounts, and no production credentials. Early exact-profile attempts failed because a few expected strings still used generic role aliases instead of profile canary values; the harness was corrected and the final run above passed. Those mismatches were test assertion defects, not candidate failures.

SYS-MEM-01 = PASS_WITH_SCOPE (driver-realized isolated group-state mounts for the exact profile groups)
SYS-CHAT-01 = PASS_WITH_SCOPE (migrated DB ownership, profile provider binding, scoped lookup, and negative cross-group lookup; no real channel/router)
SYS-TOOL-01 = PASS_WITH_SCOPE (direct A2A denied without a cross-role destination grant; remaining tool authority not tested)
SYS-CRED-01 = PASS_WITH_SCOPE (role-unique synthetic material isolated in a read-only per-session auxiliary container; provider/gateway custody not tested)
SYS-HANDOFF-01 = PASS_WITH_SCOPE (Anna/Apollo typed requests passed through reference broker to NAIA's candidate mailbox; action dispatch accepted only under NAIA identity; no real provider decision or product wiring)
SYS-HANDOFF-02 = PASS_WITH_SCOPE (untyped body, wrong recipient, authority field, and unbrokered native A2A denied in the test composition; sensitive-consent positive path not tested)
SYS-BG-01 = PASS_WITH_SCOPE (profile-bound task creation/session and cross-group CLI denial; exact-pin upstream task/recurrence/sweep suites pass; three-role task fire/retry/recovery not exercised)
SYS-STATE-01 = PASS_WITH_SCOPE (state survives driver-managed stop/prepare; host restart not simulated)
SYSTEM_PROFILE_GATE = NOT_PASSED (required assertions remain open)
SYSTEM_COMPOSITION_EXECUTION = PARTIAL_PASS_WITH_SCOPE

The local scratch executor still has no Docker/Podman and no local checkout of the private Atento repo. Hosted Actions supplies the exact-pin runtime and checked-out Atento harness for this bounded probe. Apollo was exercised only as a profile-bound role-isolation fixture; this does not start Apollo product research or select an Apollo base.

NANOCLAW_EXACT_PIN_ACQUIRED = YES
DIRECT_GITHUB_ACCESS = AVAILABLE
HOSTED_DOCKER_RUNNER = AVAILABLE
SYSTEM_NANOCLAW_THREE_ROLE_PROFILE = FROZEN_V1
SYSTEM_PROFILE_PIN_AND_HASH_PREFLIGHT = PASS
SYSTEM_RUNTIME_AND_SESSION_PROBE = PASS_WITH_SCOPE (final run 36815873223; 7 tests, 7 passed, 0 failed; includes broker/mailbox handoff and profile-bound scheduled-task authority)
SYSTEM_PROFILE_GATE = NOT_PASSED
NEW_BENCHMARKS = NONE
UNIQUE_FINAL_CHASSIS = NOT_ESTABLISHED

The independent NAIA candidate Gate-2 queue remains governed by its own frozen order (AI Butler first); this product-wide system-chassis probe is a separate decision path.

## Residual handoff architecture audit — exact NanoClaw pin

Source inspection of the frozen NanoClaw pin identifies its native route at [`src/delivery.ts`](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/delivery.ts) and [`src/modules/agent-to-agent/agent-route.ts`](https://github.com/nanocoai/nanoclaw/blob/4c1eabd3ddd74cc3d71b1871da857391a9411c8d/src/modules/agent-to-agent/agent-route.ts). When an outbound message has `channelType === 'agent'`, the host dispatches directly to `routeAgentMessage`; that route uses the candidate's `agent_destinations` authorization and delivers into a target agent session. The system profile has no native cross-role destination grant, so the tested direct path is denied. Granting such a destination would enable the candidate-native route and would not, by itself, establish the Atento broker contract or receiver-side action reauthorization.

The reference broker in `evals/atentoeval/handoff_broker.py` validates a bounded envelope and rejects authority-bearing fields, but it is candidate-agnostic and does not deliver into NanoClaw or authorize the receiving role's action. Its unit contract is not evidence of an integrated NanoClaw handoff. The candidate has a visible host delivery branch and a separate A2A module, which suggests a possible integration seam; the amount of Atento-specific change and its locality have not been measured in an implemented composition.

```text
NATIVE_DIRECT_A2A_WITHOUT_DESTINATION = PASS_WITH_SCOPE (denied)
BROKER_ENVELOPE_TO_NANOCLAW_RECEIVER = NOT_RUN
RECEIVER_ACTION_REAUTHORIZATION = NOT_RUN
BROKER_BYPASS_RESISTANCE = NOT_RUN
HANDOFF_REPAIR_CLASS = UNRESOLVED (implementation and change locality not measured)
```

The next decisive probe must connect the real Atento broker envelope to a NanoClaw receiver session, demonstrate recipient-side authorization before any action, and show the agent cannot bypass that path through native A2A. It must also capture the Atento-specific patch and classify its change locality. A standalone envelope round-trip or broker unit test cannot close these assertions. No candidate is eliminated based on this source inspection.

## Reused exact-pin scheduler and recovery evidence

NanoClaw's existing upstream CI run [36624644303](https://github.com/nanocoai/nanoclaw/actions/runs/36624644303) is for the exact frozen commit `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` and completed successfully. Its full unit job recorded 513 passed, 3 skipped, and 0 failed across 58 files. The same run explicitly passed `src/cli/resources/tasks.test.ts` (31 tests), `src/host-sweep.test.ts` (21 tests), `src/mailbox/sqlite/tasks.test.ts` (13 tests), and `src/modules/scheduling/recurrence.test.ts` (9 tests). Reuse these as exact-pin task CRUD, recurrence/backoff, and host-sweep/recovery evidence; they do not establish three-role Atento task execution, recipient/provider behavior, or recovery across a full Atento process restart.

## Evidence

- [Top 10 first-sieve queue](system-chassis-top10-first-sieve-2026-09-30.md)
- [System architecture/chassis contract and assertions](atento-system-architecture-chassis-rescreen-2026-09-30.md)
- [NanoClaw exact-pin verification](nanoclaw-exhaustive-verification-2026-09-30.md)
- [NanoClaw exact-pin upstream CI, 513 passed / 3 skipped / 0 failed](https://github.com/nanocoai/nanoclaw/actions/runs/36624644303)
- [AI Butler exact-pin verification](aibutler-exhaustive-verification-2026-09-30.md)
- [Integrated candidates exact-pin source and CI verification](integrated-chassis-source-verification-2026-10-01.md)
- AI Butler scoped exact-pin Gate-2 workflow runs: [push 36801774567](https://github.com/oigorbrito/Atento/actions/runs/36801774567), [pull request 36801793397 with result artifact](https://github.com/oigorbrito/Atento/actions/runs/36801793397); [injected test source at d15e07a](https://github.com/oigorbrito/Atento/blob/d15e07a984cadd319a2810c388ebb8df7d063696/tools/naia_gate2/aibutler/atento_gate2_test.go). Candidate pin remains `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c`; its [scheduled security run 36426287353](https://github.com/LumabyteCo/aibutler/actions/runs/36426287353) still fails.
- [NanoClaw three-role probe source](../../tools/system_chassis/nanoclaw.atento.test.ts)
- [NanoClaw three-role profile-derived hosted run 36815873223 and 7/7 artifact](https://github.com/oigorbrito/Atento/actions/runs/36815873223)
- [External benchmark cross-check: OrchBench and BenchLM](system-chassis-benchmark-crosscheck-2026-09-30.md)
