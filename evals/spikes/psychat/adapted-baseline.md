# PsyChat + Atento Chassis — Adapted Baseline

## Scope

- Atento branch: `spike/psychat-fork-eval`
- PsyChat donor: `wink-wink-wink555/PsyChat`
- Pinned donor commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- Block: **BLOCO I — Knowledge / RAG**
- Project Progress impact: **none**. This remains spike evidence.

## Branch coherence

The spike was reconciled with `main` and remains **0 commits behind** the current
project baseline used by this spike:

- `main`: `70e54082b99bb055d2cac672a027432da1cdd02a`
- merge-base: current `main` baseline above;
- PR #1 remains **OPEN / DRAFT**;
- no merge has been performed.

## Upstream chassis baseline

Pinned PsyChat upstream static baseline remains:

> **CFS 10/100**

The only passing upstream static check is `routing_boundary`.

This score measures compatibility with the Atento evolvability chassis, not
conversational quality.

## Adapter boundary

The adapter now contains explicit:

- structured `RouteDecision`, `ExecutionRequest` and `ExecutionResult`;
- `CapabilityRegistry`;
- executor protocol / PsyChat executor adapter;
- output validator;
- external `SessionStore`;
- tracing;
- retry / timeout boundary;
- independent safety boundary;
- Model Gateway protocol;
- RAG trace extraction for AtentoEval.

### State ownership correction

Chassis audit v0.2 distinguishes:

- **ownership**: `self.conversation_history`, `self.no_rag_counter`,
  `self.last_retrieval_docs`;
- **bridge access**: `donor.conversation_history = ...` while restoring externally
  owned state.

Bridge access is no longer counted as local session-state ownership.

The adapter-only static CFS must be regenerated under v0.2 before a new numeric
score is recorded. The previous adapter-only 90/100 value was produced by the
more conservative v0.1 ownership heuristic and is historical, not the current
metric result.

## Real donor API defect found

The original bridge fake returned a string, while pinned PsyChat
`RAGSystem.generate_response()` returns a mapping.

The bridge now:

- accepts the real mapping shape;
- extracts a non-empty `response`;
- fails closed when `success=False`;
- still supports a string response for narrow test doubles;
- restores and extracts:
  - `conversation_history`;
  - `no_rag_counter`;
  - `last_retrieval_docs`.

This is evidence that fake-port tests alone are insufficient for donor adoption.

## Session isolation

`real_isolation_probe.py` loads the pinned donor's actual
`core/rag_system.py`, replacing only external dependencies with deterministic
stubs.

It is designed to prove two separate facts:

1. the upstream web ownership model (one shared `RAGSystem`) carries mutable
   history across conceptual clients;
2. the Atento bridge preserves same-session continuity while isolating a second
   session.

The patched provider/lifecycle probe additionally tests reuse of a long-lived
vector resource across distinct per-session RAG runtimes.

These dynamic probes are committed but **not yet recorded as passed**, because
the current GitHub Actions jobs do not execute steps.

## Minimal BLOCO I fork patch

The canonical patch is:

`evals/spikes/psychat/minimal_fork_patch.py`

It deliberately excludes donor web/TTS chassis and patches only the BLOCO I RAG surface:

- `agent/psychology_agent.py` — inject model gateway;
- `core/vector_store.py` — inject embedding gateway;
- `core/rag_system.py` — inject long-lived dependencies and remove direct LLM
  access;
- `data/processor.py` — preserve the corpus QA ID that precedes each `##`
  dialogue block.

The patch fails closed on donor source drift and requires the pinned clean
worktree.

### Provider cost semantics

Two different costs are measured:

**Boundary introduction cost**

Two Git-measured surfaces are now kept separate.

**Provider/lifecycle boundary**

> **3 donor files**

Independent Git evidence:

- baseline: `fb5368edbe23aeedf571e1f11935ae63b6da29b9`;
- patched: `15249e687c8a2fdea263cc0ae57650ab698a907f`;
- ref: `evidence/psychat-rag-minimal-patch`.

Files:

- `agent/psychology_agent.py`;
- `core/rag_system.py`;
- `core/vector_store.py`.

Approximate original-line retention: **90.99%** (1,242 / 1,365).

**Full BLOCO I RAG correctness surface**

> **4 donor files**

A corpus-provenance defect requires `data/processor.py` in addition to the
three provider/lifecycle files.

