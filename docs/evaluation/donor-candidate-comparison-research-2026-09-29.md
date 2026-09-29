# Donor candidate comparison research — 2026-09-29

## Contract

Este registro preserva a pesquisa metodológica e a evidência empírica produzidas durante a avaliação de donors/candidatos do Atento.

Não é uma decisão de seleção, não cria um benchmark novo, não substitui `docs/evaluation/harness.md` e não altera o Project Progress.

Responsabilidades:

- preservar o racional para comparar vários candidatos de forma reproduzível;
- separar benchmark externo, teste local, evidência Git e bloqueio de infraestrutura;
- registrar o que já foi empiricamente observado no spike do PsyChat;
- definir uma forma escalável de testar novos candidatos sem mudar o protocolo a cada donor.

Fontes canônicas relacionadas:

- metodologia AtentoEval: `docs/evaluation/harness.md`;
- decisão fork/donor/native: `docs/adr/ADR-000-fork-vs-greenfield.md`;
- provenance/licenças: `docs/third-party.md`;
- progresso global: `roadmap.md`.

Snapshot de referência:

- Atento `main`: `0983f502d2884f24c52d400c09131449ec59ae8c`;
- PsyChat donor: `wink-wink-wink555/PsyChat@5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`;
- PsyChat evidence branch: `spike/psychat-fork-eval@620c998332848d8100ecae51ca6180e64f28713e`.

---

## 1. Research question

A pergunta de engenharia não é:

> qual projeto possui mais funcionalidades?

A pergunta é:

> qual candidato consegue cumprir a responsabilidade de um bloco do Atento com qualidade, safety e custo aceitáveis, preservando um chassi que permita trocar provider, executor, donor ou capability com change-surface pequeno e mensurável?

Isso exige avaliar duas dimensões diferentes:

```text
feature / behavioral quality
            +
architecture / evolvability
```

Uma dimensão não compensa automaticamente a outra.

---

## 2. Evidence classes

Toda comparação deve classificar evidência antes de usá-la em uma ADR.

| Status | Significado |
|---|---|
| `PASS_EMPIRICAL` | observado por Git/API/content evidence ou probe executado |
| `PASS_STATIC` | verificado diretamente em código/Git, sem afirmar comportamento runtime |
| `PENDING_EXECUTION` | probe existe, mas ainda não foi executado em ambiente funcional |
| `INFRA_BLOCKED` | infraestrutura falhou antes de o teste executar |
| `QUALITY_RISK` | incerteza de qualidade/capability; não é defeito de chassi por si só |
| `ARCH_RISK` | risco de arquitetura/lifecycle ainda não resolvido |
| `NOT_DECIDED` | evidência insuficiente para decisão |

Regra:

```text
INFRA_BLOCKED != TEST_FAILURE
PASS_STATIC != RUNTIME_PASS
UPSTREAM_PAPER_SCORE != ATENTO_PRODUCT_PASS
```

---

## 3. Benchmark basis

O Atento não deve produzir uma média global misturando benchmarks incompatíveis.

Cada benchmark fornece evidência para um eixo específico e deve permanecer separado no report.

| Eixo | Fonte | Uso no Atento |
|---|---|---|
| support strategy | ESConv | strategy labels, support behavior, negative patterns |
| longitudinal counseling | PsychEval | continuidade multi-session, goals, memória longitudinal |
| need-aware memory | ENPMR-Bench | inferência de necessidade e seleção de memória |
| tool use | TEA-Bench | need detection, selection, process trace, grounding, failure behavior |
| broad mental-health behavior | MentalHealthBench | acuity, context seeking, agency, practical guidance |
| expert/adversarial | CounselBench | expert rubric, failure modes, judge disagreement |
| patient-style robustness | PATIENT-Ψ | slices reserved/evasive e outros estilos de comunicação |
| multi-turn safety | MHSafeEval | harm category × counselor role × severity |
| evolvability | Atento Chassis Fitness | boundaries, replaceability, state ownership, safety separation |

Primary references:

