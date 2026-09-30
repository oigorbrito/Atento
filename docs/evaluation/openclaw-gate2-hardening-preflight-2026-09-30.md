# OpenClaw Gate-2 hardening preflight — 2026-09-30

## Scope

Candidate: `openclaw/openclaw@ca8f24d05fc49a224adab0c9426077fd8d93801d`

Purpose: execute the smallest non-runtime Gate-2 test before spending composition/runtime budget:

> Can the required NAIA authority/isolation profile be expressed through supported OpenClaw configuration and deployment boundaries without a core patch?

This is a source/config-contract preflight. It is not runtime proof.

## Exact-pin evidence corrected

A direct GitHub Actions query by `head_sha` found exact-pin hosted execution that the earlier connector lookup missed.

Observed push runs at the exact SHA:

```text
CI              = SUCCESS  run 36650380651
CodeQL          = SUCCESS  run 36650379796
Workflow Sanity = SUCCESS  run 36650379848
```

The CI run is health evidence only. The relevant QA smoke lane was skipped for this push, so the NAIA composition is not claimed executed.

## Profile expressibility test

The exact-pin Zod schema and docs support all of these without modifying OpenClaw core:

### Cross-agent/session restriction

```json5
tools: {
  sessions: { visibility: "self" },
  agentToAgent: { enabled: false }
}
```

The exact schema admits `self|tree|agent|all` and an explicit `agentToAgent.enabled: false`.

The exact pin also contains an executable QA scenario,
`qa/scenarios/channels/a2a-allowlist-denied-cross-agent-send.yaml`,
whose expected contract is a technical `forbidden` result before any target model work or target session creation when the target is outside the allowlist.

This is executable test-source evidence, not proof that the scenario ran in the exact push CI.

### Tool/exec restriction

The exact schema provides:

```text
tools.allow / tools.deny
agents.entries.*.tools.allow / deny
tools.exec.mode = deny | allowlist | ask | auto | full
agents.entries.*.tools.exec.mode = same
```

Restrictive policy layers only narrow authority; deny wins.

### Sandbox isolation

The exact schema provides:

```text
sandbox.mode  = off | non-main | all
sandbox.scope = session | agent | shared
workspaceAccess = none | ro | rw
```

Per-agent sandbox configuration is supported.

### Strict NAIA/Anna trust boundary

The exact-pin trust model explicitly states that mutually untrusted/adversarial domains should use separate Gateways, preferably separate OS users/hosts. This matches the Atento requirement better than forcing both roles into one Gateway.

Therefore the intended topology can be expressed as:

```text
NAIA OpenClaw Gateway/runtime/store
        |
 explicit Atento broker
        |
Anna independent runtime/store
```

No OpenClaw core patch is required merely to express that boundary.

## Result

```text
OPENCLAW_PROFILE_EXPRESSIBILITY = PASS_STATIC_WITH_SCOPE
CORE_PATCH_REQUIRED_TO_EXPRESS_POLICY = NO
CROSS_AGENT_RESTRICTION_PRIMITIVE = PRESENT
PER_AGENT_TOOL_POLICY = PRESENT
EXEC_DENY_ALLOWLIST_MODE = PRESENT
PER_AGENT_SANDBOX = PRESENT
SEPARATE_GATEWAY_STRICT_BOUNDARY = SUPPORTED_ARCHITECTURE

EXACT_PIN_CI = PASS
A2A_DENIAL_SCENARIO_SOURCE = PRESENT
A2A_DENIAL_SCENARIO_EXACT_PIN_EXECUTION = NOT_ESTABLISHED
ATENTO_TWO_ROLE_RUNTIME_COMPOSITION = NOT_RUN

OPENCLAW_GATE2 = NOT_CLOSED
```

The result rules out `CROSS_CUTTING_STRUCTURAL_REWRITE` merely to create the hardened authority topology. It does not prove that the composed profile behaves correctly at runtime.

## Smallest next empirical test

Freeze two independent role runtimes/stores and run only:

1. denied cross-role session/tool invocation;
2. denied cross-role memory/credential access;
3. one allowed NAIA-local low-risk effect;
4. same effect through scheduled/background execution;
5. verify restart does not broaden effective policy;
6. explicit broker handoff as the only permitted cross-role path.

Acceptance:

```text
CROSS_MEMORY_READ = DENIED
CROSS_CREDENTIAL_USE = DENIED
CROSS_TOOL_OR_CHANNEL_USE = DENIED
SILENT_AGENT_INVOCATION = DENIED
BACKGROUND_AUTHORITY <= INTERACTIVE_AUTHORITY
AUTHORITY_AFTER_RESTART <= AUTHORITY_BEFORE_RESTART
EXPLICIT_BROKER_HANDOFF = ONLY_ALLOWED_CROSS_ROLE_PATH
```

Until that composition executes, OpenClaw remains unqualified.
