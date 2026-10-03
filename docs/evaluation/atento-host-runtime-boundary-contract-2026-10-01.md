# Atento host-runtime boundary contract — 2026-10-01

## Purpose and status

This contract defines the observable boundary required to evaluate an Atento composition that runs NAIA, Anna, and Apollo. It is an evaluation contract, not a production API, an implementation choice, or a candidate-selection decision.

```text
HOST_RUNTIME_CONTRACT = DEFINED_FOR_EVALUATION
ATENTO_PRODUCT_RUNTIME = NOT_PRESENT_IN_REPOSITORY
NANOCLAW = PROVISIONAL_NAIA_BASE_DIRECTION; NOT_QUALIFIED
SYSTEM_PROFILE_GATE = NOT_PASSED
ANNA_BASE = PSYCHAGENT_USER_DIRECTED; NOT_QUALIFIED
COMMON_THREE_ROLE_CHASSIS = NO_WINNER
```

The Atento repository currently contains evaluation harnesses and candidate probes, but no product runtime/application entrypoint to bind or test. The existing NanoClaw probe uses the exact pinned candidate's Docker session driver, SQLite/session/mailbox code, CLI, and a test-harness broker adapter. It does not start the candidate's provider/channel/application runtime or an Atento product host.

## Contract boundary

A runtime adapter conforms only when the behavior below is enforced by the host/runtime boundary and can be observed in an execution trace or persisted state. Prompt instructions, role names alone, and profile declarations do not count as enforcement.

### Role resolution and session ownership

- Resolve the active role from trusted host/session identity. Do not accept a caller-supplied role name as authority.
- Bind each role to its own runtime identity, chat/session namespace, state root, provider identity, tool policy, and credential grant.
- Reject missing, ambiguous, stale, or mismatched role/session bindings before reading private state or executing an effect.
- A restart or session reconstruction must restore the same role binding and must not import another role's transcript, memory, tool grants, or credentials.
- Shared control-plane infrastructure is allowed only when its stored fields and access checks preserve these boundaries.

### Handoff and recipient authorization

- Cross-role transfer uses the existing Atento reference broker contract and a closed, typed, size-bounded envelope.
- Only the declared minimum request data crosses. Memory, transcript, credential, tool, session, runtime, or capability handles are not transferable authority.
- The destination is fixed and checked against the role map before delivery.
- Delivery to the recipient's mailbox/session does not itself authorize an action.
- The recipient re-evaluates the request under its own current policy and identity before any action. The resulting execution record names the recipient as the actor.
- Untyped, undeclared, overbroad, wrong-recipient, stale, and broker-bypass requests fail closed. Sensitive-consent positive paths remain outside this contract until their policy is separately decided.

### Background work, retry, and recovery

- A scheduled task records an immutable owning role and task/session identity at creation.
- At fire time, retry, and recovery, the host re-resolves that owner and applies the same or narrower grants than the role's interactive path.
- A task cannot be listed, changed, cancelled, resumed, executed, or adopted by another role through group, session, task, or stale-identity substitution.
- After a host/runtime restart, pending and claimed work is reconciled without losing its role owner. A retry cannot restore revoked authority or broaden the grant.
- When identity, policy, durable state, or scheduler control is unavailable, the work is held/failed closed and leaves an auditable reason; it is not run with ambient/default authority.

### Credentials and tool authority

- Runtime identity, provider credentials, channel credentials, and external-effect tools are bound to the owning role by an enforceable boundary.
- Raw credential material is absent from other roles' workspaces, prompts/model-visible context, process arguments, traces, and logs.
- Tool permissions are resolved by the host for the current role and operation. A handoff message cannot carry a tool grant.
- Evaluation uses synthetic grants and inert effects; it does not require production credentials or live external actions.

## Evaluation adapter surface

An implementation may use a shared process, isolated processes/containers, separate services, or another topology. The test adapter must expose equivalent observations for:

1. resolving a role and its active session;
2. reading/writing role-scoped state;
3. receiving a typed handoff into the destination session;
4. checking recipient-side authorization and the acting identity;
5. creating and inspecting a role-owned scheduled task;
6. firing, retrying, stopping, restarting, and recovering that task;
7. enumerating effective tools and credential visibility for each role;
8. recording audit events without private content or secrets.

The adapter exposes outcomes and ownership metadata, not raw secrets or unrestricted runtime handles. This lets the same assertions be applied to different chassis without prescribing one internal architecture.

## Gate assertions and current evidence

Reuse the system profile assertions in `evals/config/system_chassis_nanoclaw_v1.json`: `SYS-CHAT-01`, `SYS-MEM-01`, `SYS-TOOL-01`, `SYS-CRED-01`, `SYS-HANDOFF-01`, `SYS-HANDOFF-02`, `SYS-BG-01`, and `SYS-STATE-01`.

The Atento hosted run `36815873223` recorded 7/7 passing tests with scope. Reusable observations include per-role driver-realized state roots, group/session lookup isolation, synthetic credential mounts, denial of unbrokered direct A2A, typed reference-broker delivery into NanoClaw's mailbox API, receiver-identity CLI enforcement, scheduled-task group ownership, and driver stop/prepare state continuity.

The following remain open because the existing test does not start an Atento product runtime or NanoClaw's complete application/provider/channel runtime:

- production host service wiring for the broker adapter;
- a recipient model/provider decision made inside the runtime, followed by recipient-side reauthorization;
- task firing through each role's runtime;
- retry and recovery across a full host-process restart;
- end-to-end proof that production configuration cannot enable a native handoff bypass;
- live provider/gateway credential custody (to be tested with synthetic material and restricted boundaries first).

Therefore all prior classifications remain scoped:
```text
EXISTING_SYSTEM_PROBE = PARTIAL_PASS_WITH_SCOPE
ATENTO_RUNTIME_INTEGRATION = NOT_RUN
THREE_ROLE_BACKGROUND_EXECUTION_AND_RECOVERY = NOT_RUN
SYSTEM_PROFILE_GATE = NOT_PASSED
```

## Minimum execution record

For any future adapter run, retain:

- Atento commit and exact upstream commit;
- profile and policy hashes;
- changed-file list, dependency/pin delta, and runtime/store/service boundaries;
- command, workflow/run/job IDs, raw test output, and artifact hashes;
- each assertion's PASS / FAIL / BLOCKED / NOT_TESTED status and scope;
- startup, task-fire, retry, and restart/recovery observations;
- synthetic-credential visibility checks and redacted audit output;
- elapsed engineering time, rework, and ongoing services/dependencies separately.

Do not convert a missing runtime or unavailable runner into candidate failure. This evaluation contract is not decision authority. Current role-base decisions are in their ADRs and system composition in `../adr/ADR-SYS-001-common-chassis-mindroom.md`. A passing adapter probe advances evidence only; it does not select or promote a chassis.
