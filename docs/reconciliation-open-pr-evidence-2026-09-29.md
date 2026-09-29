# Open-PR evidence reconciliation — 2026-09-29

## Contract

This ledger records how pre-reset PRs are reconciled into the current product reset.

Classification:

- `PRESERVE_CANONICAL` — copy/reference evidence in the active reset line.
- `PRESERVE_HISTORICAL` — retain immutable PR/commit evidence without granting current decision authority.
- `ALREADY_PRESERVED` — current reset already contains the material evidence.
- `SUPERSEDED_DECISION` — historical decision/ranking must not control current work.
- `CLOSE_AFTER_RECONCILIATION` — old PR can be closed after the preceding states are satisfied.

Agent ownership labels:

- `NAIA`
- `ANNA`
- `APOLLO`
- `SHARED_INFRA`
- `HISTORICAL_EVIDENCE`

## PR #11 — chassis/evolvability benchmark

**Disposition:** `CLOSE_AFTER_RECONCILIATION`

| Material | Ownership | Disposition |
|---|---|---|
| chassis selection research MD/YAML | SHARED_INFRA / HISTORICAL_EVIDENCE | PRESERVE_CANONICAL |
| Letta scaffold/archive index | SHARED_INFRA / HISTORICAL_EVIDENCE | PRESERVE_CANONICAL |
| raw benchmark package | HISTORICAL_EVIDENCE | PRESERVE_HISTORICAL at PR #11 head `bc2d16be396e92b10ca15b98ccb2f9099058d9ae` |
| Letta `EXECUTABLE_CHASSIS_SELECTED` label | HISTORICAL_EVIDENCE | SUPERSEDED_DECISION; means benchmark scaffold result only |
| candidate pins/provenance | SHARED_INFRA | PRESERVE_CANONICAL in `docs/third-party.md` |
| any implication that Letta is the NAIA base | NAIA | SUPERSEDED_DECISION |

Canonical interpretation:

```text
PR11_EVIDENCE = PRESERVED
LETTA_BENCHMARK_RESULT = HISTORICAL
NAIA_BASE = NOT_SELECTED
```

Closing PR #11 does not delete its evidence. Its immutable head remains a historical evidence location; current decision authority belongs to the reset documents on PR #19.


## PR #17 — OpenClaw evidence

**Disposition:** `CLOSE_AFTER_RECONCILIATION`

- OpenClaw qualification evidence: already preserved in the reset line.
- Former finalist comparison: archived under `docs/evaluation/history/` and non-authoritative.
- OpenClaw probe artifacts and historical runner: preserved under `evals/chassis/openclaw/` and `evals/chassis/openclaw_naya_probe.py`.
- Exact legacy Anna/Therapist-specific artifact not promoted; it remains traceable at PR #17 head `d62626d03685b55ee9110b98c707e797465d4f60`.
- Old shortlist ordering and execution priority: superseded.

Current state remains:

```text
NAIA_BASE = NOT_SELECTED
OPENCLAW_SHORTLIST = NOT_SELECTED
ANNA = SEPARATE_DOMAIN
```
