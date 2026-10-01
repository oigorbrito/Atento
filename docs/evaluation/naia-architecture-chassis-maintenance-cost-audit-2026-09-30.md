# NAIA architecture/chassis maintenance-cost audit — 2026-09-30

## Decision question

Architecture and chassis are evaluated as **one candidate-level object**. In this project, architecture is the organization and change structure embodied by the candidate chassis; they are not competing score dimensions.

The selection objective is the candidate that can meet the Atento contract with the lowest defensible **total adaptation and ongoing maintenance cost**. Do not assume a perfect chassis, infer low cost from repository size, or rank architecture separately from the base product.

```text
ARCHITECTURE_AND_CHASSIS = ONE_EVALUATION_OBJECT
SELECTION_PARAMETER = TOTAL_ADAPTATION_AND_MAINTENANCE_COST
PERFECT_CHASSIS_ASSUMPTION = FORBIDDEN
OBSERVED_COST != STATIC_RISK_SIGNAL
```

## Evidence-based interpretation

Empirical work supports treating architecture as a possible major source of maintenance cost, especially where architectural debt and coupling cause changes or defects to propagate. One study evaluated its approach on seven large open-source systems; the five highest architectural debts captured 20–61% of maintenance effort in those systems. This is evidence that architecture can be expensive, not a universal ratio or a comparison proving architecture always costs more than a framework/chassis.

Frameworks and reusable bases also create downstream maintenance through API evolution and integration. A field study monitoring 400 Java libraries/frameworks for 116 days identified client-impacting API changes; developers reported that most observed client impacts required minor migration effort. This establishes a separate cost source, not a universal cost ranking.

Accordingly, measure the combined candidate envelope:

```text
TOTAL_COST_ENVELOPE =
  structural adaptation / cross-cutting change
  + chassis integration and component adaptation
  + dependency and upstream-update friction
  + deployment/topology and operational upkeep
```

Do not collapse these into a precise scalar until the same target capability profile and comparable observations exist.

Sources:
- Xiao et al., “Identifying and quantifying architectural debt,” ICSE Companion 2016, DOI: https://doi.org/10.1145/2884781.2884822
- Brito et al., “Why and How Java Developers Break APIs,” field study of 400 libraries/frameworks: https://arxiv.org/abs/1801.05198
- ISO/IEC 25010:2023 defines a software-product quality model for lifecycle specification, measurement, and evaluation: https://webstore.iec.ch/en/publication/90024

## Common measurement protocol

Capture the following during a real, decision-relevant composition using a frozen candidate pin and the same Atento capability contract:

- files added/copied and existing files modified;
- dependency changes, versions, and transitive update surface;
- configuration-only change versus adapter/component change versus core change;
- number of independent execution/control paths touched;
- runtime/store/service identities required by the role topology;
- whether extension/application is idempotent;
- upstream update friction when an update is actually exercised;
- one representative messaging/browser/provider path actually used;
- engineering wall time and failed/rework attempts;
- model calls, tokens, and monetary cost when applicable and observable.

Classify evidence as:
- `OBSERVED`: collected from an executed composition/update;
- `PARTIAL_STATIC_MEASUREMENT`: exact source/payload touchpoints counted, but no full Atento composition or lifecycle observed;
- `STATIC_STRUCTURAL_SIGNAL`: exact-pin architecture/change boundary found, but effort and upkeep not measured;
- `NOT_MEASURED`: no decision-relevant cost evidence found.

Do not treat CI test counts, a passing adapter test, or a blocked checkout as maintenance-cost measurements.

## Candidate review

Gate 1 statically screened all 26 frozen candidates. It identified one complete-base stop (SelfAgent) and 25 advances. This is structural screening, not a comparative cost measurement.

