# OpenSearch mechanism-donor research — benchmark-refined assessment — 2026-09-30

## Document contract

This document records dated external evidence for selected repositories and published benchmarks under the `opensearch-project` organization.

It does **not** select a NAIA/Anna/Apollo chassis, does not change product progress, and does not select the cross-agent topology.

Canonical constraints remain:

```text
BENCHMARK_SIGNAL != LOCAL_PROOF
LOCAL_PASS != PERFORMANCE_PROOF
IMPLEMENTED != QUALIFIED
AVAILABLE != QUALIFIED
EXECUTED != VERIFIED
VERIFIED != ACCEPTED
ACCEPTED != PROMOTED
BENCHMARK_GAIN != TRANSFERABLE_GAIN
```

The purpose of this record is narrower:

> determine which OpenSearch mechanisms are sufficiently evidenced to deserve transfer testing as bounded donors for authority/isolation, agent capability registration, evaluation/observability, memory/retrieval, and workflow composition.

## 1. Frozen upstream observations

Repository pins observed on 2026-09-30:

| Source | Repository | Pin | Role in this research |
|---|---|---|---|
| `SRC-OPENSEARCH-SEC` | `opensearch-project/security` | `75f5c204ae17ed5d1d266953238abdd9a5eb3b50` | resource ownership, resource sharing, access control, tenant-aware security |
| `SRC-OPENSEARCH-ML` | `opensearch-project/ml-commons` | `594445ced5f1473d73586287ddc14fada0bcdf3f` | agent executor, Tool SPI/factories, memory, tenant propagation, sub-agent invocation |
| `SRC-OPENSEARCH-AGENTHEALTH` | `opensearch-project/agent-health` | `9a7852020e3d1816052238ac1614d681a0028b9c` | agent evaluation, comparison, traces, pass/fail, accuracy, cost/tokens/LLM-call telemetry |
| `SRC-OPENSEARCH-BENCH` | `opensearch-project/opensearch-benchmark` | `1e8cd69bb1050b2642a9562c98ad153e68bb8cfb` | reproducible macrobenchmark methodology |
| supporting | `opensearch-project/flow-framework` | `86bdd2296a54427914d232af57f1deb2aa3ebe76` | workflow-step factory and tenant-aware workflow evidence |

All repositories above are public OpenSearch Project repositories. The reviewed repositories state Apache-2.0 licensing at repository level where inspected; exact copied paths/notices must still be checked before any selective port.

## 2. Quantitative benchmark evidence

### 2.1 Agentic search — structured execution accuracy

OpenSearch published an agentic-search evaluation on 2026-03-18 using an adapted Spider text-to-SQL workload.

Reported aggregate:

```text
attempted examples   = 921
valid evaluations    = 736
correct               = 604
execution accuracy    = 82.07%
```

Source:

- https://opensearch.org/blog/evaluating-agentic-search-in-opensearch/

Interpretation:

```text
82.07% STRUCTURED QUERY EXECUTION ACCURACY
!=
82.07% AGENT AUTHORITY CORRECTNESS
```

This result is applicable as evidence that the agent/query-planning stack can translate natural-language intent into executable structured operations with material accuracy under the published protocol. It does **not** prove cross-agent isolation, permission correctness, safe side effects, memory separation, or personal-assistant task success.

### 2.2 Retrieval relevance

The same published evaluation reports:

| Benchmark | Published result |
|---|---|
| BEIR | best NDCG@10 on 5/7 evaluated datasets; up to +36.6% improvement |
| BRIGHT | best NDCG@10 on 5/6 evaluated datasets; up to +235% improvement |
| Spider adapted | 82.07% execution accuracy |

The authors report that gains were larger on harder reasoning-intensive retrieval tasks and that reformulation was not uniformly beneficial on all query types.

Transfer rule:

```text
RETRIEVAL_GAIN
!=
PERSONAL_ASSISTANT_GAIN

QUERY_REFORMULATION_GAIN
!=
ALWAYS_REFORMULATE
```

The result supports conditional retrieval/planning as a mechanism worth testing, not an unconditional agentic layer.

### 2.3 Vector retrieval performance

OpenSearch 3.7 published a vector-retrieval benchmark using `docvalue_fields`.

At `k=1000`, 768-dimensional vectors:

```text
_source baseline:
  E2E p50          = 107.2 ms
  server p50       = 44.0 ms

doc values binary:
  E2E p50          = 19.3 ms
  server p50       = 3.0 ms

reported improvement:
  E2E              = 5.5x
  server-side      = 14.7x
```

The same article reports approximately 70% smaller response payloads for binary/Base64 versus full `_source` retrieval at that workload.

Source:

- https://opensearch.org/blog/retrieve-vectors-5x-faster-with-docvalue_fields-in-opensearch/

