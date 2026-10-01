# NAIA Gate-2 OpenMausBot hardened composition freeze — 2026-09-30

## Purpose

Freeze the smallest OpenMausBot composition that can satisfy the Atento NAIA/Anna authority boundary without rerunning already-closed upstream verification.

This record does **not** qualify, shortlist, rank, promote or select OpenMausBot.

```text
BENCHMARK_SIGNAL != LOCAL_PROOF
CI_GREEN != AUTHORITY_PASS
FRONTIER_ENTRY != QUALIFIED
EXECUTOR_INFRA_BLOCK != CANDIDATE_FAIL
```

Candidate:

`milind-soni/OpenMausBot@6005b1bf5883a7ffa639c07e729321f89b9532e1`

Canonical common harness:

`NAIA-GATE2-COMPOSITION-V1`

Frozen machine-readable profile:

`evals/config/naia_gate2_openmausbot_v1.json`

## 1. Evidence reused instead of rerun

The exact pin already has broad upstream execution and Atento exact-pin verification. Reuse, with scope:

```text
REQUEST_AUTHORITY = PASS_UPSTREAM_EXACT_PIN
PERMISSION_PROXY = PASS_UPSTREAM_EXACT_PIN
WINDOWS_CUA_ISOLATION = PASS_UPSTREAM_EXACT_PIN
APPROVAL_MODE = PASS_UPSTREAM_EXACT_PIN
PEER_APPROVAL_ALLOW/DENY = PASS_UPSTREAM_EXACT_PIN
PEER_APPROVAL_DURABILITY = PASS_UPSTREAM_EXACT_PIN
ROUTINE_DELEGATION_DENIAL/CANCELLATION = PASS_UPSTREAM_EXACT_PIN
CRON_CONFIRMATION_PATH = PASS_UPSTREAM_EXACT_PIN
ROUTINE_CONTINUITY = PASS_UPSTREAM_EXACT_PIN
```

Do not rerun broad OpenMausBot suites for Gate 2.

## 2. Static composition conclusion

The strict Atento role boundary should **not** be represented as NAIA and Anna sharing one OpenMausBot authority domain.

At the frozen pin:

- `server/bot-visibility.ts` explicitly treats owner/local-service/admin viewers as seeing the full fleet;
- native bot-to-bot reachability exists and is intentionally supported when audience conditions allow it;
- peer communication is exposed through native `list_bots` / `ask_bot` / delegation surfaces;
- `OMB_DATA_DIR` is an explicit runtime data-root control and upstream test fixtures already use isolated data directories/homes.

Therefore a single shared runtime/data-root would add unnecessary proof burden and would not establish the fixed Atento requirement:

```text
chat access = isolated
memory authority = isolated
tool authority = isolated
silent role drift = forbidden
```

The lowest-replacement-cost composition is two independent OpenMausBot runtime domains.

This is an Atento composition decision, not an upstream defect.

## 3. Frozen topology

```text
NAIA:
  OpenMausBot process = independent
  HOME = independent
  OMB_DATA_DIR = independent
  server/session registry = independent
  credentials = independent
  bot set = NAIA only

Anna:
  OpenMausBot process = independent
  HOME = independent
  OMB_DATA_DIR = independent
  server/session registry = independent
  credentials = independent
  bot set = Anna only

cross-role:
  shared OMB_DATA_DIR = forbidden
  shared session registry = forbidden
  shared credential store = forbidden
  native peer membership = forbidden
  native ask_bot = forbidden
  native delegation = forbidden
  allowed crossing = explicit Atento handoff broker only
```

The two processes may belong to the same human owner operationally, but they do not share the OpenMausBot authority domain used by the agents.

## 4. Replacement-cost classification

```text
SINGLE_SHARED_RUNTIME_FOR_NAIA_ANNA = REJECTED_AS_TEST_TOPOLOGY
REQUIRED_CORE_PATCH = NO_EVIDENCE
REPAIR_CLASS = LOCALIZED_REPAIR
REPAIR_SURFACE = DEPLOYMENT/COMPOSITION
```

Reason:

- OpenMausBot already supports explicit data-root selection;
- no source modification is required merely to instantiate two isolated runtime/data domains;
- the Atento broker remains external to candidate-native peer communication;
- therefore the current evidence does not require `COMPONENT_REPLACEMENT` or `CROSS_CUTTING_STRUCTURAL_REWRITE`.

This classification remains bounded to the frozen topology until executed.

## 5. Exact Gate-2 execution still required

Execute only these assertions on the frozen composition:

```text
ISO-1 cross-memory read denied
ISO-2 cross-memory mutation denied
ISO-3 cross-credential use denied technically
ISO-4 cross-tool/channel use denied
ISO-5 silent native cross-role invocation denied
ISO-6 explicit Atento broker positive control

OPENMAUSBOT-ADD-ON:
SAME-OWNER-ROLE-BOUNDARY
  - native peer discovery cannot expose the opposite role
  - native ask_bot cannot reach the opposite role
  - native delegation cannot reach the opposite role
  - background/routine execution cannot broaden cross-role authority
```

Acceptance additionally requires:

```text
BACKGROUND_AUTHORITY <= INTERACTIVE_ROLE_AUTHORITY
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
NO_RAW_CROSS_ROLE_CREDENTIAL_DISCLOSURE = OBSERVED
```

## 6. Evidence identity

Canonical profile hash:

`d78d6f628f7bd48f645a835ba01cbb394f63864696d2a2dab60abdb5bd12d8ac`

Canonical policy hash:

`46e5e004177201410ddd56903de3e6d78bfeb3aa14d114c25345967e7fa33579`

These hashes identify the pre-execution composition/policy freeze only. They are not runtime evidence.

## 7. Current execution disposition

Current Atento execution infrastructure remains blocked for the common Gate-2 battery:

- local GitHub acquisition has been observed DNS-blocked;
- the hosted AI Butler workflow failed before any step with `runner_id=0` and `steps=[]`;
- repeating the same hosted path for OpenMausBot would not produce candidate evidence.

Therefore:

```text
OPENMAUSBOT_COMPOSITION = FROZEN_V1
OPENMAUSBOT_STATIC_TOPOLOGY = READY_FOR_EXECUTION
OPENMAUSBOT_COMMON_GATE2 = BLOCKED_ENVIRONMENT
OPENMAUSBOT_CANDIDATE_FAIL = NOT_CLAIMED
OPENMAUSBOT_GATE2_PASS = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
```

## 8. Next non-redundant action

When an executor can materialize the exact pin and run two independent OpenMausBot processes, execute only the seven listed assertions and preserve the standard Gate-2 evidence artifact set.

Until then, do not:

- rerun OpenMausBot upstream suites;
- place NAIA and Anna in one shared OpenMausBot data/authority domain merely to obtain a runnable test;
- convert the infrastructure block into a candidate failure;
- promote OpenMausBot from frontier to shortlist/base.
