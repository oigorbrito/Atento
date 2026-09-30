# Anna candidate completeness audit — 2026-09-29

## Contract

This record closes the **candidate-equivalence / completeness** question for the currently enumerated Anna sources at their pinned revisions.

It does not rank candidates, create a shortlist, select a base, or claim clinical efficacy.

```text
THERAPEUTIC_SOURCE != THERAPEUTIC_BASE
RESEARCH_AGENT != PRODUCT_RUNTIME
PROMPT_SYSTEM != OWNED_AGENT_RUNTIME
RAG_COMPANION != LONGITUDINAL_THERAPEUTIC_CHASSIS
STATIC_SOURCE != RUNTIME_PASS
```

Current decision state remains:

```yaml
ANNA_BASE: NOT_SELECTED
ANNA_SHORTLIST: NOT_SELECTED
candidate_universe_complete: false
```

## 1. Equivalence contract

A `THERAPEUTIC_BASE_CANDIDATE` should expose, at minimum:

1. executable end-to-end counselor/emotional-support flow;
2. longitudinal session/profile/memory ownership;
3. strategy/intervention behavior beyond retrieval-only generation;
4. explicit role/safety boundary or a clearly separable place to integrate it;
5. a runtime/product surface that Atento can operate or wrap;
6. enough source ownership to measure provider/session/privacy adaptation.

A source can still be highly valuable while failing this equivalence gate. Such a source is classified as a donor/toolkit/model/eval source rather than compared head-to-head with complete chassis.

---

## 2. Classification result

| Source | Pinned revision | Executable counseling flow | Longitudinal ownership | Strategy/intervention | Safety/role surface | Runtime/product ownership | Defensible class |
|---|---|---|---|---|---|---|---|
| **PsychAgent** | `469f45ef...` | yes — public multi-session generation + web workspace | explicit memory/planning/profile/session assets | multiple therapy schools, skills and reward-guided trajectory machinery | material gap remains: no independently qualified crisis/safety runtime established by Atento | owns generation/eval/RFT/web runtime surfaces | `THERAPEUTIC_BASE_CANDIDATE` |
| **OpenCouch** | `ac5af6ee...` | yes — FastAPI text runtime + web/TUI | Postgres durable thread/session + three-layer memory | guided exercises + therapeutic-approach prompt/runtime flows | safety classification every turn, crisis flow/audit source surfaces | broad backend/runtime/product surface | `THERAPEUTIC_BASE_CANDIDATE` with **domain-fit audit required** because upstream explicitly scopes itself as emotional-support/wellness, not therapist |
| **TherapyMind** | `bfed3f5be...` | no owned counselor runtime established | profile/draft memory manager exists | compiled prompt system contains roles, phases, theories, safety and session rules | strong prompt/safety specification | implementation is primarily prompt compiler + profile CLI + evaluation scripts; no owned chat/server agent runtime established | `MECHANISM_DONOR` / prompt+memory toolkit |
| **TheraMind** | `416d0a00...` | executable research therapist/patient simulation | file-backed `StrictMemoryManager` and multi-session research state | dual-loop/adaptive therapy selection | no independent product-grade safety/crisis boundary established | 4-agent-file research harness; hard-coded/provider/data assumptions; no product/user runtime | `MECHANISM_DONOR` / research simulation chassis, not comparable product base |
| **PsyChat** | `5bf6f806...` | web conversational prototype exists | conversation history is RAG/runtime state, not a demonstrated longitudinal therapeutic authority model | RAG routing, query rewriting, retrieval/style transfer | no independent safety/crisis subsystem established | small RAG-centric FastAPI prototype | `MECHANISM_DONOR` — Agentic RAG / retrieval / style mechanism |
| **Inner Dialogue** | `ffc9e8f7...` | user can conduct sessions through an external AI host | local profile + dated session files | multiple therapy modalities and session structures | safety protocol + hooks/evals exist | no owned model/session server; package is consumed by Claude/GPT/other host | `MECHANISM_DONOR` / host-dependent therapy toolkit |
| **therapist** (`matteodante/therapist`) | `dd9848fe...` | self-reflection agent/tooling | encrypted/persistent longitudinal state | reflection/intervention semantics | explicit role boundary | upstream explicitly states “not therapy” | `MECHANISM_DONOR / DOMAIN_ADJACENT` |

No class above is a quality score.

---

## 3. Evidence details

### PsychAgent — complete research chassis with product gaps

Primary upstream documentation explicitly describes a research codebase for **multi-session AI psychological counseling**.

