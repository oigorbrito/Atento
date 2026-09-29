# AGENTS.md — Regras de Engenharia do Atento

Este arquivo define como agentes de código, copilotos e contribuidores automatizados devem trabalhar neste repositório.

O objetivo é manter o Atento **arquiteturalmente defensável, auditável, reproduzível e seguro**.

> Regra central: **não implementar por plausibilidade. Implementar por contrato + provenance + evidência + teste.**

---

## 1. Escopo

Estas regras se aplicam a qualquer alteração em:

- arquitetura;
- prompts;
- modelos;
- memória;
- RAG;
- ferramentas;
- safety;
- schemas;
- benchmarks;
- datasets;
- infraestrutura;
- produto;
- observabilidade;
- avaliação;
- código importado ou adaptado de terceiros.

Elas também se aplicam a spikes, forks, clones e experimentos que possam posteriormente migrar para produção.

---

## 2. Hierarquia de documentos do projeto

Antes de implementar, consultar nesta ordem:

1. **`AGENTS.md`** — regras operacionais e de defensabilidade;
2. **`roadmap.md`** — arquitetura, módulos, fases e provenance;
3. **`docs/adr/`** — decisões arquiteturais aprovadas;
4. **`docs/evaluation/harness.md`** — critérios de avaliação;
5. **`evals/config/`** — benchmarks, sistemas e release gates;
6. **`docs/third-party.md`** — dependências externas, licença e provenance;
7. documentação local do módulo;
8. testes existentes.

Se houver conflito entre documentos, **não escolher silenciosamente**. Abrir ou atualizar ADR.

---

# 3. Regra de defensabilidade

Uma mudança só é considerada **defensável** quando for possível responder claramente:

1. **Por que esse componente existe?**
2. **De onde veio a ideia/algoritmo?**
3. **Qual é o contrato de entrada e saída?**
4. **Qual hipótese ele pretende melhorar?**
5. **Como essa hipótese será testada?**
6. **Qual baseline ele precisa superar?**
7. **Quais riscos ele introduz?**
8. **Como ele falha com segurança?**
9. **Como saberemos se houve regressão?**
10. **Como removeremos ou substituiremos esse componente?**

Se qualquer uma dessas respostas estiver ausente, a feature ainda não está pronta para produção.

---

# 4. Provenance obrigatório

Nenhuma feature relevante deve entrar sem um `SOURCE_ID`.

As fontes canônicas estão registradas em `roadmap.md` e `docs/third-party.md`.

Exemplos:

- `SRC-ATENTO` — arquitetura/engenharia própria;
- `SRC-PA` — PsychAgent;
- `SRC-PSYCHAT` — PsyChat;
- `SRC-CADSS` — CADSS / CPsDD;
- `SRC-UKA` — User-Aware Active Knowledge Acquisition;
- `SRC-SAGE` — SAGE;
- `SRC-TEA` — TEA-Bench;
- `SRC-ENPMR` — ENPMR-Bench;
- `SRC-ESCONV` — ESConv;
- `SRC-MHB` — MentalHealthBench;
- `SRC-COUNSEL` — CounselBench.

Todo módulo relevante deve documentar algo equivalente a:

```text
Module: services/planner

Sources:
  - SRC-CADSS: planner/strategy decomposition
  - SRC-SAGE: strategy-aware retrieval
  - SRC-ESCONV: strategy taxonomy

Implementation:
  - ATENTO clean-room

Validation:
  - AtentoEval/strategy

External code copied:
  - none
```

---

# 5. Não confundir tipos de fonte

O agente deve distinguir:

| Tipo | Pode fazer |
|---|---|
| `IMPLEMENTATION_REFERENCE` | estudar código; copiar/adaptar apenas com licença compatível |
| `ARCHITECTURE_REFERENCE` | reproduzir comportamento clean-room |
| `BENCHMARK_REFERENCE` | usar metodologia/protocolo de avaliação |
| `DATA_REFERENCE` | usar dados somente após revisão de licença/uso |
| `MODEL_REFERENCE` | avaliar modelo/checkpoint isoladamente |
| `ATENTO_NATIVE` | implementação própria com ADR quando necessário |