Independent Git evidence:

- baseline: `f2317be0fc27b1f4a6a39c5c89f22faf550045bf`;
- patched: `afbd41eca44661e174e144e86620fbf611660420`;
- ref: `evidence/psychat-rag-block-correctness-v2`.

Approximate original-line retention over all four files: **91.06%**
(1,457 / 1,600).

This proves both designed change-surfaces are narrow. It does **not** yet prove
that `minimal_fork_patch.py` executes cleanly against a full cloned worktree;
that executable assertion remains pending runner access.

**Provider swap after boundary**

The patched constructors accept model and embedding gateways by injection.
`provider_replacement_probe.py` verifies that model and embedding providers can
then be replaced by composition only.

Expected donor-source edits for a subsequent provider swap:

> **0 donor files**

Again, this remains pending dynamic execution.

## Change-surface: executor and capability

`adapter_change_surface_probe.py` separates runtime selection from implementation
cost.

### Swap already-registered executor

The Registry resolves executor A, switches to executor B, then rolls back to A.

The probe compares Git status before and after selection.

Target metric:

- `files_touched_to_swap_executor = 0`;
- rollback must pass.

### Introduce a new executor

The Git seam scenario adds one extension implementation file.

Target metrics:

- total files touched: **1 new extension file**;
- existing adapter chassis files touched: **0**.

### Add a new capability

The Git seam scenario adds one new capability implementation file.

Target metrics:

- `files_touched_to_add_capability = 1`;
- existing adapter chassis files touched: **0**.

These change-surface values now also have independent GitHub Git Data evidence,
preserved under dedicated refs:

- registered executor swap:
  - evidence commit `bdb21f9a7581ac5c5aac78b4b94ccef0aac186e0`;
  - ref `evidence/adapter-swap-zero`;
  - compare vs adapter baseline HEAD: **0 changed files**;
- introduce alternate RAG executor:
  - evidence commit `a309475e8578c888f36e16bbd95dbb22a15cf52a`;
  - ref `evidence/adapter-new-executor`;
  - compare: **1 added extension file**, **0 existing chassis files modified**;
- add lookup capability:
  - evidence commit `afdae6b10d28515cb466ba97fd49969c94de6e78`;
  - ref `evidence/adapter-new-capability`;
  - compare: **1 added extension file**, **0 existing chassis files modified**.

The runtime behavior of Registry selection/rollback remains a separate dynamic
assertion; Git evidence proves the source change-surface only.

## Corpus QA-ID provenance defect

Pinned `DataProcessor.split_psychology_qa_pairs()` splits source files on
`##`, but each corpus ID appears in the section immediately *before* the
dialogue section. The function resets `qa_id` for every section instead of
carrying it forward.

Source-level execution of that exact parser logic over all 12 pinned knowledge
blobs gives:

- dialogue sections: **4,760**;
- dialogue sections with known `qa_id`: **0**;
- dialogue sections with `qa_id=unknown`: **4,760 (100%)**.

This means the unpatched vector index cannot preserve source-record identity in
its `qa_id` metadata, including gold IDs 328, 350, 1864 and 1882.

The corrected carry-forward parser logic over the same pinned blobs gives:

- raw unique IDs: **4,760**;
- preserved unique IDs: **4,760**;
- unknown dialogue sections: **0**;
- missing raw IDs: **0**;
- all four current PsyChat gold IDs survive.

`qa_id_provenance_probe.py` is committed to execute the real upstream and
patched `DataProcessor` when a runner becomes available.

## AtentoEval RAG surface

AtentoEval now has deterministic RAG fields:

- `rag_required`;
- `rag_document_ids`.

Metrics now include:

- `rag_route_hit`;
- `rag_retrieval_precision`;
- `rag_retrieval_recall`;
- `rag_retrieval_f1`.

The PsyChat adapter emits a `rag.completed` trace that distinguishes:

- `attempted` — the donor entered the RAG branch;
- `used` — retrieved evidence was actually used;
- `retrieved_ids`;
- `retrieved_count`.

Turn-only donor metadata is removed before state is persisted.

### RAG v0 cases

`evals/cases/rag_v0.jsonl` currently contains **20** synthetic deterministic
cases, including:

- retrieval-positive cases;
- negative controls;
- contextual cases;
- insufficient-evidence behavior;
- four cases mapped to document IDs in the pinned PsyChat corpus.

