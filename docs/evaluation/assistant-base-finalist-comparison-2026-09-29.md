# Assistant base finalists — decision-frontier comparison — 2026-09-29

## Contract

This document applies the ADR-002 decision protocol to the three remaining Assistant-base finalists:

- OpenMausBot;
- NaIA;
- OpenClaw.

It is a decision-frontier record, not the final selection.

The question remains:

> Which functioning system reaches the target Assistant with the smallest structural change while preserving the greatest amount of already-proven capability?

The comparison distinguishes:

```text
LOCALIZED_REPAIR
vs
CROSS_CUTTING_STRUCTURAL_REWRITE
vs
EVIDENCE_PENDING
```

and preserves:

```text
PERSISTENCE != DURABLE_EXECUTION
FEATURE_RICH != GOOD_CHASSIS
HARNESS_NOT_RUN != CANDIDATE_FAIL
```

## Pins used

### OpenMausBot

- Original qualification snapshot: `947bef311bf5c3f55d3590849abf0eb329408519`
- Finalist-comparison repin: `56ac27a01a2ceb27d44c3ef0cf8d63f692f68cb8`
- Delta from original qualification: 7 commits.

The reviewed delta is concentrated in ChatGPT-plan authentication/model routing, Cloud onboarding, UI and verification coverage.

Targeted transfer check of authority-adjacent files:

- `src/components/ApprovalModeSelector.tsx`: no focused approval/policy semantic delta found;
- `server/config.ts`: additions are ChatGPT-plan/Codex provider configuration;
- `server/contracts.ts`: additions describe ChatGPT-plan authentication/account metadata;
- `server/index.ts`: no focused authority/durability semantic delta found in the targeted check.

No new evidence was found in this delta for generalized external-effect reconciliation, persistent Nayá authority, or therapeutic-memory isolation.

Therefore the original qualification conclusions remain transferable to the comparison repin.

```text
OPENMAUS_REPIN_TRANSFER = ACCEPTED_STATIC
```

### NaIA

- Qualified/current main snapshot: `23e4ca55abfaf399844047792018a22415ed3738`
- Delta from qualified snapshot to current main: 0 commits.

No repin transfer is required.

### OpenClaw

- Qualification repin: `e9571d77e76bd6d35996273d9e8398ad539b26e1`
- Detailed evidence: `docs/evaluation/openclaw-qualification-2026-09-29.md`

The static qualification is complete. The Atento candidate harness and controlled effect algorithm have partial empirical evidence, while pinned OpenClaw runtime execution remains infrastructure-blocked.

---

## Same-protocol comparison

| Decision property | OpenMausBot | NaIA | OpenClaw |
|---|---|---|---|
| Functioning assistant product | strong | partial / lower composition maturity | strong |
| Persistent assistant state | strong | present, less product-integrated | strong |
| Interrupted-turn/restart recovery | not proven at OpenClaw level | contracts/research; less product integration | strong upstream evidence |
| Background work / routines | strong | modules present | strong |
| Provider/model surface | strong; current delta adds ChatGPT-plan path | strong provider-neutral concepts; less product composition | strong |
| Policy/approval primitives | present, but Nayá authority needs reinforcement | strong fail-closed/explicit authority model | strong primitives; Nayá hardening required |
| Approval persistence / stale-authority defense | provider/delegation authority was observed partly process-local | strong contracts/evidence concepts | persistent approvals + strong stale-authority evidence |
| Durable outbound messaging | partial evidence | messaging ambiguity remains | strong channel-specific evidence |
| Generic arbitrary external-effect durability | not proven | not proven | not proven generally; localized controlled-adapter reconciliation is feasible |
| Core memory/persona separation | personal/shared concepts need Nayá boundary reinforcement | strong sensitive-memory/consent concepts, lower product integration | strong per-agent core state; plugin stores require scope review |
| Strict Assistant ↔ Therapist boundary | requires Atento-enforced boundary beyond native memory concepts | authority concepts useful, but product composition remains higher-cost | separate Gateway/runtime required; compatible with ADR-001 topology |
| Product adaptation | product-rich base; authority reinforcement required | higher integration/build surface | low/moderate product adaptation + moderate hardening |
| Universal durability retrofit | cross-cutting if required | cross-cutting if required | cross-cutting if required |
| Critical-tool durability via controlled adapters | not yet demonstrated | operation/idempotency concepts exist; product proof absent | algorithm subprobe passed; plugin/runtime validation pending |
| License/provenance for direct product-base adoption | Apache-2.0 core; separate terms under `enterprise/` | root license not detected at qualified revision | MIT |
| Current runtime-local delta status | prior qualification transferable after targeted repin review | qualified snapshot current | OC-NAYA runtime portion infrastructure-blocked |
| Final selection | not selected | not selected | not selected |

