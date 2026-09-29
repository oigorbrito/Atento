# PsyChat — Static Chassis Baseline

## Scope

- Donor: `wink-wink-wink555/PsyChat`
- Pinned commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`
- Evaluation type: static architecture screening
- Metric: Chassis Fitness Score (CFS) v0.1
- Project progress impact: none; this is evidence for ADR-000, not a completed production block.

## Result

> **Static Chassis Fitness: 10/100**

This score measures compatibility with the Atento long-term chassis requirements. It is **not** a conversational-quality score.

| Fitness function | Result | Evidence |
|---|---|---|
| routing_boundary | PASS | routing/analysis lives in `agent/psychology_agent.py`; orchestration/generation lives in `core/rag_system.py` |
| executor_abstraction | FAIL | no `Executor` or `Adapter` abstraction found |
| capability_registry | FAIL | no capability/executor registry found |
| structured_contracts | FAIL | no Pydantic/BaseModel/dataclass/TypedDict contract layer found |
| output_validation | FAIL | no validator/contract normalization layer found |
| provider_boundary | FAIL | direct `requests.post` calls found in agent, RAG system and vector store |
| state_externalization | FAIL | `conversation_history`, `no_rag_counter` and `last_retrieval_docs` are process-local controller state |
| observability_hooks | FAIL | no logging/tracing framework evidence found in code search |
| resilience_boundary | FAIL | no retry evidence; provider HTTP calls do not show request timeout evidence in the searched code |
| independent_safety_boundary | FAIL | no independent safety/risk/crisis boundary found by code search |

## Raw evidence

### Direct provider coupling

At least three direct HTTP provider call sites are present:

- `agent/psychology_agent.py` — LLM call through `requests.post`;
- `core/rag_system.py` — LLM call through `requests.post`;
- `core/vector_store.py` — embedding call through `requests.post`.

### Global config coupling

`from config import *` is present in at least:

- `agent/psychology_agent.py`;
- `core/rag_system.py`;
- `core/vector_store.py`;
- `core/tts_service.py`;
- `web/interface.py`.

### Process-local session state

`core/rag_system.py` owns:

- `self.conversation_history`;
- `self.no_rag_counter`;
- `self.last_retrieval_docs`.

That makes horizontal scaling, session migration and executor replacement harder without an adapter/refactor.

## Positive evidence

PsyChat is not a monolith in every respect.

It already separates a meaningful decision layer:

```text
PsychologyAgent
  ├── RAG need decision
  ├── topic classification
  └── ReAct query rewrite

RAGSystem
  ├── retrieval execution
  ├── response generation
  └── session state
```

That is why `routing_boundary` passes.

This makes PsyChat a plausible **donor for Agentic RAG**, even though its upstream chassis does not yet satisfy the Atento medium/long-term runtime contract.

## CI execution attempt

Two GitHub Actions runs were started:

- main run `36537718722`;
- spike branch run `36537777020`.

Both failed **before runner allocation**:

- `runner_id = 0`;
- no workflow steps were started;
- no donor command was executed.

Therefore this is an infrastructure failure, **not a PsyChat test failure**. The workflow remains committed and ready to run when a runner is available.

## Current interpretation

The result does **not** reject a fork/full donor.

It says that adopting upstream unchanged would inherit substantial chassis debt.

The next defensible experiment is:

```text
PsyChat upstream
        ↓
thin Atento Adapter
        ├── Model Gateway boundary
        ├── Executor contract
        ├── Capability Registry
        ├── Output Validator
        ├── external Session State
        ├── tracing
        └── independent Safety Gate
        ↓
rerun CFS
        ↓
