# PersonalJarvis Gate-2 CI attribution — 2026-09-30

Candidate: `PersonalJarvis/PersonalJarvis@1be33c457739ca7e161ee6fbaf298ec10d4dad3b`

Exact-pin CI is red across several Linux/Windows shards and static gates.

A directly Gate-2-relevant contract test fails:

`tests/contract/test_agent_mcp_harmony.py::test_every_society_route_is_decided`

The failing contract reports that newly exposed Society/MCP routes lack an explicit policy classification. The affected surface includes chat-group operations and a society-agent routine-operation route.

```text
SOCIETY_MCP_AUTHORITY_SURFACE = INCOMPLETE_POLICY_COVERAGE
NEW_ROUTE_POLICY_COVERAGE = FAIL_EXACT_PIN
ROUTINE_OPERATION_ROUTE_POLICY = UNRESOLVED
CHAT_GROUP_ROUTE_POLICY = UNRESOLVED
```

Other exact-pin failures include static-gate, Windows CLI, UI/provider and realtime regressions. They are not independently promoted to Gate-2 failures here.

The authority gap appears bounded to the existing MCP/policy decision table; current evidence does not establish a cross-cutting structural rewrite.

```text
REPAIR_CLASS = LOCALIZED_POLICY_COVERAGE
CROSS_CUTTING_STRUCTURAL_REWRITE = NOT_ESTABLISHED
PERSONALJARVIS_ELIMINATED = NO
PERSONALJARVIS_FRONTIER_ELIGIBLE = NO_AT_CURRENT_PIN
```

Reconsideration for the transferable-evidence frontier requires a changed pin or exact proof that all relevant Society/MCP routes receive explicit deny/allow/approval treatment.
