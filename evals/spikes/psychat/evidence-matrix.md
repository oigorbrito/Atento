# BLOCO I — RAG Evidence Matrix

This file is the canonical evidence-status ledger for the PsyChat fork/donor
evaluation. It separates architecture/chassis evidence from RAG feature-quality
evidence and from execution infrastructure.

Pinned donor:

- repository: `wink-wink-wink555/PsyChat`
- commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

Atento evaluation branch:

- `spike/psychat-fork-eval`

## Status vocabulary

- **PASS_EMPIRICAL** — observed from Git/API/content evidence or an executed probe.
- **PASS_STATIC** — directly verified from source/Git content, but not runtime.
- **PENDING_EXECUTION** — executable probe exists but current runner cannot execute it.
- **INFRA_BLOCKED** — external execution infrastructure failed before test code ran.
- **QUALITY_RISK** — feature-quality uncertainty that must not be interpreted as a chassis defect.
- **NOT_DECIDED** — evidence is insufficient for ADR-000.

## Evidence

| Area | Metric / question | Status | Current evidence |
|---|---|---|---|
| Upstream chassis | Static CFS | PASS_STATIC | Pinned PsyChat baseline: 10/100; only routing boundary passes static screening. |
| Branch coherence | Spike behind main? | PASS_EMPIRICAL | Spike has repeatedly been reconciled to 0 behind main; compare must be rechecked before final ADR freeze. |
| Donor license | Fork/modification permission known | PASS_EMPIRICAL | Pinned donor `LICENSE` is MIT; modification/distribution/sublicensing are permitted subject to retaining the copyright and permission notice in copies or substantial portions. Versioned evidence: `evals/evidence/psychat_license.json`; the upstream MIT text is also stored alongside copied donor source in both evidence refs. |
| Fork surface | Files touched to introduce model + embedding provider boundaries | PASS_EMPIRICAL | Git compare baseline `fb5368edbe23aeedf571e1f11935ae63b6da29b9` -> patched `15249e687c8a2fdea263cc0ae57650ab698a907f`: exactly 3 files. |
| Fork surface | Provider/lifecycle boundary files | PASS_EMPIRICAL | `agent/psychology_agent.py`, `core/rag_system.py`, `core/vector_store.py`. |
| Fork preservation | Original-line retention over 3-file provider-boundary surface | PASS_EMPIRICAL | Approx. 90.99% retained: 1,242 / 1,365 original lines not deleted/replaced. |
| BLOCO I correctness surface | Files touched for provider/lifecycle + QA provenance correctness | PASS_EMPIRICAL | Git compare baseline `f2317be0fc27b1f4a6a39c5c89f22faf550045bf` -> corrected patched `ac8b7ce2a5fe9a6540c4702f3358cddbb3a766f9`: exactly 4 files, adding `data/processor.py`; preserved ref `evidence/psychat-rag-block-correctness-v2`. The previous processor snapshot used literal `\\n` splitting and is superseded. |
| BLOCO I correctness surface | Original-line retention over 4-file block patch | PASS_EMPIRICAL | Measured patched code commit `afbd41eca44661e174e144e86620fbf611660420`; approx. 91.06% retained: 1,457 / 1,600. Preserving ref now points to license-notice-only descendant `a6c5c38c5a020ecaaba281c4b1f11c0e6fbe0428`; that descendant is excluded from change-surface counting. |
| Provider boundary | Direct `requests.post` in patched RAG surface | PASS_STATIC | 0 in preserved patched ref `evidence/psychat-rag-minimal-patch`. |
| Provider boundary | Model provider injectable | PASS_STATIC | `PsychologyAgent` and `RAGSystem` contain model-gateway seams in preserved patched Git content. |
| Provider boundary | Embedding provider injectable | PASS_STATIC | `VectorStore` and `RAGSystem` contain embedding-gateway seams in preserved patched Git content. |
| Provider boundary | Final-response gateway preserves donor message construction | PASS_STATIC | Audit found the earlier patch replacement removed the local `messages` construction while still passing `messages=messages` to the gateway. `minimal_fork_patch.py` v0.6 now removes only provider HTTP/config blocks, preserves the donor system/history/user message assembly, and asserts `_generate_response` assigns `messages` locally. |
| Provider boundary | Reapply v0.6 patch to pinned donor and execute final response path | PENDING_EXECUTION | Static generator fix is committed, but the current execution environment cannot clone the donor and GitHub Actions remains blocked before runner allocation. Do not promote this regression fix to runtime PASS yet. |
| Provider replacement | Swap provider without donor source edit after boundary | PENDING_EXECUTION | `provider_replacement_probe.py` asserts 0 donor source edits after boundary and tests two model + two embedding gateways. |
| Router authority | Atento can force RAG after selecting `knowledge.rag` | PASS_STATIC | Minimal patch adds `force_retrieval`; bridge now propagates it and fails closed for unpatched donors. |
| Router authority | Runtime propagation through real patched donor | PENDING_EXECUTION | Unit/dynamic probes exist; Actions cannot run. |
| Session isolation | Shared upstream runtime risks cross-session state | PENDING_EXECUTION | Real-source isolation probe exists against pinned `RAGSystem`; not yet executed by a functioning runner. |
| Session lifecycle | Long-lived vector/gateway resources can be shared while session runtime remains isolated | PENDING_EXECUTION | Factory seam and unit probe exist; runtime execution pending. `_style_cache` is now restored/persisted through the external SessionStore so fresh runtimes do not lose the upstream style-analysis optimization. |
| Adapter replaceability | Runtime executor swap touches existing source | PENDING_EXECUTION | Git-backed adapter change-surface probe asserts 0 source edits for switching already-registered executors. |
| Adapter extensibility | Add new capability touches existing chassis | PENDING_EXECUTION | Probe asserts 1 new extension file and 0 existing chassis files. |
| Adapter safety | Independent pre/post safety enforcement | PENDING_EXECUTION | Dynamic chassis probe exists. |
| Adapter validation | Schema validation coverage | PENDING_EXECUTION | Dynamic chassis probe requires 100% of encoded validation checks. |
| Adapter tracing | Required trace coverage | PENDING_EXECUTION | Dynamic chassis probe requires RAG + executor trace events. |
| Retrieval mechanics | Multi-query merge/dedup/ranking preserved after fork patch | PENDING_EXECUTION | Upstream/patched mechanics probes + preservation comparator exist. |
| Vector metric | Upstream distance semantics match `1 - distance` similarity transform | PASS_STATIC | No `hnsw:space` is configured in pinned `VectorStore`; Chroma documents L2 as the default, while donor interprets `1 - distance` as similarity. |
| Vector metric | Patched distance semantics | PASS_STATIC | BLOCO I patch sets `hnsw:space=cosine` in the already-touched `core/vector_store.py`, making `1 - cosine_distance` a cosine-similarity score. |
| Vector metric | Runtime metadata before/after | PENDING_EXECUTION | `vector_metric_probe.py` dynamically records collection metadata upstream vs patched without real Chroma/network access. |
| Dependency reproducibility | Chroma version pinned | QUALITY_RISK | Donor requirement is `chromadb>=0.4.0`, not an exact/locked version; `retrieval_readiness_probe.py` now reports the requirement and whether it is exact. Atento integration environment must own/pin the effective Chroma version before production adoption. |
| QA provenance | Upstream parser preserves corpus IDs in indexed chunks | PASS_EMPIRICAL | No. Applying the pinned parser logic to all 12 corpus blobs yields 30,255 / 30,255 emitted chunks with `qa_id=unknown`; 0 known IDs survive. The corpus contains 4,760 unique record IDs. |
| QA provenance | Corrected parser preserves corpus IDs | PASS_EMPIRICAL | Corrected carry-forward logic over the same 12 pinned blobs emits 30,255 / 30,255 chunks with known `qa_id`, preserves all 4,760 unique record IDs, emits 0 unknown chunks, and retains gold IDs 328/350/1864/1882. |
| QA provenance | Real DataProcessor before/after runtime probe | PENDING_EXECUTION | `qa_id_provenance_probe.py` dynamically loads the actual donor processor and asserts upstream broken vs patched preserved behavior; runner unavailable. |
| Gold provenance | PsyChat gold IDs exist in pinned corpus | PASS_EMPIRICAL | Exact IDs verified: 328 + 350 in `职场.txt`; 1864 + 1882 in `心理学知识.txt`. |
| RAG suite composition | Deterministic AtentoEval RAG case balance | PASS_EMPIRICAL | 20 total: 13 positive, 7 negative, 4 PsyChat gold, 3 contextual, 1 multi-evidence, 1 insufficient-evidence, 1 attempted-empty, 2 explicit user-goal negative controls. |
| Harness plumbing | Route -> Registry -> Executor -> bridge -> trace -> AtentoEval | PENDING_EXECUTION | End-to-end deterministic plumbing probe now includes the real bridge seam and forced-empty retrieval semantics. |
| Retrieval reproducibility | Knowledge corpus committed | PASS_EMPIRICAL | 12 knowledge `.txt` files are present in pinned donor. |
| Retrieval reproducibility | Persisted vector index committed | PASS_EMPIRICAL | No root `storage/` directory is committed at pinned donor commit. |
| Retrieval reproducibility | Embedding config sufficient from Git alone | PASS_EMPIRICAL | `EMBEDDING_MODEL=text-embedding-v4`; committed `ALIBABA_API_KEY` is empty. |
| Retrieval reproducibility | Repository alone reproduces semantic retrieval | QUALITY_RISK | No committed vector index; rebuild requires a functioning embedding provider. |
| Multilingual retrieval | pt-BR query retrieves Chinese gold evidence | QUALITY_RISK | Not yet measured. Paired pt-BR/zh-CN gold manifest exists for IDs 328, 350, 1864, 1882. Alibaba Cloud documentation states `text-embedding-v4` supports 100+ languages including Chinese and Portuguese, but provider capability is not donor retrieval evidence. |
| Multilingual retrieval | Source-language vs pt-BR retrieval gap | PENDING_EXECUTION | `multilingual_retrieval_score.py` reports hit-rate/MRR by language and zh-minus-pt gap once real retrieval results exist. |
| Multilingual retrieval | Low-cost real-evidence benchmark | PENDING_EXECUTION | `multilingual_microbenchmark.py` now uses donor-equivalent 6-utterance chunks (6 chunks for each current gold), explicit cosine similarity, top-k 6 and threshold 0.15; compares pt-BR vs zh-CN without rebuilding the full Chroma index. |
| Multilingual retrieval | Required external dependency for microbenchmark | QUALITY_RISK | Requires a functioning embedding provider credential; workflow records `SKIPPED_NO_EMBEDDING_CREDENTIAL` instead of treating a missing secret as PASS. |
| GitHub Actions | Minimal one-step runner smoke | INFRA_BLOCKED | Smoke run #2: both `ubuntu-latest` and `ubuntu-24.04` fail with `steps=null`; log fetch returns `BlobNotFound`. |
| Main BLOCO I workflow | Test execution | INFRA_BLOCKED | Jobs are created then fail before checkout or any command. No functional failure may be inferred. |
| ADR-000 | Fork/full donor decision | NOT_DECIDED | Architecture evidence improved, but runtime and RAG-quality evidence remain incomplete. |
| Project progress | Global progress | NOT_DECIDED | Remains 3/100; spike evidence alone does not advance project completion. |

## Current interpretation

The evidence supports a narrow architectural statement:

> PsyChat's RAG core can be isolated behind a small, three-file provider/lifecycle
> boundary, but BLOCO I correctness requires a fourth donor file because the
> upstream QA parser loses every corpus record ID during chunking.

It does **not** yet support these stronger claims:

- that the patch compiles/runs in a complete donor environment;
- that provider replacement passes dynamically;
- that real multi-session isolation passes;
- that Portuguese queries retrieve the pinned Chinese gold evidence at acceptable quality;
- that PsyChat should be selected in ADR-000.

## External blocker

GitHub Actions failure is independently reproduced by
`.github/workflows/actions-infra-smoke.yml`, whose only payload is an echo
command across two GitHub-hosted runner labels. Both jobs terminate before steps
are allocated and produce no logs.

This blocker must remain separate from `TEST FAILURE`.
