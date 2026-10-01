# NAIA top 5 prioritário — custo combinado de arquitetura/chassi (2026-10-01)

## Decisão de triagem

O usuário definiu como primeira métrica de seleção o custo total de manutenção do objeto combinado **arquitetura + chassi**, incluindo adaptação para o contrato Atento e manutenção subsequente. O objetivo é encontrar a opção de menor custo defensável, não um chassi perfeito.

Com a evidência atual, não há medidas comparáveis suficientes para afirmar que estes cinco são os cinco mais baratos, nem para ordenar uns contra os outros. Este registro define, portanto, o **Top 5 prioritário para a próxima comparação empírica de custo**. Ele é uma coorte de triagem, não um ranking de custo observado, shortlist qualificada ou seleção de `NAIA_BASE`.

## Top 5 prioritário

| Candidato | Sinal atual de custo de arquitetura/chassi | Incerteza que impede dizer “mais barato” |
|---|---|---|
| **OpenClaw** | Chassi de produto maduro; fronteira NAIA pode ser expressa com runtimes/Gateways separados; hardening descrito como delimitado. | Custo real de dois domínios, configuração, operação e atualização não foi medido em composição Atento. |
| **AI Butler** | Seams nativos úteis: memória por bank, shell fail-closed, credential broker e scheduler persistente. | Topologia de papéis/banks/canais e manutenção dessa composição ainda não foram executadas. |
| **NanoClaw** | Isolamento por grupo/container e credential gateway são nativos; é o único com contagem parcial de touchpoints. | Auditoria estática varia de 4 a 40 arquivos copiados conforme perfil; não mede tempo, manutenção contínua, nem uma receita Atento completa. |
| **QwenPaw** | Estado e políticas por agente existem; os principais ajustes apontados são perfil/sandbox e defaults do cron. | O custo da configuração hardened e do ciclo de vida sob composição Atento não foi capturado. |
| **Letta Code** | Identidade/memória persistente, scheduler e seams de permissões oferecem limites reutilizáveis. | Defaults irrestritos, modos compartilhados e custo de separar runtime/memória por papel continuam sem medição comparável. |

A escolha desses cinco é uma **priorização para medir**, baseada em sinais de seams estruturais utilizáveis e escopo de adaptação aparentemente delimitável. “Aparentemente delimitável” é sinal estático, não custo observado. NanoClaw entra também porque tem dados parciais quantificados; isso não significa que seja o mais barato.

## Exclusões e reconciliação

- **SelfAgent** continua parado como candidato de chassi completo no pin avaliado, devido ao reparo transversal de autoridade central, execução em segundo plano e ciclo de vida do scheduler. Não entra no Top 5.
- **Engram** permanece elegível como componente/donor de memória ou arquitetura; não é comparado aqui como chassi integral. Sua composição runtime/home está bloqueada por infraestrutura, e custo integral não foi observado.
- **OpenMausBot** tem bateria upstream extensa e aprovada, mas isso não resolve o custo de adaptação nem a fronteira de isolamento entre papéis do Atento. Não deve entrar no Top 5 apenas pelo volume de testes.
- **Rakazo, Suna, AgentOS, Octop e demais sobreviventes** não foram reprovados; ficam fora desta primeira coorte porque não há base comparável que demonstre custo menor que o dos cinco selecionados para priorização. Podem substituir um integrante se surgir evidência nova e material.

A categoria correta para todos os cinco é **candidatos prioritários para medição**, não “mais baratos medidos”. Os cinco ainda precisam passar pelos gates rígidos de autoridade, isolamento, persistência e segurança.

## Estado da evidência

```text
TOP5 = [OpenClaw, AI Butler, NanoClaw, QwenPaw, Letta Code]
TOP5_ORDERING = NOT_ESTABLISHED
TOP5_BASIS = STATIC_STRUCTURAL_SIGNALS + NanoClaw_PARTIAL_STATIC_MEASUREMENT
FULL_COMPARABLE_TOTAL_COST_MEASUREMENTS = 0/26
OBSERVED_TOTAL_COST_WINNER = NONE
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
CURRENT_PIN_QUALIFIED = 0
```

Não some sinais qualitativos em uma pontuação numérica. Durante a próxima composição equivalente, capture por candidato os arquivos criados/copied/alterados, dependências e pins, caminhos de execução tocados, topologia por papel, atrito de atualização, tempo e retrabalho observados, e custos de chamadas quando aplicável. O custo só poderá ser comparado após o mesmo perfil de capacidade e contrato Atento serem congelados para cada candidato.

## Próximo gate

A execução comparativa depende de executor capaz de materializar os pins exatos. O registro canônico atual informa que a execução empírica comum do Gate 2 está bloqueada por infraestrutura antes do checkout, com AI Butler como próximo alvo dessa fila. Ao retomar, preservar essa fila e o harness comum; não fingir que a ordem deste Top 5 substitui a fila de execução. Depois de destravada a infraestrutura, executar a menor composição equivalente, capturando custo de adaptação na mesma passagem dos testes de autoridade/isolamento.

## Fontes canônicas internas

- `docs/evaluation/naia-architecture-chassis-maintenance-cost-audit-2026-09-30.md`
- `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`
- `docs/evaluation/naia-authority-isolation-gate2-screen-2026-09-30.md`
- `docs/evaluation/naia-gate2-composition-execution-block-2026-09-30.md`
- `docs/evaluation/nanoclaw-change-surface-audit-2026-09-29.md`
- `docs/handoff-2026-09-30-naia-chassis-first-selection.md`