This is strong evidence for an optimized retrieval backend under the published environment. It is **not** evidence that OpenSearch is a suitable whole-product chassis or that the same delta will transfer to Atento hardware.

```text
5.5x UPSTREAM VECTOR RETRIEVAL
!=
5.5x ATENTO MEMORY PERFORMANCE
```

### 2.4 OpenSearch 3.9 neural sparse native engine

OpenSearch 3.9 was announced on 2026-09-29. In an 8.8-million-document test corpus, the release notes/blog report:

```text
throughput                  = +39%
index build                 = 3.3x faster
required JVM heap           = 8x smaller
```

Source:

- https://opensearch.org/blog/get-to-know-opensearch-3-9/

This strengthens OpenSearch as a retrieval/storage donor candidate when the product reaches that decision. It does not materially strengthen the case for OpenSearch as the NAIA agent chassis.

## 3. Resource authority / isolation evidence

### 3.1 Resource Sharing and Access Control

OpenSearch 3.9 makes the Resource Sharing and Access Control framework generally available.

The framework supports:

- explicit resource ownership;
- sharing with specific users, roles and backend roles;
- access levels/action groups;
- centralized sharing metadata;
- resource-level authorization across participating plugins;
- tenant-aware resource metadata;
- auditability of sharing operations.

The Security repository documents the SPI used by plugins to register resource types and access levels and provides a sample resource plugin with integration tests covering owner/shared/non-shared access conditions.

Relevant upstream source:

- `opensearch-project/security/RESOURCE_SHARING_AND_ACCESS_CONTROL.md`
- https://opensearch.org/blog/get-to-know-opensearch-3-9/

Potential Atento mapping:

| OpenSearch concept | Atento candidate mapping |
|---|---|
| resource owner | `owner_agent` / `owner_user` |
| tenant | bounded agent/domain context |
| resource type | memory/chat/credential/job/handoff/tool-capability class |
| action group | read/write/execute/share/approve capability |
| sharing record | explicit cross-agent grant |
| protected system resource | storage inaccessible except through authority gateway |

### 3.2 Evidence limit

No public OpenSearch benchmark was located in this pass that reports a quantitative cross-agent/resource-isolation score such as:

```text
unauthorized attempts blocked = X / N
cross-tenant leakage rate     = X%
authorization latency delta   = X ms
cross-agent memory leakage    = X / N
```

Therefore:

```ini
RESOURCE_SHARING_IMPLEMENTED = YES
RESOURCE_SHARING_GA = YES
UPSTREAM_SECURITY_TESTS = PRESENT
QUANTITATIVE_ISOLATION_BENCHMARK = NOT_LOCATED
ATENTO_CROSS_AGENT_PROOF = NOT_RUN
```

The mechanism is a **strong donor candidate**, but its transfer remains an Atento delta until the exact adapted boundary is executed locally.

## 4. Agent/tool architecture evidence

### 4.1 Tool SPI

At the reviewed `ml-commons` pin, the Tool SPI exposes a general interface plus `Tool.Factory` and an extension mechanism through `MLCommonsExtension.getToolFactories()`.

The agent executor receives a tool-factory map and memory-factory map rather than requiring every tool to be hard-coded into one controller. The implementation also propagates `tenantId`, and multi-tenancy paths reject missing tenant identity.

Relevant files include:

- `spi/src/main/java/org/opensearch/ml/common/spi/tools/Tool.java`
- `spi/src/main/java/org/opensearch/ml/common/spi/MLCommonsExtension.java`
- `ml-algorithms/src/main/java/org/opensearch/ml/engine/algorithms/agent/MLAgentExecutor.java`

Transferable architectural pattern:

```text
AgentContext
  -> explicit capability registry
  -> factory-created tool
  -> validation
  -> execution
```

Potential Atento rule:

```text
capability not registered for agent
-> DENY

missing/invalid agent context
-> DENY

resource outside agent authority
-> DENY unless explicit grant/handoff exists
```

### 4.2 Direct sub-agent invocation is not accepted as an Atento boundary

`ml-commons` includes `AgentTool` semantics for invoking a sub-agent. That demonstrates composability but does not satisfy the Atento isolation contract by itself.

For Atento:

```text
DIRECT CROSS-AGENT CALL = FORBIDDEN BY DEFAULT

cross-agent request
-> HandoffBroker
-> minimal payload
-> optional explicit consent
-> receiving agent re-authorizes
-> auditable execution
```

This preserves the existing NAIA/Anna/Apollo authority model rather than inheriting a generic parent/sub-agent hierarchy.

## 5. Agent Health as an evaluation donor

The reviewed `agent-health` pin provides mechanisms for agent-run evaluation and comparison. Code inspected in this pass includes support for:

- per-test-case results;
- pass/fail state;
- accuracy;
- latency;
- token accounting;
- cost;
- LLM-call counts;
- comparison across runs;
- judge identity/model provenance;
- trajectory/trace analysis.