- ESConv: https://aclanthology.org/2021.acl-long.269/
- PsychEval: https://aclanthology.org/2026.findings-acl.1115/
- ENPMR-Bench: https://aclanthology.org/2026.findings-acl.2080/
- TEA-Bench: https://aclanthology.org/2026.acl-long.2152/
- MentalHealthBench: https://openai.com/index/introducing-mentalhealthbench/
- CounselBench: https://github.com/llm-eval-mental-health/CounselBench
- PATIENT-Ψ: https://github.com/ruiyiw/patient-psi
- MHSafeEval: https://github.com/suhyun565/MHSafeEval

A lista de provenance e termos aplicáveis permanece em `docs/third-party.md`.

---

## 4. Multi-candidate experiment design

### 4.1 Candidate identity

Cada candidato deve ser definido por dados reproduzíveis, não apenas por nome.

Manifest mínimo:

```yaml
candidate_id:
block:
source_id:
repository:
upstream_sha:
variant: UPSTREAM | WRAPPED | FORKED | NATIVE | MODEL_ADAPTER
adapter_id:
atento_sha:
case_set_hash:
policy_hash:
provider_config:
external_terms_note:
```

Sem `repository + upstream_sha`, o resultado não é elegível para comparação de decisão.

### 4.2 Variants

Quando fizer sentido, um donor pode ser medido em variantes diferentes:

```text
UPSTREAM
  projeto intacto

WRAPPED
  upstream preservado atrás dos contratos/chassi do Atento

FORKED
  donor com patches internos explícitos

NATIVE
  implementação do bloco no Atento
```

Essas variantes respondem perguntas diferentes:

- `UPSTREAM` mede o comportamento e a arquitetura original;
- `WRAPPED` mede quanto o chassi consegue absorver sem alterar internals;
- `FORKED` mede o custo e o benefício de introduzir seams dentro do donor;
- `NATIVE` fornece uma alternativa sem dívida herdada do donor.

Não é obrigatório executar todas as variantes se uma delas já for tecnicamente inviável e a evidência estiver registrada.

### 4.3 Same-contract rule

Para comparar candidatos do mesmo bloco, todos devem expor o mesmo contrato Atento.

Exemplo conceitual para BLOCO I:

```text
RagRequest
   ↓
RagExecutor
   ↓
RagResult
```

Implementações possíveis:

```text
PsyChatRagExecutor
CandidateXRagExecutor
NativeRagExecutor
```

O harness avalia o contrato do bloco e o trace, não os internals particulares do donor.

---

## 5. Git as empirical measurement infrastructure

Git deve medir change-surface, preservação e substituibilidade; não apenas armazenar código.

### 5.1 Recommended Git metrics

Registrar:

```text
baseline_sha
candidate_sha

files_added
files_modified
files_deleted

donor_internal_files_modified
donor_original_lines
donor_original_lines_retained
donor_original_lines_replaced

files_touched_to_add_capability
files_touched_to_swap_executor
files_touched_to_swap_provider
```

Interpretar número de arquivos junto com concentração de diff.

Um resultado como `4 files touched` não é suficiente se um único arquivo foi quase totalmente reescrito.

### 5.2 Mutation-style architecture tests

A evolvabilidade deve ser testada através de mudanças deliberadas.

#### Swap executor

Trocar um executor já registrado por outro.

PASS esperado:

- nenhuma edição de Router;
- nenhuma edição de Planner;
- nenhuma edição de Safety;
- nenhuma edição de API/session;
- mudança limitada a configuração/registro quando aplicável.

#### Add capability

Adicionar uma nova capability.

PASS esperado:

```text
novo executor/adapter
+ novo schema quando necessário
+ registro
+ evals
```

e poucas ou zero alterações em componentes centrais existentes.

#### Swap provider

Trocar o provider através do Model Gateway.

PASS esperado:

- domínio/RAG/Planner não precisam conhecer o provider;
- credenciais e retries permanecem no boundary;
- donor não volta a chamar provider diretamente.

#### Session isolation

Executar sessões independentes contra o mesmo conjunto de recursos long-lived.

PASS esperado:

- estado de uma sessão não aparece em outra;
- restart/reconstruction não mistura ownership;
- shared resources não implicam shared mutable conversation state.

---

## 6. Git/GitHub execution model

### 6.1 Local parallelism with worktrees

`git worktree` permite manter várias árvores de trabalho ligadas ao mesmo repositório e fazer checkout de mais de uma branch simultaneamente.