| Candidate | Existing architecture/chassis cost evidence | Cost-evidence status |
|---|---|---|
| OpenClaw | Separate runtime/Gateway authority domains are a viable route; hardening is described as bounded. No composition cost captured. | STATIC_STRUCTURAL_SIGNAL |
| OpenMausBot | Product chassis and exact-pin verification exist; same-owner role composition remains unresolved. No adaptation diff/time captured. | STATIC_STRUCTURAL_SIGNAL |
| QwenPaw | Per-agent state/policy exist; sandbox fallback and cron defaults need hardening. No profile cost captured. | STATIC_STRUCTURAL_SIGNAL |
| AI Butler | Per-bank memory, fail-closed shell, credential broker, and scheduler are usable seams; target role/bank composition unexecuted. | STATIC_STRUCTURAL_SIGNAL |
| NanoClaw | Exact static touchpoint counts exist for representative recipes (below); real Atento recipe and lifecycle cost are not observed. | PARTIAL_STATIC_MEASUREMENT |
| TrustClaw | Effective action/sandbox authority depends on Composio/Vercel/provider seams; dependency profile and upkeep not measured. | STATIC_STRUCTURAL_SIGNAL |
| Open Assistant | Role/credential separation and per-action authority imply high hardening; required cross-cutting rewrite is not yet established. No composition cost captured. | STATIC_STRUCTURAL_SIGNAL |
| Suna | Risk policy and role topology remain composition work. No composition cost captured. | STATIC_STRUCTURAL_SIGNAL |
| Letta Code | Unrestricted defaults/shared modes must be constrained; role-separated runtime/memory cost not captured. | STATIC_STRUCTURAL_SIGNAL |
| PersonalJarvis | Credential/runtime role topology remains a composition delta. No adaptation cost captured. | STATIC_STRUCTURAL_SIGNAL |
| Rakazo | Separate Spaces/Private Computers and explicit authority rules are needed; deployment/change cost not captured. | STATIC_STRUCTURAL_SIGNAL |
| Gobii | Role grants and brokered peer path remain; exact-pin failures and test counts are not cost measurements. | STATIC_STRUCTURAL_SIGNAL |
| Octop | Permissive defaults require a hardened profile and role topology. Suite size/pass count is not cost measurement. | STATIC_STRUCTURAL_SIGNAL |
| Agent Zero | Instance-wide plugin/OAuth/host-CUA surfaces need separate authority handling; composition cost not captured. | STATIC_STRUCTURAL_SIGNAL |
| Rome | Provider-native bypass and autoapproval require constraints; profile cost not captured. | STATIC_STRUCTURAL_SIGNAL |
| OpenGrokBot | Browser effects and full-toolset routines require additional mediation; classified high-hardening, but no implementation effort measured. | STATIC_STRUCTURAL_SIGNAL |
| SelfAgent | Exact-pin findings require repairs across central authority, background execution, and scheduler lifecycle: a cross-cutting structural rewrite for the complete-base question. Effort was not timed/count-measured. | STATIC_STRUCTURAL_SIGNAL; STOP_COMPLETE_BASE |
| GoClaw | Strict role separation requires separate memory/runtime/data domains or equivalent; deployment and upkeep cost unmeasured. | STATIC_STRUCTURAL_SIGNAL |
| Nebo | Separate role runtime/data domains and background-authority parity remain; cost unmeasured. | STATIC_STRUCTURAL_SIGNAL |
| AutoMate | Deny-by-default, bounded elevation, and role-memory separation remain; cost unmeasured. | STATIC_STRUCTURAL_SIGNAL |
| AgentOS | Interactive/cron policy and browser boundary need a narrow profile; cost unmeasured. | STATIC_STRUCTURAL_SIGNAL |
| OpenAgentd | Blocking ruleset and role domains are required; high-hardening signal, no implementation cost observed. | STATIC_STRUCTURAL_SIGNAL |
| HubOS | Fail-closed guard, background authority, and brokered role topology remain; high-hardening signal, no implementation cost observed. | STATIC_STRUCTURAL_SIGNAL |
| RustFox | Universal effect mediation and role-separated memory/grants remain; high-hardening signal, no implementation cost observed. | STATIC_STRUCTURAL_SIGNAL |
| Engram | Separate runtime/home/service identities plus browser-effect mediation define the composition surface; candidate-runtime composition is infrastructure-blocked. | STATIC_STRUCTURAL_SIGNAL |
| Holt | Effective authority is owned by an external CLI brain/provider; dependency/update and credential-separation costs unmeasured. | STATIC_STRUCTURAL_SIGNAL |

## Only existing partial quantitative measurement: NanoClaw

The pinned change-surface audit counts representative upstream skill/application touchpoints:

| Profile component | Files copied | Existing import/index touchpoints | Dependencies | Finding |
|---|---:|---:|---:|---|
| WhatsApp channel | 4 | 1 | 4 | Low-to-moderate static surface; stale copied adapter risk on upstream update |
| OneCLI credential gateway | 8 | 1 | 1 SDK | Moderate static surface |
| OpenCode provider | 40 | 5 | 1 SDK plus manifest/build touchpoints | High multi-point static surface |
| Published Ollama skill | Not a defensible count | Multiple manual core edits implied | Profile-dependent | Requires re-derivation against the exact pin |

This is useful partial measurement of adaptation surface, not elapsed maintenance cost, not a complete NAIA profile comparison, and not proof that NanoClaw is cheaper or more expensive overall. Exact-pin registry CI passed, but CI passing does not measure future upkeep.

## Current result

```text
CANDIDATES_SCREENED_FOR_STRUCTURE = 26/26
STRUCTURAL_ADVANCES = 25
STRUCTURAL_COMPLETE_BASE_STOP = [SelfAgent]

FULL_COMPARABLE_TOTAL_COST_MEASUREMENTS = 0/26
PARTIAL_STATIC_CHANGE_SURFACE_MEASUREMENTS = [NanoClaw]
REAL_COMPOSITION_COST_CAPTURE = NOT_OBSERVED
```

The frozen Gate-2 composition attempt failed before checkout or test steps because the executor could not materialize the candidate. That is an environment block and produced no candidate cost evidence. Engram’s adapter-only 8-test pass likewise did not execute the Engram runtime or capture its two-runtime/two-home cost.

Therefore there is **no defensible measured winner on total maintenance cost yet**. The existing evidence supports a structural triage, with SelfAgent stopped at its frozen pin and NanoClaw the only candidate with quantified static touchpoints. The remaining candidates require comparable, profile-frozen composition evidence before a total-cost ordering can be claimed.

## Canonical inputs

- `docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md`
- `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`
- `docs/evaluation/naia-authority-isolation-gate2-screen-2026-09-30.md`
- `docs/evaluation/naia-residual-only-probe-ledger-2026-09-30.md`
- `docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md`
- `docs/evaluation/naia-gate2-empirical-execution-infrastructure-block-2026-09-30.md`
