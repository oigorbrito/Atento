# NAIA Gate-2 composition preparation frontier V1 — 2026-09-30

## Purpose

Close the static composition-preparation phase for the 12 candidates in the frozen Gate-2 transferable-evidence frontier.

This record does **not** qualify, rank, shortlist, promote or select any candidate.

Canonical harness:

`NAIA-GATE2-COMPOSITION-V1`

Canonical matrix:

`evals/config/naia_gate2_composition_v1.json`

## 1. Preparation gate

```text
FRONTIER_CANDIDATES = 12
FROZEN_COMPOSITION_IDENTITIES = 12/12
PIN_REPO_HARNESS_RECONCILIATION = PASS
TOPOLOGY_HASH_RECONCILIATION = PASS
POLICY_HASH_RECONCILIATION = PASS

GATE2_EMPIRICAL_PASS = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

A frozen identity means only that the exact candidate pin, Atento topology, hardened policy and required assertion set are no longer ambiguous.

```text
FROZEN != EXECUTED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED
```

## 2. Frozen frontier

| Order | Candidate | Frozen config | Static preparation |
|---:|---|---|---|
| 1 | AI Butler | `evals/config/naia_gate2_aibutler_v1.json` | READY; executable hosted harness repaired, post-repair run not observed |
| 2 | OpenMausBot | `evals/config/naia_gate2_openmausbot_v1.json` | READY |
| 3 | NanoClaw | `evals/config/naia_gate2_nanoclaw_v1.json` | READY; exact core/channel/provider/gateway recipe frozen |
| 4 | AgentOS | `evals/config/naia_gate2_agentos_v1.json` | READY |
| 5 | Rome | `evals/config/naia_gate2_rome_v1.json` | READY |
| 6 | Suna | `evals/config/naia_gate2_suna_v1.json` | READY |
| 7 | Rakazo | `evals/config/naia_gate2_rakazo_v1.json` | READY |
| 8 | Letta Code | `evals/config/naia_gate2_letta_code_v1.json` | READY |
| 9 | Octop | `evals/config/naia_gate2_octop_v1.json` | READY |
| 10 | QwenPaw | `evals/config/naia_gate2_qwenpaw_v1.json` | READY; Python 3.11 qualification scope, unresolved Python 3.13 PTY path excluded |
| 11 | RustFox | `evals/config/naia_gate2_rustfox_v1.json` | READY |
| 12 | Engram | `evals/config/naia_gate2_engram_v1.json` | READY; new split-AgentDef composition frozen, not executed |

The table order is the pre-existing frozen execution order, not a preference or ranking.

## 3. Static integrity gate

A dependency-free repository validator now exists:

`tools/naia_gate2/validate_frozen_configs.py`

It checks:

- exactly the 12 common-matrix candidates;
- exact repository and frozen SHA;
- harness identity;
- canonical SHA-256 of the serialized `topology`;
- canonical SHA-256 of the serialized `policy`;
- common ISO-1..ISO-6 assertion set;
- exact candidate-specific add-on assertion set;
- common-matrix add-on identity.

Before this record was written, all 12 machine-readable configs were independently re-read from `main` and their repository, pin, harness, topology hash and policy hash were recomputed mechanically.

Observed reconciliation:

```text
candidate_count = 12
all_ok = true
```

The check also exposed and corrected two preparation-only defects before closure:

- OpenMausBot's stored hash literals did not match its serialized freeze and lacked a canonical `policy` object;
- AgentOS stored hardened profile fields outside the canonical `policy` object, so the stored hash literals did not identify the actual frozen policy.

Both were corrected without changing candidate behavior, runtime evidence or decision state.

## 4. AI Butler evidence-path repair

The previous AI Butler Gate-2 injected test used a synthetic in-process echo for ISO-6.

That path is no longer accepted.

Current workflow:

- calls the real Atento `ExplicitHandoffBroker` through `tools/naia_gate2/broker_runtime_adapter.py`;
- rejects an injected authority-bearing `credential` field;
- builds a canonical result only after exact-pin assertions pass;
- validates that result with `evals.atentoeval.composition validate-result`;
- uploads the validated result.

Therefore:

```text
AI_BUTLER_SYNTHETIC_ISO6 = REMOVED
AI_BUTLER_REAL_BROKER_PATH = WIRED
AI_BUTLER_CANONICAL_RESULT_VALIDATION = WIRED
AI_BUTLER_POST_REPAIR_EXECUTION = NOT_OBSERVED
```

Prior runner-provisioning failures remain infrastructure evidence only.

## 5. NanoClaw recipe ambiguity closed

The NanoClaw SUT identity is now frozen from candidate-owned exact-run evidence rather than subjective selection.

```text
core = 4c1eabd3ddd74cc3d71b1871da857391a9411c8d
channels = 3f7e13b591a0c8980242b81ceff4b3f542ef839a
provider registry = 3959d1f055cba2320cf843b30834a278250346b8

channel = add-telegram / @chat-adapter/telegram@4.29.0
provider = add-codex / @openai/codex@0.155.1
gateway = add-onecli
OneCLI gateway = 1.41.0
OneCLI CLI = 2.2.5
OneCLI SDK = 2.2.1
```

The complete Atento recipe remains unexecuted.

## 6. Engram prior failure preserved and treatment narrowed

The previously tested single AgentDef exposing both scheduled and interactive adapter identities remains:

```text
DUAL_IDENTITY_ONE_AGENTDEF = FAIL_EMPIRICAL_FOR_TESTED_COMPOSITION
```

Exact frozen-pin source establishes a narrower supported treatment:

```text
scheduled Job.agent_id
  -> task.agent
  -> AgentDef
  -> AgentDef.allowed_tools
  -> run_task_core ToolRegistry filtering
```

The new frozen composition therefore uses distinct NAIA interactive and scheduled AgentDefs with static toolsets.

This is `LOCALIZED_REPAIR` at the composition/binding layer until executed. It does not convert the prior FAIL into a PASS.

## 7. Execution blocker remains separate

The known infrastructure observations remain:

```text
local exact-pin acquisition = previously BLOCKED_DNS
hosted AI Butler attempts = runner_id 0 / steps []
candidate result from those attempts = NONE
```

Rule:

```text
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
```

Do not rerun the broken hosted path merely to reproduce an unassigned runner.

## 8. Next gate

Static composition definition is exhausted for the current frontier.

The next decision-relevant work is empirical execution in the existing frozen order, beginning with AI Butler when an executor actually runs steps.

For each candidate:

1. materialize the exact frozen pin;
2. verify the dedicated frozen topology/policy hashes;
3. execute ISO-1..ISO-6;
4. execute only the matrix-listed add-ons;
5. preserve canonical evidence artifacts;
6. classify `PASS_WITH_SCOPE`, `FAIL_LOCALIZED`, `FAIL_STRUCTURAL`, `BLOCKED_ENVIRONMENT` or `INVALID_EVIDENCE`;
7. stop immediately on a proven cross-cutting structural rewrite.

No further broad static candidate audit is authorized merely because execution remains blocked.

## 9. Current gate state

```text
GATE2_STATIC_COMPOSITION_PREPARATION = COMPLETE_V1
FROZEN_COMPOSITION_IDENTITIES = 12_OF_12
FROZEN_CONFIG_INTEGRITY = PASS
EXECUTION_ORDER = UNCHANGED

GATE2_EMPIRICAL_PASS = 0
NEW_TECHNICAL_ELIMINATIONS = 0

NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```