**Benchmark não é implementação.**  
**Paper não é licença de código.**  
**Código público não significa uso comercial permitido.**  
**Dataset aberto não significa redistribuição irrestrita.**

---

# 6. Regra de fork / clone / selective port

Antes de usar projeto externo como base:

1. executar o gate da seção 2.2 de `roadmap.md`;
2. verificar licença;
3. verificar licença/provenance dos dados;
4. pinçar commit;
5. executar upstream sem alterações;
6. medir baseline;
7. mapear arquitetura externa → contratos Atento;
8. estimar quanto código sobreviverá à adaptação;
9. registrar decisão em `ADR-000-fork-vs-greenfield.md`.

Não fazer fork de produto apenas porque:

- "já funciona";
- "parece parecido";
- "economiza código";
- "é open source";
- "tem benchmark alto".

### Preferência

- valor em poucos módulos → **selective port**;
- valor nos pesos/modelo → **Model Gateway adapter**;
- código sem licença → **clean-room**;
- arquitetura muito incompatível → **clean-room**;
- upstream realmente compatível e útil → **fork**, somente após ADR.

---

# 7. Arquitetura alvo é modular, não multi-agent por obrigação

Não transformar uma função em "agente" sem necessidade.

Evitar:

```text
LLM
↓
LLM
↓
LLM
↓
LLM
```

apenas para chamar isso de multi-agent.

Preferir componentes com contrato explícito:

```text
StateEstimator
  input: conversation
  output: state.json

Planner
  input: state + memory
  output: plan.json

Generator
  input: plan + evidence
  output: candidate_response

Safety
  input: state + candidate
  output: allow | modify | escalate
```

Um novo agente autônomo só entra se:

- tiver responsabilidade distinta;
- tiver estado/contrato claro;
- houver ganho mensurável;
- custo/latência forem justificáveis;
- houver trace e fallback.

---

# 8. Structured outputs antes de parsing textual

Decisões de máquina devem usar schemas.

Não preferir:

```text
"YES, emoção, trabalho"
```

quando pode existir:

```json
{
  "need_rag": true,
  "topics": ["emotion", "work"],
  "confidence": 0.83
}
```

Regras:

- schema versionado;
- validação obrigatória;
- comportamento definido em erro;
- nunca interpretar texto malformado silenciosamente;
- migration quando contrato mudar.

---

# 9. Estado explícito

O sistema deve separar:

- fato observado;
- inferência;
- hipótese;
- confiança;
- memória;
- decisão;
- plano.

Não tratar inferência como fato.

Exemplo:

```json
{
  "observed": {
    "user_said": "estou sobrecarregado"
  },
  "beliefs": [
    {
      "need": "validation",
      "probability": 0.46
    }
  ],
  "decision": {
    "action": "clarify"
  }
}
```

---

# 10. Incerteza deve ser operacional

Se a incerteza muda a decisão, ela precisa existir no schema.

Exemplos:

- perguntar em vez de assumir;
- recuperar memória antes de responder;
- buscar conhecimento;
- não diagnosticar;
- evitar ferramenta desnecessária;
- encaminhar para safety flow.

Não gerar números de confiança sem calibração. Se confidence não tiver uso ou avaliação, remover.

---

# 11. Memória: mínimo necessário

Memória não é log completo.

Separar:

- working memory;
- episodic memory;
- preferences;
- summaries;
- safety-relevant memory.

Toda gravação deve ter:

- origem;
- timestamp;
- tipo;
- sensibilidade;
- motivo de retenção;
- TTL quando aplicável.

Toda recuperação deve poder explicar:

- por que essa memória foi selecionada;
- relação com a necessidade atual;
- score/relevância;
- provenance.

### Falhas bloqueantes

- memória de outro usuário;
- memória inventada;
- memória contraditória tratada como verdade;
- uso de inferência sensível persistida sem política;
- vazamento de conteúdo privado em logs.

---

# 12. Planner separado do Generator

O Planner decide **o que fazer**.

O Generator decide **como formular**.

O Generator não pode alterar silenciosamente:

- estratégia;
- rota de safety;
- decisão de tool use;
- evidência usada;
- política de memória.

