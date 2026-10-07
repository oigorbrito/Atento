# Repository topology separability probe — 2026-10-06

## Question

Can Atento defensibly split NAIA, Anna and Apollo into three physical repositories now, or is logical separation inside the monorepo the only topology currently supported by repository evidence?

## Method

Executed `tools/repo_topology_probe.py` against full Git history (`fetch-depth: 0`) on branch `eval/repo-topology-separability`.

The decision rule intentionally uses necessary conditions rather than a preference score:

A physical three-repository split is eligible for an extraction experiment only if **each** role already has:

1. role-specific executable code;
2. an independent build manifest;
3. independent tests;
4. no direct cross-role references in role-specific code.

Missing evidence produces `NOT_PROVEN`. This does not claim that monorepo or multirepo is universally superior.

GitHub Actions run: `37551663915`  
Head: `a30170405a134c0db1eaedd8522f2bac598953e1`  
Workflow conclusion: `success`

## Executed result

| Measure | NAIA | Anna | Apollo |
|---|---:|---:|---:|
| Role-named files | 93 | 2 | 1 |
| Role-named code files | 20 | 0 | 0 |
| Independent build manifests | 0 | 0 | 0 |
| Independent test files | 0 | 0 | 0 |

Repository-wide:

- tracked files: **226**
- shared implementation files: **48**
- direct cross-role references found by the bounded probe: **15**
- total commits inspected: **407**
- commits touching role-named paths: **150**
- commits touching 2+ roles: **1**
- commits touching all 3 roles: **0**
- multi-role ratio among role-touching commits: **0.0067**
- role-touching commits: NAIA **145**, Anna **4**, Apollo **2**

The direct cross-role references are concentrated in NAIA evaluation/configuration artifacts and one Gate-2 test, primarily references to Anna. They are evidence of shared evaluation semantics, not sufficient evidence of runtime coupling by themselves.

## Interpretation boundary

The very low historical co-change ratio **cannot** be used as proof that three repositories are independently maintainable. Anna and Apollo currently have almost no role-specific executable surface in this repository, so the history is strongly maturity-skewed toward NAIA.

Likewise, the absence of independent manifests/tests is not evidence that physical separation would fail. It means physical separability has not yet been demonstrated.

## Decision

```text
LOGICAL_BOUNDED_CONTEXTS_IN_ONE_REPO = TESTABLE_NOW
PHYSICAL_THREE_REPO_SPLIT             = NOT_PROVEN
MERGE_AFTER_INDEPENDENT_DEVELOPMENT   = NOT_TESTED
```

The defensible next topology experiment is therefore **logical separation first inside the existing repository**: explicit NAIA/Anna/Apollo project roots, explicit shared/host contracts, independent manifests/tests, and forbidden untyped cross-role imports. Re-run this probe after those boundaries exist.

Only then is an extraction experiment to three physical repositories comparable: copy each already-independent logical project without changing behavior, run its own build/tests, then run the shared integration suite. A physical split should not be promoted before that matched experiment exists.

## Artifact

The raw machine-readable result is produced as:

`artifacts/repo-topology-separability.json`

GitHub Actions artifact name:

`repo-topology-separability`
