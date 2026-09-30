# NAIA static residual disposition v1 — 2026-09-30

## Purpose

This record executes step A of the frozen residual-only plan:

```text
A. resolve config/source-only residuals first
```

It does not run a local microprobe, rank candidates, create a shortlist, qualify a current pin, select a NAIA base, or select the final NAIA/Anna topology.

Canonical inputs:

- `docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md`
- `docs/evaluation/naia-expanded-upstream-evidence-matrix-2026-09-29.md`
- candidate-specific current-pin / transfer / admission audits already on `main`

This pass asks only:

> Does existing exact-pin source/config/topology evidence already tell us enough to avoid a local runtime probe now?

Rules preserved:

```text
STATIC_SOURCE != RUNTIME_PASS
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
HISTORICAL_EVIDENCE != CURRENT_PIN_PROOF
COMPOSE_FIRST != PROBE_NOW
ADAPT_FIRST != QUALIFIED_AFTER_PATCH
DEPENDENCY_FIRST != DEPENDENCY_ACCEPTED
```

## 1. Static closure result

The existing evidence is sufficient to close one cross-candidate question:

```text
GENERIC_VENDOR_DEFAULT_RETEST = NOT_JUSTIFIED
```

For every candidate with a documented permissive, incomplete, externally owned, or composition-dependent authority boundary, a local run of the unchanged vendor/default profile would only reconfirm a known source/config fact.

Therefore:

```text
DEFAULT_PROFILE_RUNTIME_CONFIRMATION = NOT_REQUIRED
HARDENED_COMPOSITION_REQUIRED_BEFORE_LOCAL_PROBE = YES
```

This is a static/config closure only. It does not prove that any future hardened composition works.

## 2. Candidate disposition

Legend:

```text
COMPOSE_FIRST    = freeze the exact hardened candidate profile/topology before any local proof
DEPENDENCY_FIRST = freeze the exact external authority owner/profile before any local proof
UPSTREAM_FIRST   = exact current-pin changed-contract upstream evidence remains the first unresolved step
ADAPT_FIRST      = exact-pin source already shows the target property is absent and must be implemented before it can be tested
LEGAL_SEPARATE   = non-empirical adoption boundary remains independent of technical runtime evidence
```

