# Independent three-project evolution and remerge — 2026-10-06

## Question

Can NAIA, Anna and Apollo evolve independently after extraction and then be reassembled without role-owned change collisions or boundary violations?

## Experiment

The probe starts from the three self-contained logical role projects established by the prior topology experiment.

For each role independently it:

1. copies the role root into its own temporary Git repository;
2. commits an identical baseline snapshot;
3. applies one role-owned source change and one matching role-owned test;
4. compiles and executes that role's tests;
5. builds a wheel independently;
6. records the exact changed paths;
7. removes generated artifacts and repository metadata;
8. reassembles all three evolved role roots into a fresh Atento-style `agents/` tree;
9. re-runs the logical boundary validator and all three role test suites.

Pairwise changed-path intersections are then measured.

## Evidence hygiene correction

The first execution (`37552986830`) passed functionally but its evidence set accidentally included generated `__pycache__/*.pyc` files because compilation occurred before the temporary evolution commit.

That run is not used for the final changed-path claim.

The probe was corrected to remove generated interpreter artifacts before committing the independently evolved source.

## Accepted execution

Workflow: `Independent three-project evolution remerge`

Head:

`b0fb6b6d48351ecce8de59ac00e52a3f0e94035c`

Run:

`37553047966`

Conclusion:

`success`

Artifact digest:

`sha256:63c3753e55983337350b5f05a53397ca20abaa1b1d9855491994cfb899a86380`

Observed role-owned changes:

```text
NAIA:
  atento_naia/__init__.py
  tests/test_independent_evolution.py

ANNA:
  atento_anna/__init__.py
  tests/test_independent_evolution.py

APOLLO:
  atento_apollo/__init__.py
  tests/test_independent_evolution.py
```

Each independently evolved project:

- compiled successfully;
- passed its own tests;
- built a wheel independently.

Pairwise changed-path collisions after role-root qualification:

```text
NAIA : ANNA   = 0
NAIA : APOLLO = 0
ANNA : APOLLO = 0
TOTAL         = 0
```

The reconstructed tree passed the logical-boundary gate and all three role test suites.

## Decision

```text
INDEPENDENT_ROLE_EVOLUTION_3_OF_3     = PASS
REMERGE_AFTER_INDEPENDENT_CHANGES     = PASS
ROLE_OWNED_CHANGED_PATH_COLLISIONS    = 0
SHARED_CONTRACT_CHANGE_COORDINATION   = NOT_TESTED
HOSTED_MULTIREPO_OPERATIONAL_COST     = NOT_TESTED
PRODUCTION_REPO_TOPOLOGY_SELECTION    = NOT_YET_AUTHORIZED
```

## Interpretation

This is stronger than a split/remerge of unchanged trees: each role can carry an independent source/test commit and then be reassembled with no changed-path collision in the current role-owned fixture.

It still does not establish the cost or safety of simultaneous changes to the shared Host/runtime contract. Shared-contract coordination is the next topology-specific failure mode that must be tested before physical repository separation can be preferred.
