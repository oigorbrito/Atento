# Gate 2 continuation — authority and isolation — 2026-10-01

## Decision question

The user directed the comparison to continue until one chassis/composition remains. This gate advances candidates using existing exact-pin evidence only. It does not rerun benchmarks or create an aggregate score.

Selection requirements are the Atento product contract: separate chat/session identity, memory, tools, credentials, persistent state, and role-preserving background work for NAIA, Anna, and Apollo; cross-role work uses an explicit minimal auditable handoff and recipient-side authorization.

## Current gate outcome

```text
UNIQUE_FINAL_CHASSIS = NOT_ESTABLISHED
SINGLE_CANDIDATE_ADVANCED_TO_NEXT_RESIDUAL_PROBE = NanoClaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d
OTHER_CANDIDATES = UNRESOLVED_OR_PIN_BLOCKED; NOT_ALL_ELIMINATED
ATENTO_SYSTEM_ASSERTION_EXECUTION = NOT_RUN
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

## Execution state — rechecked 2026-10-01

The exact public NanoClaw pin was acquired into the scratch workspace and verified at:
`nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`.
A fresh `git ls-remote` now succeeds, so the earlier DNS-only block is no longer the current blocker. The private Atento repository is still not checked out locally. This executor has Node 24 but neither Docker nor Podman; NanoClaw's tested isolation boundary depends on its container runtime. No candidate runtime or Atento assertion was executed. The frozen profile passed a local integrity preflight: profile version and exact pin, checked-out NanoClaw HEAD, canonical topology/policy hashes, three distinct role/group/channel IDs, required assertion list, and no-live-call/no-production-secret constraints all matched.

The existing frozen NAIA recipe is explicitly two-role (NAIA + Anna); it is not the required product-wide NAIA + Anna + Apollo profile. The current system-level run now needs only an executable container runtime and a local Atento checkout or equivalent reproducible harness material before launch.

```text
NANOCLAW_EXACT_PIN_ACQUIRED = YES
DIRECT_GITHUB_ACCESS = AVAILABLE
LOCAL_ATENTO_CHECKOUT = ABSENT
CONTAINER_RUNTIME = UNAVAILABLE (docker, podman)
NAIA_NANOCLAW_PROFILE = FROZEN_TWO_ROLE
SYSTEM_NANOCLAW_THREE_ROLE_PROFILE = FROZEN_V1
SYSTEM_PROFILE_PIN_AND_HASH_PREFLIGHT = PASS
SYSTEM_COMPOSITION_EXECUTION = BLOCKED_ENVIRONMENT
NEW_BENCHMARKS = NONE
UNIQUE_FINAL_CHASSIS = NOT_ESTABLISHED
```

The independent NAIA candidate Gate-2 queue remains governed by its own frozen order (AI Butler first); this product-wide system-chassis probe is a separate decision path.

## Evidence

- [Top 10 first-sieve queue](system-chassis-top10-first-sieve-2026-09-30.md)
- [System architecture/chassis contract and assertions](atento-system-architecture-chassis-rescreen-2026-09-30.md)
- [NanoClaw exact-pin verification](nanoclaw-exhaustive-verification-2026-09-30.md)
- [AI Butler exact-pin verification](aibutler-exhaustive-verification-2026-09-30.md)
- [Integrated candidates exact-pin source and CI verification](integrated-chassis-source-verification-2026-10-01.md)
- [External benchmark cross-check: OrchBench and BenchLM](system-chassis-benchmark-crosscheck-2026-09-30.md)
