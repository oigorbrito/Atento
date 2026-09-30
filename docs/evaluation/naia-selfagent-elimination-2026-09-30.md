# NAIA candidate elimination — SelfAgent frozen pin — 2026-09-30

## Decision

Candidate: `oezercet/SelfAgent@c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1`

```text
COMPLETE_NAIA_BASE_CANDIDATE = ELIMINATED_AT_FROZEN_PIN
ELIMINATION_GATE = ARCHITECTURE_GATE_1
REASON = CROSS_CUTTING_STRUCTURAL_REWRITE
DONOR_REFERENCE_STATUS = PRESERVED
RECONSIDERATION = ONLY_AFTER_MATERIAL_UPSTREAM_CHANGE
```

This formalizes the Gate-1 result already recorded in
`docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`.

The elimination is based on the conjunction of exact-pin findings:

- consequential-action confirmation metadata exists but is not consumed by the central execution path;
- scheduled raw shell bypasses the ordinary terminal/registry authority path;
- persisted scheduler state is not wired to startup reload/re-arm;
- strict NAIA/Anna isolation additionally requires separate runtime/store composition.

The first three gaps span the central authority chokepoint, background execution path and scheduler lifecycle. Closing them is not a bounded configuration change or isolated component substitution.

This does not classify SelfAgent as a bad project and does not discard its reusable mechanisms. It only removes this frozen pin from the complete-base funnel.
