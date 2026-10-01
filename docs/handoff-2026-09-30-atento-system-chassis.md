# Handoff — Atento system-level architecture/chassis rescreen

Date: 2026-09-30 (America/Sao_Paulo)

## Objective

Continue the Atento decision at the **complete product architecture/chassis** level: NAIA (personal assistant/secretary), Anna (therapeutic/emotional agent), and Apollo (fitness/nutrition; functional research remains deferred). Choose no architecture until evidence supports the lowest defensible total adaptation and ongoing-maintenance cost while all hard role boundaries pass.

## Current reconciled state

```text
OLD_NAIA_GATE1 = VALID_FOR_NAIA_ROLE_ONLY (26 screened, 25 advanced, SelfAgent stopped as complete NAIA base at its pin)
OLD_NAIA_TOP5 = ROLE_SPECIFIC_MEASUREMENT_COHORT_ONLY
NEW_SYSTEM_LEVEL_SCREEN = DISCOVERY_AND_STATIC_PRETRIAGE
NEW_SYSTEM_PLATFORM_DISCOVERY = [MindRoom, Ontheia, Bob Labs, Clawix, Memoh, OpenAkita]
CARRYOVER_COMPOSITION_PROBES = [OpenClaw, QwenPaw]
ARCHITECTURE_REFERENCES = [Asterism, AgentSpace]
NEW_TECHNICAL_ELIMINATIONS = 0
THREE_ROLE_ATENTO_COMPOSITION_TESTS = 0
COMPARABLE_SYSTEM_COST_MEASUREMENTS = 0
SYSTEM_CHASSIS_WINNER = NONE
SYSTEM_CHASSIS_SHORTLIST = NOT_SELECTED
APOLLO_FUNCTIONAL_CHASSIS_RESEARCH = DEFERRED
```

Repository README/docs were inspected; no candidate was cloned or executed in this discovery sweep. Upstream README claims and source tests do not establish Atento system proof.

## Canonical records

- System-level rescreen and initial GitHub discovery: `docs/evaluation/atento-system-architecture-chassis-rescreen-2026-09-30.md`
- Product composition ADR and current boundaries: `docs/adr/ADR-001-naya-product-composition.md`
- External source/provenance entries: `docs/third-party.md`
- Former NAIA-only screen: `docs/evaluation/naia-architecture-gate1-screen-2026-09-30.md`
- Former NAIA-only measurement cohort: `docs/evaluation/naia-architecture-chassis-top5-prioritization-2026-10-01.md`
- Former NAIA-only policy now explicitly scope-bounded: `docs/evaluation/naia-architecture-first-chassis-selection-2026-09-30.md`

## Next work

1. Reconcile the full former 26-candidate universe against the system-level contract without turning NAIA-only passes into system passes.
2. Freeze exact commits for each system-level candidate. Memoh exact commit is still unresolved; OpenClaw/QwenPaw must use Atento's frozen candidate pins rather than branch heads.
3. Compare three open architecture alternatives: integrated multi-agent platform, separate specialist chassis behind an explicit Atento control/handoff layer, and hybrid shared control plane with isolated role runtimes.
4. Run only the smallest exact-pin source/test probes for missing seams: role identity/state ownership, private chats/memory/credentials/tool grants, handoff mediation, scheduler/recovery authority, and update/deployment surface.
5. Run a common three-role negative composition only after exact pins/materialization are ready. Capture adaptation and ongoing-maintenance cost in the same runs. An infrastructure block is not candidate failure.
6. Do not set a system-level Top 5, shortlist, or winner until comparable cost evidence and all hard gates support it.

Do not reactivate Apollo's separate functional candidate search: keep Apollo's domain boundary in the shared architecture contract while its functional-base research remains deferred.