Uso recomendado para pesquisa paralela:

```text
Atento/
../atento-psychat/
../atento-candidate-x/
../atento-native/
```

Cada worktree continua ligado ao mesmo repositório Git, evitando checkout/stash constante durante comparação concorrente.

Official reference:

- https://git-scm.com/docs/git-worktree

### 6.2 Donor checkout by pinned SHA

Durante qualificação, preferir checkout efêmero de donor por `repo + SHA` em vez de vendorizá-lo antecipadamente no Atento.

Layout de job:

```text
workspace/
├── atento/
└── donor/
```

O `actions/checkout` suporta múltiplos repositórios lado a lado e checkout por `ref`.

Reference:

- https://github.com/actions/checkout/blob/main/README.md

### 6.3 One workflow, matrix of candidates

Um mesmo workflow deve executar o mesmo protocolo em várias configurações através de matrix strategy.

Conceito:

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - id: psychat_upstream
        variant: UPSTREAM
      - id: psychat_wrapped
        variant: WRAPPED
      - id: atento_native
        variant: NATIVE
```

Isso reduz o risco de criar um workflow favorável a um candidato e outro protocolo para o concorrente.

Reference:

- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations

### 6.4 Results as artifacts

Cada matrix job deve emitir um result manifest versionado.

Exemplo:

```json
{
  "candidate_id": "psychat_wrapped",
  "block": "I",
  "upstream_sha": "5bf6f806...",
  "atento_sha": "...",
  "case_set_hash": "...",
  "chassis": {},
  "rag": {},
  "safety": {},
  "latency": {},
  "cost": {},
  "git_surface": {}
}
```

Artifacts preservam test output e permitem um job agregador comparar resultados sem transformar o log da CI em banco de evidência.

Reference:

- https://docs.github.com/en/actions/concepts/workflows-and-actions/workflow-artifacts

---

## 7. Why not submodules/vendor all candidates during qualification

Submodule ou vendoring podem fazer sentido depois que um upstream se torna dependência persistente.

Durante seleção, eles introduzem custo desnecessário:

- poluem a árvore canônica;
- confundem código em avaliação com código adotado;
- tornam provenance/diff mais difícil;
- podem induzir agentes a tratar o donor como decisão já tomada.

Durante qualificação, preferir:

```text
candidate registry
+ pinned repo/SHA
+ ephemeral checkout
+ result artifacts
```

Depois da decisão, o adoption mode define se o código será:

- fork externo;
- subtree/vendor;
- package/dependency;
- model adapter;
- selective port;
- Atento-native.

---

## 8. Empirical PsyChat evidence

Esta seção resume somente evidência já registrada no branch de avaliação.

Fonte detalhada:

- `spike/psychat-fork-eval@620c998332848d8100ecae51ca6180e64f28713e`
- `evals/spikes/psychat/evidence-matrix.md`
- `evals/spikes/psychat/forkability-baseline.md`
- `evals/spikes/psychat/static-baseline.md`

### 8.1 Upstream chassis

Pinned PsyChat static CFS:

```text
10/100
```

No screening estático inicial, apenas o routing boundary passou.

Esse resultado mede compatibility/adaptation gap para o chassi Atento; não mede qualidade terapêutica ou qualidade RAG.

### 8.2 Explicit extension seams

Forkability baseline:

```text
explicit extension seams = 0/5
```

O upstream não oferece explicitamente, sem donor edit:

- injectable LLM dependency;
- injectable vector store/embedding dependency;
- injectable agent dependency;
- external web-session ownership;
- structured route protocol.

O donor também constrói `PsychologyAgent()` e `VectorStore()` internamente.

Conclusão restrita:

> um wrapper externo puro, com zero donor edits, não é uma estratégia de chassi forte para o RAG do PsyChat.

Isso não rejeita um fork pequeno.

### 8.3 Fork/change surface

Provider/lifecycle boundary empiricamente medido:

```text
3 donor files
```

- `agent/psychology_agent.py`
- `core/rag_system.py`
- `core/vector_store.py`

A correção completa da responsabilidade atual de BLOCO I adiciona:

- `data/processor.py`

Total da surface atual:

```text
4 donor files
```

No snapshot Git v0.19 registrado na evidence matrix:

```text
original lines: 1600
retained:       1410
retention:      88.125%
```

Esse percentual é descritivo, não um threshold de aceitação.

### 8.4 Provider boundary

Na preserved patched RAG surface:

```text
direct requests.post = 0
```

Model e embedding gateways foram introduzidos nos arquivos já tocados pelo fork.

Execução runtime completa desse patch continua pendente enquanto a infraestrutura de Actions não fornece runner funcional.

### 8.5 Corpus provenance defect

O parser upstream foi aplicado ao corpus pinado.

Resultado registrado:

```text
unique corpus IDs: 4,760
IDs lost by upstream chunking: 4,760 / 4,760
```

O problema ocorre porque o ID do registro precede o delimitador de diálogo usado pelo parser e não é carregado para os chunks.

A correção no processor preserva:

```text
4,760 / 4,760 IDs
unknown chunk IDs: 0
```

Isso é evidência de correctness/provenance do BLOCO I, não de qualidade semântica do retrieval.

### 8.6 Vector metric semantics

No upstream pinado não foi observada configuração explícita de `hnsw:space`, enquanto o donor transforma distance em similarity através de `1 - distance`.

O patch de BLOCO I configura cosine distance explicitamente, alinhando:

```text
1 - cosine_distance
```

com uma interpretação de cosine similarity.

### 8.7 CI infrastructure status

A evidence matrix mantém GitHub Actions separado de resultado funcional.

O smoke workflow de infraestrutura e o workflow de BLOCO I observaram jobs terminando antes de steps serem alocados, com `steps=null` e sem logs materializados.

Classificação:

```text
INFRA_BLOCKED
```

Não classificar como:

```text
PsyChat test failure
Atento test failure
runtime regression
```

### 8.8 What remains unproven

Ainda não existe evidência suficiente para afirmar:

- full patched donor runtime PASS;
- dynamic provider replacement PASS;
- real multi-session isolation PASS;
- pt-BR retrieval quality against Chinese gold evidence;
- ADR-000 winner.

Portanto:

```text
ADR-000 = NOT_DECIDED
Project Progress = unchanged by this research record
```

---

## 9. Candidate comparison output

O report comparativo não deve emitir um único score vencedor.

Formato recomendado:

| Axis | Candidate A | Candidate B | Native |
|---|---:|---:|---:|
| CFS / architecture fitness | | | |
| behavioral benchmark | | | |
| safety blocking defects | | | |
| RAG/tool/memory metric for block | | | |
| p50/p95 latency | | | |
| cost | | | |
| donor files modified | | | |
| original-line retention | | | |
| swap-provider surface | | | |
| swap-executor surface | | | |
| add-capability surface | | | |
| runtime blockers | | | |

A ADR interpreta trade-offs; o harness não deve esconder dimensões incompatíveis em uma média.

---

## 10. Candidate runner direction

A generalização tecnicamente defensável do spike atual é:

```text
candidate registry
        ↓