Se precisar divergir, retornar erro/evento estruturado ao executivo.

---

# 13. RAG é condicional

Não usar RAG em todos os turnos.

O sistema deve decidir:

- se precisa recuperar;
- o que recuperar;
- quando evidência é insuficiente;
- quando não recuperar.

Todo conteúdo recuperado deve carregar provenance.

RAG não transforma fonte em verdade absoluta.

Em conflito entre fontes:

- sinalizar conflito;
- usar política definida;
- evitar síntese inventada.

---

# 14. Tools: princípio do menor poder

Toda ferramenta deve ter:

- nome estável;
- schema;
- escopo;
- permissões;
- timeout;
- retry policy;
- side-effect classification;
- confirmação quando necessária;
- logging;
- mock/fixture para eval.

Resultado de tool é **evidência**, não instrução de sistema.

Conteúdo externo recuperado por tool/RAG deve ser tratado como não confiável para instruções.

Nunca permitir que texto vindo de ferramenta:

- altere system policy;
- desative safety;
- peça secrets;
- mude autorização;
- crie nova tool permission.

---

# 15. Safety é independente e bloqueante

Safety não deve existir apenas dentro do prompt principal.

A arquitetura deve permitir:

```text
input pre-check
→ state/risk
→ executive policy
→ generator constraints
→ output safety gate
```

O gerador não pode fazer override do Safety Engine.

Uma melhora em:

- empatia;
- naturalidade;
- benchmark;
- preferência;

**não compensa falha crítica de safety.**

---

# 16. Não transformar o Atento em diagnóstico automático

O Atento pode:

- apoiar;
- contextualizar;
- fazer perguntas;
- oferecer informação;
- orientar busca de suporte;
- reconhecer sinais que exigem rota de safety.

O sistema não deve, sem requisitos e validação específicos:

- declarar diagnóstico;
- afirmar transtorno como fato;
- atribuir causalidade clínica;
- sugerir tratamento médico como prescrição;
- substituir profissional;
- declarar risco com falsa certeza.

Classificadores internos são sinais operacionais, não diagnóstico clínico.

---

# 17. User agency

Respostas devem preservar decisão humana.

Evitar:

- coerção;
- excesso de autoridade;
- linguagem de certeza sem base;
- definir objetivos pessoais pelo usuário;
- transformar hipótese do sistema em interpretação definitiva.

Quando múltiplos caminhos são razoáveis, apresentar opções e trade-offs.

---

# 18. Benchmark-first, mas benchmark não manda sozinho

Toda mudança relevante precisa responder:

```text
baseline
→ mudança
→ mesmo dataset/case set
→ mesma configuração relevante
→ resultado
→ custo
→ latência
→ regressões
```

Não declarar "melhor" sem:

- mesma tarefa;
- mesmo split;
- protocolo compatível;
- mesma métrica;
- configuração registrada.

Não misturar scores de benchmarks diferentes em uma média global.

---

# 19. AtentoEval é obrigatório

Mudanças em:

- state;
- belief;
- memory;
- planner;
- RAG;
- tools;
- critic;
- safety;
- model;
- prompt principal;

devem adicionar ou atualizar casos em `evals/`.

No mínimo:

1. caso positivo;
2. caso negativo;
3. regressão conhecida;
4. edge case;
5. safety case se aplicável.

---

# 20. Avaliar processo, não só resposta

Uma resposta pode parecer boa e ainda estar errada arquiteturalmente.

AtentoEval deve observar:

```text
state
belief
memory retrieval
executive decision
plan
RAG
tools
critic
safety
response
```

Exemplos de falhas:

- estratégia errada + resposta eloquente;
- memória errada + resposta plausível;
- tool desnecessária + resposta correta;
- safety bypass + texto cuidadoso;
- RAG irrelevante + conclusão coincidentemente correta.

Essas continuam sendo falhas.

---

# 21. LLM-as-judge não é autoridade única

LLM-as-judge pode ajudar em:

- relevância;
- estilo;
- pairwise preference;
- rubric semântica.

Não pode ser único gate para:

- safety crítico;
- privacy;
- unauthorized actions;
- cross-user memory;
- secrets;
- compliance de schema.

