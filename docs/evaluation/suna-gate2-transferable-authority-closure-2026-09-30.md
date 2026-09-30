# Suna Gate-2 transferable authority closure — 2026-09-30

## Candidate

`kortix-ai/suna@270c4a57c8ae5ffb85eff6d5b9700c5713612f28`

## Exact-pin hosted execution

Direct Actions lookup establishes exact-pin hosted execution:

```text
CI = SUCCESS
Tests = SUCCESS
CodeQL = SUCCESS
secret-scan = SUCCESS
secrets-guard = SUCCESS
DB Migrations = SUCCESS
Deploy Dev = SUCCESS
```

The Tests workflow executed multiple lanes, including a core lane and four browser lanes.

Observed core-lane result:

```text
502 scenarios executed
502 PASS
```

The logs include directly relevant access-control and gateway tests such as:

- IAM privilege denials returning 403;
- project-membership and policy-read denial;
- project-model access denial;
- agent identity/resource-grant authorization;
- gateway credential refresh rejecting unauthenticated access;
- OAuth/account-token authority checks;
- sandbox and gateway access cases.

## Gate-2 clauses transferable from executed evidence

The exact-pin run backs the previously source-only v2 grant/authorization surface and project/account IAM enforcement.

Combined with the frozen transfer audit:

```text
PER_AGENT_V2_GRANT_PATH = EXECUTED_WITH_SCOPE
PROJECT/IAM_DENIAL = RUN_BACKED
GATEWAY_AUTHN/AUTHZ_NEGATIVES = RUN_BACKED
SANDBOX/GATEWAY_ACCESS_SURFACE = EXECUTED
```

This does not make the permissive connector default acceptable. The candidate still requires an explicit hardened project policy.

## Remaining Atento-specific residual

```text
policy.default_mode = risk or stricter
explicit deny rules for consequential tools
NAIA project/repository/grants isolated from Anna project/repository/grants
shared project brain not used across the role boundary
explicit Atento broker = only cross-role path
background trigger grants <= interactive grants
adapter-specific external-effect idempotency/reconciliation where required
```

## Gate-2 disposition

```text
SUNA_EXACT_PIN_TESTS = PASS
SUNA_CORE_SCENARIOS = 502_PASS
SUNA_AUTHORITY_TRANSFER = PASS_WITH_SCOPE
SUNA_ATENTO_RESIDUAL = HARDENED_PROJECT_POLICY + TWO_PROJECT_ROLE_COMPOSITION

SUNA_CURRENT_PIN_QUALIFIED = NO
```

No broad Suna suite should be rerun locally.
