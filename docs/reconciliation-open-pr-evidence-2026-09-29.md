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
- OpenClaw probe artifacts and historical runner: preserved at PR #17 head `d62626d03685b55ee9110b98c707e797465d4f60`; deliberately excluded from active `main` during pre-merge cleanup.
- Exact legacy Anna/Therapist-specific artifact not promoted; it remains traceable at PR #17 head `d62626d03685b55ee9110b98c707e797465d4f60`.
- Old shortlist ordering and execution priority: superseded.

Current state remains:

```text
NAIA_BASE = NOT_SELECTED
OPENCLAW_SHORTLIST = NOT_SELECTED
ANNA = SEPARATE_DOMAIN
```


## PRs #1–#10 — PsyChat / Anna

**Disposition:** `CLOSE_AFTER_RECONCILIATION`

These PRs are historical Anna/PsyChat evidence. They do not define the current Anna chassis.

Primary spike:
- #1 head `8f14cb1599e106596b0f311596a21d52beea26d0`
- PsyChat case sets and the larger experimental adapter/probe tree remain traceable at immutable PR #1 head `8f14cb1599e106596b0f311596a21d52beea26d0`; candidate-specific executable evidence was deliberately excluded from active `main` during pre-merge cleanup.

Evidence sequence:
- #2 `a6c5c38c5a020ecaaba281c4b1f11c0e6fbe0428`
- #3 `afdae6b10d28515cb466ba97fd49969c94de6e78`
- #4 `a309475e8578c888f36e16bbd95dbb22a15cf52a`
- #5 `bdb21f9a7581ac5c5aac78b4b94ccef0aac186e0`
- #6 `75707879a8ced08e1f5e48af517156b6c4a414e5`
- #7 `ac8b7ce2a5fe9a6540c4702f3358cddbb3a766f9`
- #8 `da07c84c9ed6ae979b04bbf8d6091c7a64f90762`
- #9 `f74be929b056db8d7cb1035c4de9512a5796cdc9`
- #10 `7eb5d516f5b5d6491ad6babbed4e00018b690aa6`

PRs #9 and #10 contain identical final blobs for the four principal source files:
- psychology agent: `e0284eee8ee2790a48a85946781e4a4a3a3d6085`
- RAG system: `8240d29b9870b86e5773e427e92e62747b01fe21`
- vector store: `a6b1690d9ecbbb799b3227006d1644aa547c5ef6`
- data processor: `22f9d362bad10a2238e9e638929799308d8478f1`

#9 is the preferred historical source snapshot because it also includes the license in its PR surface.

Current interpretation:

```text
PSYCHAT_EVIDENCE = PRESERVED
PSYCHAT_BASE_FOR_ANNA = NOT_SELECTED
PSYCHAT_SHORTLIST = NOT_SELECTED
OLD_BLOCK_CENTRIC_DECISIONS = SUPERSEDED
ANNA_ROLE = EMOTIONAL_THERAPEUTIC_DOMAIN
```


## Pre-merge executable-artifact cleanup

Candidate-specific historical executables are not part of the active reset architecture.

Removed from the PR before merge:
- historical PsyChat workflow from active `.github/workflows/`;
- PsyChat historical case sets that were only needed for the closed spike line;
- OpenClaw hardening fixtures, controlled-effect plugin and historical qualification runner.

Preservation rule:

```text
EVIDENCE_PRESERVED_AT_IMMUTABLE_PR_HEAD
!=
EXECUTABLE_ARTIFACT_MERGED_TO_MAIN
```

The generic candidate registry, generic candidate-evidence workflow, AtentoEval agent-scope machinery and decision-reset guards remain active.