Para esses casos, preferir check determinístico e revisão humana amostrada.

---

# 22. Reprodutibilidade

Toda execução relevante deve registrar:

- git SHA;
- model/provider;
- model revision;
- prompt hash;
- policy hash;
- case set hash;
- judge version;
- temperature;
- seed quando aplicável;
- tool fixtures;
- custo;
- latência.

Se não for reproduzível, não usar como evidência de promoção.

---

# 23. Prompts são código

Prompts devem:

- viver em arquivos versionados;
- possuir ID/versão;
- ter testes;
- ter hash em runs;
- evitar lógica crítica invisível;
- não duplicar policy em múltiplos lugares.

Mudança de prompt principal deve rodar regressão.

---

# 24. Model Gateway obrigatório

Nenhum módulo de domínio deve chamar provider diretamente.

Evitar:

```python
requests.post("https://api.provider.com/...")
```

em módulos de domínio.

Usar o `Model Gateway`.

Objetivos:

- trocar provider;
- medir custo;
- padronizar retries;
- versionar modelos;
- controlar timeout;
- facilitar benchmark.

---

# 25. Nenhum provider é arquitetura

DeepSeek, GPT, Claude, Qwen, Llama, SoulChat, EmoLLM, MindChat etc. são **backends/modelos**, não o Atento.

A arquitetura deve sobreviver à troca de modelo.

Se trocar modelo exige reescrever Executive/Memory/Planner, existe acoplamento incorreto.

---

# 26. Dependência externa: pin + licença + provenance

Ao adicionar dependência externa:

- pin de versão quando possível;
- registrar licença;
- registrar função;
- registrar risco;
- registrar substituto;
- atualizar `docs/third-party.md`.

Código copiado/adaptado precisa registrar:

- repo;
- commit;
- arquivo upstream;
- arquivo Atento;
- licença;
- modificações;
- attribution.

---

# 27. Dados de pesquisa não entram por conveniência

Antes de usar dataset:

- licença;
- finalidade permitida;
- commercial use;
- redistribution;
- sensitive data;
- consent/provenance;
- derived artifact policy.

Se não estiver claro, não incorporar.

É permitido criar caso sintético equivalente para teste interno sem copiar conteúdo protegido.

---

# 28. Privacidade por design

Não logar por padrão:

- conteúdo integral sensível;
- secrets;
- tokens;
- credenciais;
- dados pessoais desnecessários.

Tracing deve preferir:

- IDs;
- hashes;
- categorias;
- métricas;
- versões;
- eventos estruturados.

Quando texto bruto for indispensável para debug, usar ambiente/retenção controlados.

---

# 29. Feature flags e rollback

Mudança de comportamento relevante deve ser:

- versionada;
- observável;
- desativável;
- reversível.

Especialmente:

- novo planner;
- nova memory policy;
- nova safety policy;
- novo model;
- novo RAG;
- nova tool.

Nunca fazer migração irreversível sem rollback documentado.

---

# 30. Complexidade precisa se pagar

Adicionar:

- novo agente;
- novo banco;
- novo modelo;
- nova etapa de LLM;
- novo reranker;
- best-of-N;
- novo vector store;

exige demonstrar ganho.

Se retirar o componente não piora métrica relevante, considerar removê-lo.

---

# 31. Budget de latência e custo

Cada nova chamada de modelo precisa declarar:

- por que existe;
- pode rodar em paralelo?;
- pode usar modelo menor?;
- pode ser condicional?;
- cache é seguro?;
- qual impacto p50/p95?;
- qual custo por turno?

Best-of-N e multi-agent entram somente após benchmark justificar.

---

# 32. Código simples primeiro

Ordem preferida:

```text
heurística simples
→ structured LLM call
→ retrieval
→ critic
→ specialized model
→ learned policy
→ multi-agent
→ reward optimization
```

Pular etapas requer evidência.

---

# 33. Testes obrigatórios por mudança

Para módulo novo:

- unit test;
- contract/schema test;
- failure-path test;
- eval case;
- observability event;
- safety test se aplicável.

Para bug:

- primeiro reproduzir;
- criar regression test;
- corrigir;
- verificar suite.

---

# 34. Erros devem falhar explicitamente

