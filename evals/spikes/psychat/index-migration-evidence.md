# PsyChat BLOCO I — Vector Index Migration Evidence

Pinned donor: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

## Correction

The QA parser evidence remains valid. The source expression
`section.split('\n')` is normal Python newline splitting; the doubled slash
seen in serialized connector output was representation escaping, not a donor
patch defect.

Like-for-like corpus replay over all 12 pinned knowledge files gives:

- raw record IDs: **4,760 unique IDs**;
- emitted chunks: **30,255**;
- upstream: **30,255 / 30,255** chunks have `qa_id=unknown`;
- corrected parser: **30,255 / 30,255** chunks have known `qa_id`;
- corrected parser preserves all **4,760** unique record IDs;
- gold IDs `328`, `350`, `1864`, `1882` all survive.

## Vector index migration

The donor interprets similarity as `1 - distance`. The BLOCO I patch therefore
uses cosine distance.

Chroma documents the collection distance metric as creation-time state; an
existing collection cannot have its distance metric changed in place.

Therefore BLOCO I must not reuse the legacy collection name when switching from
the donor's implicit L2 default to cosine.

Current patch contract:

- `hnsw:space = cosine`;
- `ATENTO_INDEX_SCHEMA_VERSION = rag-cosine-v1`;
- collection name:
  `psychology_knowledge__rag-cosine-v1`;
- metadata:
  `atento:index_schema = rag-cosine-v1`.

This forces a new vector index instead of silently opening an existing L2
collection.

## Preserved Git evidence — reconciled current snapshot

Baseline:
`f2317be0fc27b1f4a6a39c5c89f22faf550045bf`

Current measured patch:
`f9e889817e1e40cf530c56d4582cd5102108bbc2`

Measurement ref:
`evidence/psychat-rag-block-correctness-v5-source`

Preserving ref with upstream MIT notice:
`evidence/psychat-rag-block-correctness-v5`

Git compare remains exactly **4 donor files**:

1. `agent/psychology_agent.py`
2. `core/rag_system.py`
3. `core/vector_store.py`
4. `data/processor.py`

Current measured change surface:

- original lines: **1,600**
- deleted/replaced original lines: **190**
- retained original lines: **1,410**
- approximate retained-original-line ratio: **88.125%**

The later lifecycle/provenance/index corrections still do not add another donor file; they remain concentrated inside the same four-file experimental fork surface.

## Evidence status

PASS_EMPIRICAL:
- four-file Git change surface;
- QA-ID corpus replay;
- preserved gold IDs;
- versioned patch snapshot.

PASS_STATIC:
- cosine metric declaration;
- versioned collection naming;
- index-schema metadata;
- explicit-only generation-GC contract;
- exact Chroma pin in the experimental AtentoEval environment.

PENDING_EXECUTION:
- Chroma runtime creation of the versioned collection;
- full patched donor compile/runtime;
- provider swap, session isolation, retrieval mechanics and AtentoEval execution.

The GitHub Actions runner failure remains an infrastructure blocker and is not a
test failure.


## Generation retention experiment

This section records work already performed in this chat; it is not a production architecture decision.

Atomic promotion intentionally keeps old immutable generations so a promotion does not destructively invalidate the previous active index.

The experimental v0.20 patch adds an explicit maintenance operation:

`prune_inactive_generations()`

Its current contract is:

- never invoked automatically;
- requires `confirm_quiescent=True`;
- active generation is never eligible for deletion;
- a configurable number of previous generations is retained;
- the vector lifecycle probe contains the corresponding runtime assertions.

This converts the previous unbounded-retention design gap into a measurable experimental variant while preserving the four-file donor surface.

Runtime verification remains pending because the runner infrastructure did not execute the probe.

## Dependency reproducibility experiment

The upstream donor declares:

`chromadb>=0.4.0`

That open range was already identified during this chat as a reproducibility risk for vector-index behavior.

For benchmark reproducibility only, AtentoEval now owns:

`evals/spikes/psychat/constraints.txt`

with:

`chromadb==0.5.23`

`retrieval_readiness_probe.py` records the distinction between:

- upstream dependency declaration;
- exact integration/benchmark constraint.

This pin belongs to the experiment environment. It is not a production dependency decision.

## External research already used by this evidence

The following previously researched external facts informed this experiment:

- Chroma collection distance semantics were treated as creation-time index state, so the L2 -> cosine change is modeled as a new versioned index rather than an in-place mutation;
- the donor's `1 - distance` transform motivated explicit cosine semantics in the experimental index;
- Alibaba `text-embedding-v4` multilingual capability was recorded only as provider context, not as proof of PsyChat `pt-BR` retrieval quality.

The multilingual retrieval question remains a separate benchmark and is not resolved by provider documentation.
