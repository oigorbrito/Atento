# OpenClaw Nayá qualification fixtures

This directory contains qualification-only evidence for ADR-002.

It is not production configuration and it does not select the Assistant base.

## Expected local-delta contract

- `OC-NAYA-001`: fail-closed authority profile and stale-approval defenses must pass.
- `OC-NAYA-002`: generic arbitrary-tool exactly-once remains an architecture risk; the controlled adapter must prove crash reconciliation without donor edits.
- `OC-NAYA-003`: Assistant and Therapist profiles must remain independently scoped, with strict deployment requiring separate Gateway/runtime trust boundaries.
- `OC-NAYA-004`: representative memory/plugin isolation checks must pass; future plugin stores still require individual scope review.
- `OC-NAYA-005`: qualification hardening + controlled effect adapter must require zero OpenClaw core edits.

The canonical result is the typed artifact emitted by `.github/workflows/candidate-eval.yml`.