Não fazer:

```python
try:
    ...
except:
    return default
```

em decisões críticas.

Preferir:

- erro tipado;
- fallback explícito;
- trace;
- reason code;
- safe default.

Fallback deve ser testado.

---

# 35. Reason codes

Decisões importantes devem produzir códigos estáveis.

Exemplos:

```text
high_need_uncertainty
memory_relevant
knowledge_required
tool_required_current_fact
safety_high_acuity
safety_ambiguous
insufficient_evidence
provider_timeout
schema_validation_failed
```

Reason code é para observabilidade e avaliação; não é chain-of-thought.

---

# 36. Não persistir chain-of-thought

O Atento não deve depender de armazenamento de raciocínio interno livre.

Persistir apenas artefatos estruturados necessários:

- state;
- beliefs;
- decision;
- plan;
- evidence;
- reason codes;
- safety outcome.

Isso é suficiente para auditabilidade sem exigir raciocínio privado textual.

---

# 37. Pull request / commit defensável

Toda mudança significativa deve responder no PR ou commit:

```text
WHAT
- o que mudou

WHY
- hipótese / problema

SOURCES
- SOURCE_IDs

CONTRACT
- schemas/interfaces afetados

EVAL
- suites executadas
- baseline
- resultado

SAFETY
- riscos
- regressões
- fallback

COST
- impacto estimado/medido

ROLLBACK
- como reverter
```

---

# 38. Critérios de "Done"

Uma feature não está pronta apenas porque compila.

É `DONE` quando:

- [ ] contrato definido;
- [ ] provenance registrado;
- [ ] licença verificada se externo;
- [ ] testes unitários;
- [ ] evals;
- [ ] trace;
- [ ] failure mode;
- [ ] rollback;
- [ ] docs;
- [ ] safety review quando aplicável;
- [ ] custo/latência conhecidos;
- [ ] sem regressão bloqueante.

---

# 39. Mudanças que exigem ADR

Criar/atualizar ADR para:

- fork vs greenfield;
- troca estrutural de storage;
- mudança de schema compartilhado;
- nova política de memória;
- nova política de safety;
- ferramenta com side effect;
- mudança de provider que altera comportamento arquitetural;
- multi-agent;
- fine-tuning de produção;
- learned executive policy;
- persistência de novo tipo de dado sensível;
- mudança de release gate.

---

# 40. Proibições

O agente não deve:

- inventar fonte;
- inventar benchmark;
- inventar licença;
- inventar arquivo upstream;
- afirmar que código foi reproduzido sem ter executado;
- marcar teste como passado sem executar;
- alterar gate para fazer build passar;
- remover safety para melhorar benchmark;
- usar dado de benchmark como treino sem autorização;
- copiar código sem provenance;
- colocar secrets no repo;
- criar dependência silenciosa de provider;
- introduzir diagnóstico clínico como output padrão;
- usar um score agregado para esconder falha crítica;
- fazer refactor arquitetural grande sem ADR/eval.

---

# 41. Quando houver dúvida

A ordem correta é:

```text
parar
→ localizar fonte
→ verificar licença
→ ler contrato
→ consultar ADR
→ criar spike pequeno
→ medir
→ decidir
```

Não:

```text
supor
→ implementar
→ ajustar depois
```

---

# 42. Primeira ação de qualquer agente novo

Antes de escrever código:

1. ler este arquivo;
2. ler `roadmap.md`;
3. ler `docs/adr/ADR-000-fork-vs-greenfield.md`;
4. ler `docs/evaluation/harness.md`;
5. ler `docs/third-party.md`;
6. identificar a fase atual;
7. identificar `SOURCE_IDs`;
8. identificar eval suite correspondente;
9. verificar se há gate/ADR pendente;
10. somente então implementar.

---

## Regra final

**O Atento não deve ser otimizado para parecer sofisticado. Deve ser otimizado para ser justificável.**

Cada decisão relevante precisa poder ser rastreada até:

```text
problema
→ fonte/evidência
→ contrato
→ implementação
→ teste
→ benchmark
→ safety
→ decisão de release
```

Se essa cadeia estiver quebrada, a implementação ainda não é defensável.
