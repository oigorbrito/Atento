# ADR-001 — Composição de agentes do produto

> **DECISION RESET — 2026-09-29:** preservar os requisitos de isolamento e a evidência já produzida, mas não tratar a topologia histórica abaixo como arquitetura selecionada. A nomenclatura corrente é **NAIA / Anna / Apollo**.

## Document contract

Esta ADR preserva a hipótese arquitetural histórica de separação entre domínios, mas sua topologia concreta está reaberta durante a reconciliação do produto.

Ela não escolhe o sistema-base da Assistente nem o sistema-base terapêutico. Essas seleções têm ADRs/evidências próprias.

- **Status:** Reopened — `DECISION_RESET`
- **Date:** 2026-09-29
- **Decision owners:** TBD

## Context

O produto agora possui três agentes conceitualmente distintos. Esta ADR histórica descrevia apenas dois deles e, por isso, não é mais suficiente como definição completa:

1. **NAIA — assistente pessoal/secretária**
   - calendário;
   - mensagens;
   - e-mail;
   - pesquisa;
   - compras;
   - rotinas;
   - computer/browser use;
   - ferramentas com side effects.

2. **Anna — assistente emocional/terapêutica**
   - conversa terapêutica;
   - memória longitudinal terapêutica;
   - planejamento;
   - skills/intervenções;
   - safety e escalation;
   - acompanhamento multi-sessão.

3. **Apollo — nutrição/personal trainer** — permanece adiado.

O requisito atual é que esses domínios não sejam fundidos em um agente onisciente com acesso irrestrito a tools, memória ou chats dos demais.

## Functional authority matrix

The product-level role contract is:

| Domain / capability | NAIA | Anna | Apollo |
|---|---|---|---|
| general personal assistant / secretary | **OWNER** | out of scope | out of scope |
| calendar, messages, email, shopping, general research | **OWNER / EXECUTOR** | handoff to NAIA | handoff to NAIA |
| browser/computer/apps and general personal side effects | **OWNER / EXECUTOR** | no inherited authority | no inherited authority |
| therapeutic/emotional conversation | out of scope except routing/handoff | **OWNER** | out of scope |
| therapeutic longitudinal memory / strategy / interventions | no default access | **OWNER** | no default access |
| therapeutic safety/escalation policy | no default ownership | **OWNER** | no default ownership |
| fitness/training/nutrition planning | out of scope except routing/handoff | out of scope | **OWNER** |
| fitness progress / adherence / wearable-domain state | no default access | no default access | **OWNER** |
| general logistics produced by another domain | **EXECUTOR after explicit handoff** | REQUESTER | REQUESTER |

Interpretation:

```text
DOMAIN_OWNER
!=
GENERAL_SIDE_EFFECT_EXECUTOR

NAIA = general personal operational executor
ANNA = therapeutic/emotional domain authority
APOLLO = fitness/nutrition domain authority
```

NAIA may be the primary user-facing entry point, but primary entry point does not grant cross-agent memory or tool authority.

Anna and Apollo may use tools that are intrinsic to their own domain under their own future policy. They do not inherit NAIA's general personal-action toolset.

## Historical candidate topology — not selected

```text
                         ATENTO PRODUCT
                              |
              +---------------+---------------+
              |                               |
             NAIA                         ANNA
      bounded context                   bounded context
              |                               |
              +--------- HANDOFF BROKER ------+
                    minimal / explicit
```

### Boundary invariants

O alvo arquitetural deve permitir provar:

```text
Therapist cannot query Assistant memory by default
Assistant cannot query Therapy memory by default

Therapist cannot invoke personal-side-effect tools by default
Assistant cannot invoke therapy internals by default

Cross-domain exchange uses explicit contracts
Cross-domain payload is minimum necessary
Sensitive handoff can require explicit user consent
Every handoff is auditable
```

A separação deve ser enforced pelo runtime/policy, não apenas por prompt ou fine-tuning.

## Example handoff

Durante uma sessão terapêutica:

> usuário relata dificuldade em marcar uma consulta médica.

A terapeuta pode propor:

```text
ACTION_REQUEST
type: appointment_help
minimum_payload:
  specialty: cardiology
  user_requested_help: true
```

O payload não deve carregar automaticamente:

- transcrição terapêutica;
- formulações clínicas;
- histórico emocional;
- notas privadas da sessão;
- memória terapêutica sem necessidade explícita.

A Assistente executa a tarefa operacional sob sua própria policy/approval boundary.

## Non-goals

Esta ADR não determina:

- monorepo vs múltiplos repositórios;
- mesma linguagem/runtime;
- mesmo banco;
- mesmo provedor de modelo;
- mesma engine de memória;
- que o usuário deva perceber duas marcas/produtos;
- que um sistema possa ler o armazenamento interno do outro.

Um único produto pode conter dois runtimes independentemente autorizados.

## Why this is proposed rather than accepted

A direção reduz blast radius e segue least privilege/data minimization, mas ainda precisa ser concretizada e testada no Atento.

Antes de aceitar:

- definir contratos de handoff;
- definir esquema de consentimento;
- provar isolamento de tools;
- provar isolamento de memória;
- provar que a experiência não força handoffs desnecessários;
- testar recuperação/restart sem cruzar autoridade;
- decidir topologia de deploy/repo.

## Fine-tuning rule

Fine-tuning pode melhorar comportamento, voz e resistência a role drift.

Não pode ser a boundary de segurança.

Ordem esperada:

```text
runtime capability isolation
→ policy/authorization
→ handoff contract
→ adversarial eval
→ behavior training/fine-tuning quando necessário
```

## Decision reset

```yaml
decision: NOT_SELECTED
status: DECISION_RESET
required_property: strong_cross_agent_isolation
naia_memory_authority: separate
anna_memory_authority: separate
apollo_memory_authority: separate_when_implemented
cross_agent_topology: TBD
handoff_mechanism: TBD
```

## Acceptance evidence required

- [ ] tool isolation test
- [ ] memory isolation test
- [ ] cross-domain leakage test
- [ ] minimal-disclosure handoff test
- [ ] explicit-consent test for sensitive handoff
- [ ] restart/recovery authority test
- [ ] role-drift adversarial suite
