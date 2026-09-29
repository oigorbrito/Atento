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

## Preserved Git evidence v3

Baseline:
`f2317be0fc27b1f4a6a39c5c89f22faf550045bf`

Corrected/versioned patch:
`da07c84c9ed6ae979b04bbf8d6091c7a64f90762`

Preserving ref:
`evidence/psychat-rag-block-correctness-v3`

Git compare remains exactly **4 donor files**:

1. `agent/psychology_agent.py`
2. `core/rag_system.py`
3. `core/vector_store.py`
4. `data/processor.py`

Change surface:

- original lines: **1,600**
- deleted/replaced original lines: **146**
- retained original lines: **1,454**
- approximate retained-original-line ratio: **90.88%**

The index-versioning correction does not add another donor file.

## Evidence status

PASS_EMPIRICAL:
- four-file Git change surface;
- QA-ID corpus replay;
- preserved gold IDs;
- versioned patch snapshot.

PASS_STATIC:
- cosine metric declaration;
- versioned collection naming;
- index-schema metadata.

PENDING_EXECUTION:
- Chroma runtime creation of the versioned collection;
- full patched donor compile/runtime;
- provider swap, session isolation, retrieval mechanics and AtentoEval execution.

The GitHub Actions runner failure remains an infrastructure blocker and is not a
test failure.
