# Three-project extraction roundtrip — 2026-10-06

## Question

After establishing logical NAIA/Anna/Apollo boundaries inside the monorepo, can those three role roots be extracted, built/tested independently, and reassembled without changing the bounded-context contract?

## Experiment

Each role now has a minimal self-contained topology-test surface:

- `pyproject.toml`;
- local zero-dependency build backend;
- one role-owned Python package;
- one independent unittest suite.

This surface intentionally validates repository topology mechanics only. It is not the production implementation of any agent.

The GitHub Actions experiment:

1. validates the monorepo logical boundary gate;
2. copies each role root into a separate temporary directory;
3. compiles each project independently;
4. runs each project's own tests independently;
5. builds one wheel per project with no external dependencies;
6. copies the extracted projects into a fresh reconstructed `agents/` tree;
7. removes generated build artifacts;
8. compares each reconstructed tree byte-for-byte with its source role tree using `diff -qr`;
9. re-runs the logical boundary validator against the reconstructed tree.

## Executed evidence

Workflow: `Three-project extraction roundtrip`

Head:

`03e4af01824fa73a5b74d872b9a6efca5dd4e68c`

Run:

`37552622976`

Conclusion:

`success`

Gate emitted by the workflow:

```text
INDEPENDENT_ROLE_BUILD_TEST_3_OF_3=PASS
LOSSLESS_SPLIT_REMERGE_3_OF_3=PASS
PHYSICAL_REPOSITORY_HOSTING=NOT_TESTED
```

The existing logical-boundary and repository-topology workflows also remained green on the stacked branch.

## Interpretation

This result materially strengthens the earlier topology evidence:

- three logical projects can coexist in one repository;
- each can carry its own build/test contract;
- each can be extracted without needing another role's files;
- the three role roots can be reassembled without changing their tracked contents;
- the shared dependency remains the host contract, not direct role-to-role imports.

However, this is still a **topology-mechanics fixture**. It does not prove that future production NAIA/Anna/Apollo code will remain independently buildable, nor does it measure operational cost of three hosted Git repositories.

## Decision

```text
LOGICAL_THREE_PROJECT_TOPOLOGY      = PASS
INDEPENDENT_BUILD_TEST_MECHANICS    = PASS_3_OF_3
SPLIT_REMERGE_ROUNDTRIP             = PASS_3_OF_3
THREE_HOSTED_REPOSITORIES           = NOT_TESTED
PRODUCTION_REPO_TOPOLOGY_SELECTION  = NOT_YET_AUTHORIZED
```

The next empirical comparison, if physical repositories are still considered, should create three temporary hosted repositories from the same role-root commit and compare CI/release/integration overhead against the monorepo baseline. No production topology decision should be promoted from this fixture alone.