pinned checkout
        ↓
block contract adapter
        ↓
same AtentoEval cases
        ↓
same safety gates
        ↓
same chassis probes
        ↓
Git change-surface measurement
        ↓
result artifact
        ↓
comparison report
        ↓
ADR evidence
```

O runner deve aceitar novos candidatos principalmente por configuração + adapter.

Se cada donor novo exigir reescrever o harness central, o próprio mecanismo de avaliação está acoplado demais.

---

## 11. Decision implications

Esta pesquisa suporta as seguintes regras metodológicas, sem selecionar candidato:

1. comparar candidatos por BLOCO e contrato comum;
2. pinçar `repo + SHA`;
3. manter benchmark axes separados;
4. executar local deltas que o benchmark externo não cobre;
5. medir change-surface por Git;
6. diferenciar `UPSTREAM`, `WRAPPED`, `FORKED` e `NATIVE`;
7. usar worktrees para paralelismo local quando necessário;
8. usar matrix jobs para executar o mesmo protocolo na CI;
9. persistir result manifests/artifacts;
10. não tratar `INFRA_BLOCKED` como resultado do candidato;
11. não vendorizar/mergear todos os donors no repo antes da decisão;
12. manter ADR-000 aberta até runtime + quality + safety + architecture evidence serem suficientes.

Nenhuma dessas regras altera o score global do projeto por si só.
