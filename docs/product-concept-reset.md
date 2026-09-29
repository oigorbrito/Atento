# Atento — alinhamento conceitual do produto

> Status: alinhamento provisório, 2026-09-29.
>
> Este documento registra o norte conceitual enquanto as três partes do Atento ainda estão sendo reconstruídas com o usuário. Ele não apaga evidência técnica existente e não seleciona uma implementação-base.

## 1. Origem da ideia

A Nayá foi a ideia inicial de uma assistente pessoal no estilo de experiências como Zapia.

A Nayá deve ser tratada aqui como **referência de ideia e de produto**, não como referência obrigatória de projeto, código ou arquitetura.

O projeto Atento não deve inferir que precisa preservar a implementação histórica da Nayá só porque ela veio primeiro.

## 2. Mudança de direção: agente persistente

Durante a evolução da ideia surgiu a categoria de **agente/assistente persistente**.

O Grok Bot foi citado como referência conceitual dessa categoria. Nas pesquisas apareceu o **OpenMausBot** como uma implementação pública conceitualmente próxima e com uma superfície de produto significativamente mais madura que a implementação inicial da Nayá.

Isso levou à inversão estratégica:

```text
não:
OpenMausBot dentro da Nayá

avaliar:
chassis persistente maduro
        +
diferenciais/ideias da Nayá
        +
features úteis de outros donors
```

O objetivo é evitar reconstruir do zero capacidades que uma base madura já tenha resolvido melhor.

## 3. Papel atual do OpenMausBot

O OpenMausBot é o **primeiro anchor candidate conhecido** para a Parte 1 do Atento.

Ele não está automaticamente selecionado.

A evidência já coletada sobre o OpenMausBot deve ser preservada, mas a decisão de base precisa ser refeita dentro de uma comparação mais ampla e homogênea com outros projetos da mesma categoria.

Maturidade aparente, volume de desenvolvimento e atividade do projeto são sinais úteis para descoberta, mas não substituem auditoria de arquitetura, execução, testes e benchmarks.

## 4. Parte 1 do Atento — Assistente Persistente

O Atento possui três partes principais. **Somente a Parte 1 está definida neste documento.** As Partes 2 e 3 serão registradas depois do alinhamento com o usuário.

A Parte 1 é uma **assistente pessoal persistente**.

O alvo de produto é aproximar, na medida tecnicamente e financeiramente possível, o conjunto relevante de capacidades das referências de produto citadas pelo usuário — incluindo Grok Bot, Zapia e projetos "primos" descobertos durante a pesquisa — sem limitar a arquitetura a um único donor.

"100% das funcionalidades" deve ser interpretado como **meta de cobertura funcional/paridade de capacidade a ser inventariada e medida**, não como afirmação de que essa paridade já existe.

A comparação de chassis deve considerar pelo menos:

- persistência real de estado, contexto, tarefas e rotinas;
- continuidade após restart/interrupção;
- automações e execução em background;
- mensagens e canais;
- uso de computador, browser e aplicativos;
- integrações e ferramentas;
- memória pessoal;
- troca/roteamento de modelos e providers;
- arquitetura e boundaries;
- modularidade e acoplamento;
- extensibilidade e facilidade de incorporar novas features;
- superfície de adaptação/fork;
- observabilidade, testes e evidência de execução;
- segurança e autoridade sobre efeitos externos;
- custo operacional;
- capacidade de evolução no curto, médio e longo prazo.

## 5. Pesquisa de candidatos

A próxima pesquisa da Parte 1 não deve começar assumindo que a lista atual de candidatos está completa.

O processo correto é:

```text
definir a categoria
→ enumerar projetos maduros comparáveis
→ localizar benchmarks/evidência existente
→ auditar arquitetura e implementação
→ comparar sob os mesmos critérios
→ medir apenas deltas relevantes ao Atento
→ selecionar ou rejeitar o chassis
```

Projetos já presentes no repositório, incluindo OpenClaw, só permanecem como finalistas se sua inclusão puder ser justificada por esse protocolo. Evidência técnica já coletada não deve ser descartada, mas também não deve transformar um candidato em privilegiado por inércia histórica.

## 6. Licença durante descoberta

Licença **não é critério eliminatório da pesquisa técnica inicial**.

Um projeto pode ser estudado e comparado mesmo que seus termos inviabilizem posteriormente determinado modo de distribuição ou incorporação.

Ainda assim, provenance e termos legais continuam obrigatórios. A decisão de copiar, portar, fazer fork, redistribuir ou publicar código precisa respeitar os termos aplicáveis ao artefato concreto.

Portanto:

```text
TECHNICAL_CANDIDATE
!=
LEGAL_ADOPTION_CLEARED
```

## 7. Relação com a documentação existente

Este registro não apaga ADRs, avaliações ou pesquisas anteriores.

Até que as três partes do Atento estejam conceitualmente reconciliadas:

- a documentação anterior deve ser tratada como evidência e histórico;
- decomposições antigas do produto não devem ser assumidas como definitivas apenas porque já foram documentadas;
- a seleção da base da Parte 1 deve voltar à pergunta original: **qual chassis de assistente persistente é a melhor fundação para absorver os diferenciais da Nayá e as melhores capacidades dos projetos comparáveis?**
- nenhuma base está selecionada.

```text
PART_1 = PERSISTENT_PERSONAL_ASSISTANT
OPENMAUSBOT = INITIAL_ANCHOR_CANDIDATE
BASE_WINNER = NOT_SELECTED
PART_2 = PENDING_ALIGNMENT
PART_3 = PENDING_ALIGNMENT
```