At the pin, the repository contains:

- multi-session generation pipelines;
- cross-session memory/planning;
- explicit skill libraries and selection;
- multiple therapeutic schools;
- public counselor/profile/summary prompts;
- runnable web backend/frontend workspace;
- evaluation and RFT pipelines.

The upstream README also states that full paper-scale training assets and the complete post-session skill-evolution pipeline are not present in the snapshot.

Atento already records:

- demo-grade auth/privacy surface;
- no qualified independent crisis/escalation runtime;
- unresolved repository license.

Therefore:

```text
PSYCHAGENT_EQUIVALENCE = THERAPEUTIC_BASE_CANDIDATE
RUNTIME_COMPLETENESS = ESTABLISHED_AT_RESEARCH_PRODUCT_LEVEL
PRODUCT_SAFETY_PRIVACY = REQUIRES_AUDIT
LEGAL_ADOPTION = NOT_CLEARED
PT_BR_TRANSFER = NOT_ESTABLISHED
```

Do not rerun its unchanged multi-session/research architecture evidence. Test only Atento-specific gaps.

### OpenCouch — complete emotional-support product, Anna domain fit unresolved

At pin `ac5af6ee4c9a06b4050c5a912439f343ade2c35c`, upstream explicitly describes:

- FastAPI agent runtime;
- Postgres durable persistence;
- thread/session state across days;
- semantic, episodic and procedural memory;
- safety classification before response;
- crisis specialist flow and durable audit;
- 13 state-tracked guided exercises;
- web chat + text TUI;
- tracing/observability surfaces.

Source tree contains concrete modules for:

- crisis audit/logging;
- guardrails;
- guided exercises;
- therapeutic flows;
- memory extraction/retrieval/reconciliation/policy;
- Postgres runtime/session state;
- ACT/CBT/DBT/interpersonal/motivational/grief/PFA prompt sources.

But upstream also explicitly says:

```text
Not a therapist.
Not a diagnostic tool.
Supportive companion for emotional support, reflection and wellness exercises.
```

Therefore the missing question is **role/domain transfer**, not whether a runtime exists.

```text
OPENCOUCH_EQUIVALENCE = THERAPEUTIC_BASE_CANDIDATE
PRODUCT_RUNTIME = ESTABLISHED_SOURCE
SAFETY_BOUNDARY = ESTABLISHED_SOURCE
ANNA_ROLE_FIT = NOT_ESTABLISHED
PRE_BETA_MATURITY = MATERIAL
PT_BR_TRANSFER = NOT_ESTABLISHED
```

Next probe should ask whether Anna's required therapeutic role can be achieved without violating OpenCouch's safety/product contract or requiring a structural rewrite.

### TherapyMind — prompt architecture donor, not complete chassis

At pin `bfed3f5be61bab262bb00a0f3cc9718c4a965243`, the source tree is centered on:

- `build_prompt.py` compiling modular Markdown into system prompts;
- identity, safety, session-lifecycle, autonomy and theory modules;
- `memory/memory_manager.py` for profile/draft file persistence;
- evaluation scripts and scripted test sessions.

The prompt compiler itself describes its output as a compiled System Prompt. The memory manager is a CLI/profile utility.

No owned interactive counselor runtime/server/model gateway/session executor is established by this source audit.

Therefore:

```text
THERAPYMIND_EQUIVALENCE = MECHANISM_DONOR
USEFUL_SURFACES = [PROMPT_COMPILATION, SAFETY_RULES, SESSION_LIFECYCLE, PROFILE_MEMORY, GREY_ZONE_TESTS]
COMPLETE_ANNA_RUNTIME = NOT_ESTABLISHED
```

This reclassification preserves all prior TherapyMind evidence while preventing a prompt/toolkit package from being compared as if it were a complete product.

### TheraMind — executable research simulation, not product chassis

At pin `416d0a00ecc8c76229512197765dc95be6513de5`, the repository contains only a small research surface:

- `agent/main.py`;
- `agent/initialization.py`;
- `agent/evaluation.py`;
- `agent/memory.py`;
- data-generation scripts.

The code implements therapist and simulated patient agents, multi-session research conversations and a memory manager. It also directly embeds research-provider/data assumptions.

No user-facing product runtime, independent safety subsystem, auth/privacy/session service, or provider abstraction is established.

Therefore:

```text
THERAMIND_EQUIVALENCE = MECHANISM_DONOR
RESEARCH_AGENT_EXECUTABLE = YES
PRODUCT_CHASSIS = NOT_ESTABLISHED
USEFUL_SURFACES = [DUAL_LOOP, THERAPY_SELECTION, STATE_PERCEPTION, MULTI_SESSION_PLANNING]
```