| Candidate | Static disposition | Source/config conclusion | Local probe now |
|---|---|---|---|
| OpenClaw | COMPOSE_FIRST | Vendor/default authority is not the NAIA target; strict NAIA/Anna boundary requires separate authority domains or equivalent composed isolation | NO |
| OpenMausBot | UPSTREAM_FIRST | Broad historical product retest remains unnecessary; only exact current-pin changed lending/request-auth/session contracts could precede composition if still decision-relevant | NO |
| QwenPaw | COMPOSE_FIRST | Sandbox-enabled/fail-closed behavior, cron authority and chosen browser authority profile must be frozen before proof | NO |
| AI Butler | COMPOSE_FIRST | Existing shell/credential/scheduler contracts transfer statically; target profile/bank topology and one scheduled credential action remain composition-specific | NO |
| NanoClaw | COMPOSE_FIRST | Core isolation/gateway design is known; one exact channel+gateway+provider+schedule+memory recipe is required first | NO |
| TrustClaw | DEPENDENCY_FIRST | Local memory/cron contracts are known; effective action authority is partly owned by Composio/Vercel/provider seams | NO |
| Open Assistant | LEGAL_SEPARATE + COMPOSE_FIRST | Technical hardening requires per-action authority, separated role stores/credentials and browser network policy; BSL adoption remains a separate gate | NO |
| Suna | COMPOSE_FIRST | Existing governance exists, but explicit risk/deny policy and strict role topology are composition choices | NO |
| Letta Code | COMPOSE_FIRST | Unrestricted/default and optional shell/cross-agent boundaries are already known; strict permission/runtime/memory composition must be frozen first | NO |
| PersonalJarvis | COMPOSE_FIRST | Scheduled preauthorization and namespaced memory are known; background grants and role credential/runtime boundaries remain composition-specific | NO |
| Rakazo | COMPOSE_FIRST | Approval replay and uncertain-effect handling are already evidenced; consequential default remains permissive until hardened profile is composed | NO |
| Gobii | COMPOSE_FIRST | Per-agent state/secret primitives are known; contact/email review policy, org/global grants and peer messaging require exact composition | NO |
| Octop | COMPOSE_FIRST | HITL/tool-guard defaults and connector selection behavior are known; hardened policy and cron connector picks must be frozen first | NO |
| Agent Zero | COMPOSE_FIRST | Project memory is isolated by default, but tool policy/plugins/OAuth/host CUA authority requires an exact role/profile composition | NO |
| Rome | COMPOSE_FIRST | Profile isolation and approval primitives exist; autoapproval/provider-native authority must be explicitly constrained in the chosen composition | NO |
| OpenGrokBot | COMPOSE_FIRST | Per-bot container and approval endpoint exist; outward browser enforcement, routine authority and brokered peer path remain composition-specific | NO |
| SelfAgent | ADAPT_FIRST | Technical confirmation is not centrally enforced; scheduler startup reload/re-arm is not wired; scheduled raw shell bypasses the interactive authority path | NO |
| GoClaw | COMPOSE_FIRST | Per-agent policy/session primitives exist; default shell, instance-global memory and broad delegation require hardened composition | NO |
| Nebo | COMPOSE_FIRST | Interactive safeguards exist; OriginSystem/background authority and strict role authority domains require exact composition | NO |
| AutoMate | COMPOSE_FIRST | Central allow/deny and scheduler reload exist; approval enforcement, elevation bounds and shared-memory exclusion require exact composition | NO |
| AgentOS | COMPOSE_FIRST | Scheduler/security primitives exist; interactive/cron bypass defaults and external browser policy require narrow frozen profiles | NO |
| OpenAgentd | COMPOSE_FIRST | Policy engine exists but AutoAllow/trusted-host defaults do not satisfy NAIA; blocking ruleset, shell hardening and browser path must be frozen first | NO |
| HubOS | COMPOSE_FIRST | ToolGuard/approval mechanics exist, but guard errors/background context/default-enabled tools/open channels require explicit hardened composition | NO |
| RustFox | COMPOSE_FIRST | Schedule restore, high-risk supervisor and SecretBridge are evidenced; universal effect ownership and role-separated grants remain composition-specific | NO |
| Engram | COMPOSE_FIRST | Egress/signed autonomy/scheduler contracts are evidenced; consequential browser/trusted-run authority and separate ENGRAM_HOME/runtime roles require composition | NO |
| Holt | DEPENDENCY_FIRST | Workspace memory and OS scheduling are known; effective interactive/noninteractive authority belongs to the exact selected CLI brain/provider, with shared global credentials/channels otherwise | NO |

No row is a rank, score, tier, recommendation, shortlist or finalist designation.

## 3. What step A closes

The following questions do not require local execution:

```text
Should known permissive vendor defaults be rerun just to observe permissiveness? NO
Should generic schedule persistence be rerun where current evidence already closes it? NO
Should generic browser existence be rerun? NO
Should generic exactly-once behavior be benchmarked? NO
Should strict isolation be inferred from workspace/project/session naming? NO
Should dependency-owned authority be treated as candidate-local authority? NO
```

Known exact-pin absences or unsafe defaults remain evidence. They are not converted into runtime FAIL labels because no hardened composition has executed.

## 4. Execution-gate audit

Residual microprobe gate from the canonical ledger:

```text
1. exact candidate pin frozen
2. exact hardened profile/topology/dependency frozen
3. upstream implementation + relevant tests/evals already mapped
4. available current-pin run/CI evidence checked
5. one unresolved Atento property named
6. the planned probe changes the decision evidence if it passes or fails
7. pre/post adaptation diff will be preserved
```