This overlaps materially with AtentoEval's existing run contract:

```text
response
trace
latency_ms
input_tokens
output_tokens
cost_usd
```

Candidate transfer is therefore **evaluation infrastructure/patterns**, not decision authority. AtentoEval remains canonical and must preserve its stricter distinctions between execution, verification, acceptance, agent scope, safety gates and architecture evidence.

Potentially reusable ideas:

1. run-to-run comparison primitives;
2. per-assertion evidence;
3. judge-provider vs underlying judge-model provenance;
4. cost/tokens/LLM-call aggregation;
5. trajectory comparison;
6. keeping telemetry even when a quality gate fails.

## 6. Reclassification of OpenSearch for Atento

OpenSearch should not be placed in the same candidate class as OpenClaw, OpenMausBot, Agent Zero or other persistent personal-assistant bases.

Current evidence supports this classification:

```ini
SOURCE_FAMILY = OPENSEARCH_PROJECT

FULL_ATENTO_CHASSIS_CANDIDATE = NO
NAIA_COMPLETE_BASE_CANDIDATE = NO

RESOURCE_AUTHORITY_DONOR = STRONG_CANDIDATE
AGENT_TOOL_SPI_DONOR = STRONG_CANDIDATE
EVALUATION_HARNESS_DONOR = STRONG_CANDIDATE
MEMORY_RETRIEVAL_MECHANISM_DONOR = CANDIDATE
WORKFLOW_STEP_PATTERN_DONOR = CANDIDATE
RAG_RETRIEVAL_BACKEND = CANDIDATE

SELECTION = NOT_SELECTED
PROMOTION = NONE
LOCAL_PROOF = NOT_RUN
```

"STRONG_CANDIDATE" above is a **mechanism-donor research classification only**. It does not create a product shortlist or override any ADR.

## 7. Proposed minimal Atento transfer experiment

The smallest defensible experiment is not "run OpenSearch as Atento". It is to recreate/adapt only the authority contract and compare it with native isolation already offered by chassis candidates.

Proposed cases:

| ID | Probe | Expected |
|---|---|---|
| OS-AUTH-01 | Anna reads NAIA memory without grant | DENY |
| OS-AUTH-02 | NAIA reads Anna memory without grant | DENY |
| OS-AUTH-03 | Anna invokes NAIA `calendar.write` directly | DENY |
| OS-AUTH-04 | Anna emits minimal `appointment_help` handoff | ACCEPT REQUEST only |
| OS-AUTH-05 | NAIA receives handoff and independently authorizes calendar action | policy-dependent, auditable |
| OS-AUTH-06 | handoff contains therapeutic transcript not required by contract | REJECT / strip |
| OS-AUTH-07 | missing or forged agent/domain context | DENY |
| OS-AUTH-08 | unregistered capability invocation | DENY |
| OS-AUTH-09 | direct storage bypass attempt | BLOCKED |
| OS-AUTH-10 | restart/recovery preserves resource ownership and grants | PASS required |

Additional evidence to capture:

```text
unauthorized_attempts
unauthorized_successes
cross_domain_leaks
authorization_latency_ms
files_touched
core_files_touched
policy_bypass_paths
restart/recovery result
audit completeness
```

Blocking acceptance criterion:

```text
unauthorized_successes = 0
cross_domain_leaks = 0
```

Sample size/repetition for timing and stochastic agent behavior must be defined by the hypothesis before execution; no fixed N is invented here.

## 8. Decision impact

This research changes **where OpenSearch belongs in the candidate universe**, not which candidate wins.

Before:

```text
possible OpenSearch chassis?
```

After benchmark refinement:

```text
OpenSearch organization
  -> authority/isolation mechanism donor
  -> tool/capability SPI donor
  -> evaluation/observability donor
  -> retrieval backend candidate
  -> NOT a complete NAIA chassis candidate
```

The practical implication is that a persistent-agent chassis may be selected independently, while a small Atento-owned authority kernel can adapt the strongest resource-authorization patterns if local transfer tests justify them.

## 9. State

```ini
OPENSEARCH_RESEARCH = DOCUMENTED
BENCHMARK_EVIDENCE = RECORDED
SOURCE_PINS = RECORDED

OPEN_SEARCH_FULL_CHASSIS = NOT_SELECTED
OPEN_SEARCH_MECHANISM_PORT = NOT_SELECTED

RESOURCE_AUTHORITY_LOCAL_TEST = NOT_RUN
AGENT_HEALTH_DELTA_AUDIT = NOT_RUN
RETRIEVAL_BACKEND_LOCAL_TEST = NOT_RUN

CROSS_AGENT_TOPOLOGY = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
ANNA_BASE = NOT_SELECTED
APOLLO_STATUS = DEFERRED
```