### PsyChat — RAG mechanism donor

At pin `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`, the public source is small and explicitly Agentic-RAG centered.

Observed source/runtime focus:

- RAG need decision + topic classification;
- ReAct-style query rewriting;
- retrieval/context expansion;
- counselor-style extraction;
- RAG-backed response generation;
- FastAPI web prototype.

Existing Atento evidence already showed provider coupling, mutable donor state and adapter/change-surface experiments.

No complete longitudinal therapeutic-memory authority, independent safety/crisis layer or multi-session treatment planning system is established.

Therefore:

```text
PSYCHAT_EQUIVALENCE = MECHANISM_DONOR
USEFUL_SURFACES = [AGENTIC_RAG, QUERY_REWRITE, RETRIEVAL, STYLE_TRANSFER]
COMPLETE_ANNA_RUNTIME = NOT_ESTABLISHED
```

### Inner Dialogue — host-dependent therapeutic toolkit

At pin `ffc9e8f78d0f15a8d720436f92fb6e0887fe7461`, upstream describes a local persistent AI therapist, but the execution model is:

```text
therapy folder + CLAUDE.md/framework files/hooks
        ↓
Claude app / Claude CLI / another AI host
```

The repository contains:

- persistent profile/session file conventions;
- multiple modalities;
- safety protocol/hooks;
- crisis/safety eval cases;
- installer/update/doctor tooling.

It does not establish an owned inference/session server or provider-neutral agent runtime.

Therefore:

```text
INNER_DIALOGUE_EQUIVALENCE = MECHANISM_DONOR
HOST_DEPENDENCE = MATERIAL
USEFUL_SURFACES = [LOCAL_SESSION_MEMORY, MODALITIES, SAFETY_HOOKS, UPDATE_PROTOCOL]
COMPLETE_OWNED_ANNA_RUNTIME = NOT_ESTABLISHED
```

---

## 4. Comparable Anna base set after equivalence audit

From the currently enumerated sources:

```text
THERAPEUTIC_BASE_CANDIDATES:
  - PsychAgent
  - OpenCouch

MECHANISM_DONORS / NON_EQUIVALENT:
  - TherapyMind
  - TheraMind
  - PsyChat
  - Inner Dialogue
  - therapist (domain-adjacent)

MODELS / CHECKPOINTS:
  - SoulChat / PsyDT
  - EmoLLM
  - MindChat

BENCHMARKS / EVAL SOURCES:
  - PsychEval
  - MentalHealthBench
  - CounselBench
  - PATIENT-Ψ
  - MHSafeEval
  - ENPMR-Bench
  - ESConv
  - AgentMental
  - others already in provenance
```

This is **not a shortlist**. It is an equivalence partition.

Candidate discovery remains incomplete; additional complete therapeutic/emotional systems may still enter the comparable set.

---

## 5. Smallest next evidence

Do not run a broad two-way benchmark yet.

### PsychAgent missing material deltas

- independently integrated safety/crisis boundary;
- auth/privacy/session isolation for an Atento deployment;
- provider replaceability/adaptation surface;
- pt-BR transfer;
- legal/adoption terms.

### OpenCouch missing material deltas

- Anna role/domain-fit without defeating upstream safety boundaries;
- pre-beta runtime stability;
- provider replaceability/cost;
- auth/privacy/session isolation under Atento assumptions;
- pt-BR transfer;
- adaptation surface.

### Donor reuse

For TherapyMind, TheraMind, PsyChat and Inner Dialogue, preserve their useful mechanisms and evaluate them **after** a base/runtime decision only when a concrete missing capability justifies porting/adapting them.

```text
DONOR_VALUE != BASE_CANDIDACY
```

## 6. Outcome

```text
CURRENT_ENUMERATED_ANNA_SOURCES = 7
COMPARABLE_THERAPEUTIC_BASE_CANDIDATES = [PsychAgent, OpenCouch]
MECHANISM_OR_DOMAIN_ADJACENT = [TherapyMind, TheraMind, PsyChat, Inner Dialogue, therapist]
ANNA_SHORTLIST = NOT_SELECTED
ANNA_BASE = NOT_SELECTED
CANDIDATE_UNIVERSE_COMPLETE = false
NEXT_BLOCK = TARGETED_PSYCHAGENT_AND_OPENCOUCH_MISSING_DELTA_AUDITS
```