## Gap classification

### OpenMausBot

Likely localized or bounded:

- current provider/model adaptation;
- product UX integration;
- some Nayá-specific policy wrappers.

Material/cross-cutting or unresolved:

- persistent Nayá authority model if process-local permission behavior remains authoritative;
- generic external-effect reconciliation;
- strong Therapist-memory boundary;
- interrupted-turn recovery equivalence remains unproven.

```text
OPENMAUS_PRODUCT_GAP       = LOW
OPENMAUS_AUTHORITY_GAP     = MATERIAL
OPENMAUS_GENERIC_EFFECT    = NOT_PROVEN
OPENMAUS_RECOVERY_DELTA    = EVIDENCE_GAP
```

### NaIA

Likely localized or reusable:

- policy/approval contracts;
- audit/evidence model;
- sensitive-memory consent;
- provider-neutral ports;
- durability fault contracts.

Material/cross-cutting for use as the full Assistant base:

- composition of messaging, automations, personal memory, web execution and mature end-user/auth surfaces;
- productization/integration across modules;
- direct-adoption provenance remains unresolved because a root license was not detected.

```text
NAIA_AUTHORITY_GAP         = LOW
NAIA_PRODUCT_GAP           = MATERIAL
NAIA_GENERIC_EFFECT        = NOT_PROVEN
NAIA_DIRECT_ADOPTION_TERMS = BLOCKED / UNRESOLVED
```

### OpenClaw

Likely localized or bounded:

- Nayá fail-closed hardening profile;
- tool/session/agent visibility restrictions;
- plugin allowlisting;
- separate Assistant/Therapist deployment topology;
- critical high-risk adapters with explicit operation/readback/reconciliation contracts.

Material/cross-cutting only if Nayá requires a universal exactly-once contract across arbitrary third-party tools.

Still execution-pending:

- pinned-runtime validation of OC-NAYA-001/003/004/005;
- OpenClaw plugin validation for the controlled durable-effect adapter.

```text
OPENCLAW_PRODUCT_GAP       = LOW
OPENCLAW_AUTHORITY_GAP     = MODERATE_HARDENING
OPENCLAW_GENERIC_EFFECT    = NOT_PROVEN
OPENCLAW_LOCAL_DELTAS      = PARTIAL / INFRA_BLOCKED
```

---

## Decision frontier

The evidence narrows the unresolved Assistant-base decision.

NaIA remains highly valuable as the authority/evidence architecture donor, but choosing it as the complete Assistant chassis still implies a materially larger product-composition surface and unresolved direct-adoption terms.

The direct product-base frontier therefore remains between the two product-rich systems:

```text
OpenMausBot
vs
OpenClaw
```

This is not a winner declaration.

The current discriminator is not feature count. It is whether OpenClaw's strong upstream restart/authority/isolation mechanisms actually survive the Nayá hardening profile at the pinned runtime with low donor touchpoint cost.

### Evidence that can still change the decision

The following remaining evidence is material enough to change the base decision:

1. `OC-NAYA-001` — effective fail-closed policy at runtime and after fresh-process reinspection;
2. `OC-NAYA-003` — session/agent isolation under the qualification profile while preserving the separate-Gateway Therapist boundary;
3. `OC-NAYA-004` — representative plugin/memory store isolation;
4. `OC-NAYA-005` — OpenClaw plugin validation and empirical donor-core touchpoint count.

`OC-NAYA-002` no longer asks whether OpenClaw magically provides generic exactly-once behavior: it does not. The remaining adoption question is whether critical Nayá writes can be constrained to controlled adapters. The exact controlled-adapter crash algorithm already passed its isolated fault probe.

If the four pinned-runtime checks above pass without donor-core modification, the comparison will have materially stronger evidence that Nayá-specific hardening is bounded rather than structural.

If they fail in ways that require broad OpenClaw core changes, the change-surface comparison must be reopened against OpenMausBot.

---

## Current decision state

```yaml
assistant_base_winner: NOT_SELECTED
decision_frontier:
  - OpenMausBot
  - OpenClaw
naia:
  role: architectural-authority-evidence-donor
  base_candidate: higher-build-cost
openmausbot:
  comparison_pin: 56ac27a01a2ceb27d44c3ef0cf8d63f692f68cb8
  repin_transfer: ACCEPTED_STATIC
openclaw:
  qualification_pin: e9571d77e76bd6d35996273d9e8398ad539b26e1
  static_qualification: COMPLETE
  controlled_effect_algorithm: PASS_EMPIRICAL
  pinned_runtime_local_deltas: INFRA_BLOCKED
next_decision_gate: resolve-openclaw-pinned-runtime-deltas
```

No Project Point is earned by this comparison.
