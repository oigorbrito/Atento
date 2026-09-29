# ADR-001 — Composição do produto Nayá: Assistente e Terapeuta

## Document contract

Esta ADR define a hipótese arquitetural de composição do produto Nayá dentro do projeto Atento.

Ela não escolhe o sistema-base da Assistente nem o sistema-base terapêutico. Essas seleções têm ADRs/evidências próprias.

- **Status:** Proposed
- **Date:** 2026-09-29
- **Decision owners:** TBD

## Context

O produto pretendido possui dois conjuntos de responsabilidades materialmente diferentes:

1. **Assistente pessoal/secretária**
   - calendário;
   - mensagens;
   - e-mail;
   - pesquisa;
   - compras;
   - rotinas;
   - computer/browser use;
   - ferramentas com side effects.

2. **Terapeuta**
   - conversa terapêutica;
   - memória longitudinal terapêutica;
   - planejamento;
   - skills/intervenções;
   - safety e escalation;
   - acompanhamento multi-sessão.

A hipótese atual é que essas responsabilidades não devem ser fundidas em um único agente onisciente com acesso irrestrito a tools e memória.

## Proposed architecture

```text
                         NAYÁ PRODUCT
                              |
              +---------------+---------------+
              |                               |
      PERSONAL ASSISTANT                THERAPIST
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

## Decision

```yaml
decision: TBD
candidate: separate-bounded-contexts-with-handoff-broker
status: proposed
assistant_memory_authority: separate
therapy_memory_authority: separate
assistant_tool_authority: separate
therapy_tool_authority: restricted
cross_domain_channel: explicit_handoff_only
```

## Acceptance evidence required

- [ ] tool isolation test
- [ ] memory isolation test
- [ ] cross-domain leakage test
- [ ] minimal-disclosure handoff test
- [ ] explicit-consent test for sensitive handoff
- [ ] restart/recovery authority test
- [ ] role-drift adversarial suite