The four PsyChat-mapped cases pin both:

- `gold_source = SRC-PSYCHAT`;
- `gold_commit = 5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`.

`rag_harness_probe.py` is a **plumbing probe only**. It verifies that fixture
route/retrieval data survives adapter → trace → AtentoEval scoring. It must not
be interpreted as donor quality performance.

Actual PsyChat RAG quality comparison remains pending real execution.

### Cross-language quality risk

The gold-source check is provenance evidence, not retrieval-quality evidence.

Atento RAG cases are `pt-BR`, while direct repository evidence for PsyChat gold
documents (for example IDs `1864` and `1882`) contains Chinese-language
dialogue. `gold_source_probe.py` now records whether each pinned gold target has
CJK text near the matched ID and flags:

- `multilingual_retrieval_required`;
- `cross_language_gold_case_count`;
- `multilingual_retrieval_quality_status`.

Therefore a green chassis/replacement result cannot be used to infer Portuguese
semantic-retrieval quality. That remains a separate feature-quality requirement.

## CI / execution state

Latest observed Actions behavior remains:

- jobs are created;
- jobs finish with conclusion `failure`;
- job `steps` are empty;
- job logs do not exist (log fetch returns `BlobNotFound`);
- no checkout, Python process, donor clone or test command runs.

A separate minimal smoke workflow reproduces the same failure with no project
logic:

- run `36560066468`: one `ubuntu-latest` job, one `echo`, `steps=null`;
- run `36560175098`: matrix with `ubuntu-latest` and `ubuntu-24.04`;
  both jobs fail before steps and have no logs.

This isolates the blocker from PsyChat/AtentoEval workflow complexity and from a
single Ubuntu runner label.

Classification:

> **INFRA FAILURE — hosted runner provisioning/account/repository layer**

The exact administrative cause (for example account/billing/policy/service-side
provisioning) is not exposed by the available repository API. This is neither a
PsyChat functional failure nor a passing test.

The local execution environment also cannot resolve `github.com`, so it cannot
clone the pinned donor as an alternate execution path.

## Block readiness gate

`block_i_readiness_gate.py` now separates:

- versioned Git evidence (change-surface/content invariants);
- dynamic runtime evidence;
- CFS reports;
- deterministic RAG plumbing;
- real semantic/cross-language RAG quality.

It reports `ready_for_adr=true` only when the complete evidence package exists.
It does **not** choose fork vs greenfield.

The normalized real-quality artifact expected by this gate is produced by
`rag_quality_report.py`, which requires actual AtentoEval TurnResults for all
pinned PsyChat gold cases and does not impose an arbitrary quality threshold.

## Current evidence boundary

Defensible now:

- upstream CFS baseline is poor for direct chassis adoption;
- wrapper boundaries materially improve replaceability structure;
- a thin wrapper alone cannot remove upstream provider coupling;
- a minimal RAG-core fork patch can be specified with a narrow three-file
  adaptation surface;
- provider/executor/capability replacement seams are encoded as executable,
  Git-measured probes;
- multi-session isolation, resource lifecycle and AtentoEval RAG plumbing have
  executable probes;
- the RAG test set is materially broader than the original seed cases.

Not yet defensible:

- marking the new dynamic probes PASS;
- recording new adapted/composed CFS numbers;
- claiming actual PsyChat RAG quality, cost or latency;
- concluding ADR-000;
- increasing Project Progress.

## Status

**BLOCO I — RAG: IN_PROGRESS**

The next required evidence is execution of the committed probes against the
pinned donor, followed by actual AtentoEval RAG comparison. If runner execution
remains unavailable, that is an objective external blocker for closing this
spike.

### QA provenance evidence correction

The first preserved `data/processor.py` patch snapshot split sections with the literal sequence `\\n` rather than real line boundaries. It is superseded by `evidence/psychat-rag-block-correctness-v2` at commit `ac8b7ce2a5fe9a6540c4702f3358cddbb3a766f9`, which uses `splitlines()`.

Static corpus replay over all 12 pinned knowledge blobs now compares like-for-like chunk units: upstream emits 30,255/30,255 chunks with `qa_id=unknown`; the corrected logic emits 30,255/30,255 chunks with known IDs, preserving all 4,760 unique record IDs and all four current gold IDs.
