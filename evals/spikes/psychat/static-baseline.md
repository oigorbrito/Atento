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