Current generic cross-candidate state remains:

```text
GATE_1_EXACT_PIN = SATISFIED_BY_CANONICAL_AUDITS
GATE_2_HARDENED_COMPOSITION = NOT_SATISFIED_GENERICALLY
GATE_3_UPSTREAM_MAPPING = SATISFIED_FOR_FROZEN_V1
GATE_4_CURRENT_PIN_CI_RUN_CHECK = SATISFIED_AS_OBSERVATION_ONLY
GATE_5_SINGLE_PROPERTY = NOT_FROZEN_GENERICALLY
GATE_6_DECISION_RELEVANCE = NOT_ESTABLISHED_GENERICALLY
GATE_7_DIFF_PRESERVATION = PLANNED_NOT_EXECUTED
```

Post-pass exception already merged after this static sweep:

```text
Engram:
  GATE_2_HARDENED_COMPOSITION = SATISFIED_FOR_FROZEN_V1_COMPOSITION
  GATE_5_SINGLE_PROPERTY = ENGRAM_BROWSER_EFFECT_AUTHORITY
  GATE_6_DECISION_RELEVANCE = ESTABLISHED_FOR_BOUNDED_BROWSER_AUTHORITY_PROBE
  RUNTIME_EXECUTION = NOT_STARTED
```

Canonical freeze:

`docs/evaluation/naia-engram-hardened-composition-freeze-2026-09-30.md`

This exception does not establish a generic execution order or candidate preference.

Therefore:

```text
LOCAL_RESIDUAL_PROBE_EXECUTION = NOT_STARTED
RP_AUTH_01 = NOT_EXECUTED
RP_ISO_01 = NOT_EXECUTED
RP_LIFE_01 = NOT_EXECUTED
RP_BROWSER_01 = NOT_EXECUTED
RP_EFFECT_01 = NOT_EXECUTED
RP_DEP_01 = NOT_EXECUTED
RP_COST_01 = NOT_EXECUTED
```

This is intentional fail-closed behavior for every candidate/profile that has not yet closed gates 2 and 6.

Engram is now the bounded exception: its hardened composition and single browser-authority property are frozen, so the matching residual probe is ready but still not executed.

## 5. Next allowed block

The next allowed work is not another broad audit and not a generic benchmark.

It is:

```text
WHEN one or more remaining residuals are explicitly established as decision-relevant:
  freeze the exact candidate pin + hardened profile/topology/dependency
  name exactly one unresolved Atento property
  preserve the pre-composition baseline
  execute only the matching residual microprobe
  capture adaptation/change-surface/cost in the same work
ELSE:
  do not execute a local microprobe
```

Special entry modes remain:

```text
OpenMausBot -> UPSTREAM_FIRST only for exact current-pin changed contracts if still required
TrustClaw   -> DEPENDENCY_FIRST
Holt        -> DEPENDENCY_FIRST
SelfAgent   -> ADAPT_FIRST
Open Assistant -> R-LEGAL remains separate from technical evidence
```

## 6. State after this pass

```text
STATIC_RESIDUAL_DISPOSITION = COMPLETE_V1
GENERIC_LOCAL_BENCHMARK = NOT_JUSTIFIED
GENERIC_VENDOR_DEFAULT_RETEST = NOT_JUSTIFIED
LOCAL_RESIDUAL_PROBE_EXECUTION = NOT_STARTED
ENGRAM_HARDENED_COMPOSITION = FROZEN_V1
ENGRAM_BROWSER_EFFECT_AUTHORITY = UNPROVEN
RESIDUAL_BROWSER_AUTHORITY_PROBE = READY_NOT_EXECUTED

CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
CROSS_AGENT_TOPOLOGY = NOT_SELECTED
```

No promotion or candidate ordering is created by this record.
