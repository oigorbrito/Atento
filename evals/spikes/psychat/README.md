# PsyChat Fork Spike

Branch: `spike/psychat-fork-eval`

Pinned donor:
- repo: https://github.com/wink-wink-wink555/PsyChat
- commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

## Scope

This spike evaluates PsyChat as a donor for **BLOCO I — Knowledge / RAG**. It does not migrate production code and does not award Project Points by itself.

## Test batches

### Upstream baseline
- static Chassis Fitness audit;
- provider/change-surface audit;
- session-isolation audit;
- compile/runtime workflow when CI runner is available.

### Adapted-donor boundary
A thin Atento chassis is placed around a donor port without rewriting donor internals:

```text
Route contract
→ CapabilityRegistry
→ PsyChatExecutorAdapter
→ donor port
→ ResultValidator
→ trace
```

Cross-cutting boundaries in the spike:
- ModelGateway protocol;
- external SessionStore;
- SafetyPolicy;
- timeout/retry wrapper;
- structured trace events.

The adapted boundary is tested with a fake donor port so chassis behavior can be validated independently of external API keys.

## Decision evidence

The fork decision must compare:
- upstream CFS;
- adapted CFS;
- donor code retained;
- files touched to swap executor/provider;
- session isolation;
- safety enforcement;
- conversational/RAG quality when live donor execution is available.

Do not interpret this spike as a production migration.
