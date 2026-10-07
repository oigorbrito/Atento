# Logical agent boundary experiment — 2026-10-06

## Question

Can Atento establish NAIA, Anna and Apollo as independently governed logical projects inside one physical repository without changing runtime behavior or inventing cross-agent authority?

## Experiment

Three explicit role roots were added:

- `agents/naia/project.json`
- `agents/anna/project.json`
- `agents/apollo/project.json`

Each manifest declares:

- one unique bounded context;
- NanoClaw as the common chassis;
- isolated runtime group required;
- `services/host` as the only shared implementation dependency;
- zero direct agent-to-agent dependencies;
- host-owned, non-caller-selectable role identity.

`tools/validate_logical_agent_boundaries.py` fails closed if those invariants drift or executable files below a role root directly reference another role root.

## Executed evidence

GitHub Actions workflow `Logical agent boundaries` executed on head:

`edd70ec0da5a9ba356d3a8df0a832a1dad2e4405`

Run:

`37552442859`

Conclusion:

`success`

Observed gate:

```text
LOGICAL_AGENT_BOUNDARIES=PASS
DIRECT_AGENT_DEPENDENCIES=0
SHARED_DEPENDENCY=services/host
RUNTIME_CHASSIS=nanoclaw
```

The repository-topology separability workflow also remained green while the three role roots were introduced.

## Scope limit

This proves only that the **logical dependency/authority boundary can be represented and enforced inside the monorepo**.

It does not prove:

- independent build systems;
- independent release cadence;
- independent role test suites;
- physical repository extraction;
- later re-merge cost;
- runtime handoff between agents.

Those remain separate empirical gates.

## Decision

```text
LOGICAL_THREE_PROJECT_TOPOLOGY = PASS
PHYSICAL_THREE_REPO_EXTRACTION = NOT_PROVEN
```

The next matched experiment should add a real, minimal role-owned executable/test surface for each agent without introducing direct role-to-role dependencies. Only after each role can build/test independently should the same commit be extracted into three temporary repositories and compared against the monorepo baseline.