run conversational AtentoEval
```

The key measurement is whether these boundaries can be added **around** the donor while keeping most of the donor internals intact.

## Next metrics

The adapted-donor test must record:

- `files_touched_to_add_capability`;
- `files_touched_to_swap_executor`;
- `files_touched_to_swap_provider`;
- `direct_provider_bypass_count`;
- `mutable_session_state_count`;
- `chassis_fitness_score`;
- quality/safety/cost/latency deltas.

No decision on ADR-000 should be made from the static score alone.


## Test batch 2 — integration surface audit

### Provider swap surface

Static search on the pinned upstream shows provider configuration/calls spread across multiple core files.

#### LLM provider
- `config.py`
- `agent/psychology_agent.py`
- `core/rag_system.py`

#### Embedding provider
- `config.py`
- `core/vector_store.py`

#### TTS provider
- `config.py`
- `core/tts_service.py`

This confirms that provider replacement is not currently isolated behind a gateway.

**Observed minimum LLM provider change-surface:** 3 files.  
**Observed cross-provider change-surface:** at least 5 implementation/config files.

### Session isolation risk

The web app creates a process-global runtime:

```python
rag_system = RAGSystem()
```

and the chat endpoint calls that shared instance.

Static search found no `session`, `cookie` or `user_id` handling in the repository.

At the same time, `RAGSystem` stores mutable conversation state on the instance:

- `conversation_history`;
- `no_rag_counter`;
- `last_retrieval_docs`;
- style cache cleared by `clear_conversation_history()`.

**Finding:** upstream architecture has a **cross-session isolation risk** in web deployment because mutable conversation state is attached to a global process instance.

This is not recorded as a confirmed privacy leak until a dynamic multi-client test runs, but it is a blocking chassis concern for direct adoption.

### Routing behavior coupling

The upstream decision layer is useful, but policy is mixed with implementation details:

- `PsychologyAgent.analyze_user_input()` selects RAG need and query rewrite;
- `RAGSystem.generate_response()` owns conversation counters and can force retrieval;
- `MAX_NO_RAG_ROUNDS = 3` causes forced retrieval after consecutive non-RAG turns.

That means routing is separated enough to be reusable, but not yet expressed as a capability contract independent from RAG policy.

### Parser / validation finding

The routing LLM is instructed to return:

```text
NO
YES,topic1,topic2
```

and the result is parsed using string splitting.

Fallback behavior includes broad `except` branches, including one that returns `need_rag=True` when classification fails.

**Finding:** the donor does not currently provide a schema-validation boundary. This supports keeping `structured_contracts` and `output_validation` as FAIL in the baseline.

### Revised fork hypothesis

PsyChat remains a plausible donor for the **RAG block**, but the evidence currently argues against adopting its web/session/runtime chassis unchanged.

The next adapted-donor test should preserve the donor's RAG logic while moving these responsibilities outside it:

1. session ownership;
2. provider access;
3. capability registration;
4. structured route contract;
5. output validation;
6. safety gate;
7. tracing/resilience.

The test should measure whether this can be done with a thin wrapper rather than a rewrite.


## Test batch 3 — thin donor bridge

A concrete `PsyChatRagSystemPort` was added to test whether upstream `RAGSystem` can sit behind the Atento Executor boundary without modifying upstream source.

The bridge deliberately creates a fresh donor runtime for each invocation, restores session state before `generate_response()`, and extracts the next state afterward.

This tests an important fork hypothesis:

> Can session ownership move outside PsyChat while preserving its RAG behavior?

The spike has deterministic tests for:

- restoring donor state from external session state;
- extracting the next state after execution;
- preventing accidental donor instance reuse across independent calls.

### Trade-off exposed by the bridge

Per-call donor construction is intentionally conservative for isolation but may be too expensive because upstream construction also owns vector-store/provider resources.

Therefore the bridge is **architecturally useful evidence, not the final runtime design**.

If PsyChat is adopted for BLOCO I, the next design problem is to separate:

```text
long-lived stateless resources
(vector index / clients)
        from
per-session mutable state
(history / counters / retrieval trace)
```

without moving session ownership back into a process-global donor instance.
