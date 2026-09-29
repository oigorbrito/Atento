# Third-Party Provenance Register

## Document contract

Este arquivo é a fonte canônica para **provenance externo**: origem, commit/versão, termos/licença conhecidos, artefatos usados, modo de adoção e attribution.

O Atento está atualmente em **modo de pesquisa/estudo**. A política interna permite `FULL_DONOR` quando empiricamente defensável.

> **DECISION RESET:** os campos de status/adoption deste registro descrevem provenance, modo histórico de consideração ou possibilidade técnica. Eles **não constituem shortlist, preferência ou decisão atual** de chassis da NAIA ou da Anna. A seleção da Anna é regida por `docs/adr/ADR-ANNA-001-therapeutic-base-selection.md` enquanto o reset estiver ativo.

> Importante: autorização interna para copiar/adaptar não altera direitos de terceiros. Para estudo é permitido clonar e executar donors; para redistribuir código copiado dentro deste repositório, preservar notices e observar os termos externos aplicáveis.

## Status legend

- `REFERENCE_ONLY` — apenas referência.
- `EXTERNAL_RESEARCH_CLONE` — clone externo para estudo/benchmark.
- `FULL_DONOR_CANDIDATE` — candidato a adoção integral.
- `FULL_DONOR` — donor integral adotado.
- `FORK` — fork mantido com relação upstream.
- `SELECTIVE_PORT` — partes adotadas.
- `MODEL_ADAPTER` — modelo/serviço integrado.
- `REJECTED` — avaliado e rejeitado empiricamente.

## Registry

| ID | Projeto | Repo / fonte | Commit / versão | Termos conhecidos | Status inicial | Uso pretendido |
|---|---|---|---|---|---|---|
| SRC-PA | PsychAgent (Anna research; selection reset) | https://github.com/ECNU-ICALK/PsychAgent | `469f45ef468b968b3fccd1936d7e6a0a574e4c5c` | licença de repo não detectada na revisão | EXTERNAL_RESEARCH_CLONE | memória, skills, multi-session, reward rollout |
| SRC-PSYCHAT | PsyChat (Anna research; selection reset) | https://github.com/wink-wink-wink555/PsyChat | `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4` | MIT | FULL_DONOR_CANDIDATE | Agentic RAG, query rewrite, context expansion, runtime donor |
| SRC-THERAPYMIND | TherapyMind (Anna research; selection reset) | https://github.com/zx070326-hash/TherapyMind | `bfed3f5be61bab262bb00a0f3cc9718c4a965243` | MIT + notice contextual | FULL_DONOR_CANDIDATE | prompts modulares, safety patterns, grey-zone tests |
| SRC-PE | PsychEval | https://aclanthology.org/2026.findings-acl.1115/ | release oficial | verificar assets específicos ao integrar | REFERENCE_ONLY | multi-session benchmark |
| SRC-UKA | User-Aware Active Knowledge Acquisition | https://arxiv.org/abs/2605.29715 | preprint | paper; implementação pública não presumida | REFERENCE_ONLY | belief/uncertainty |
| SRC-SAGE | SAGE | https://doi.org/10.1016/j.eswa.2026.131524 | paper | paper; implementação pública não presumida | REFERENCE_ONLY | strategy/retrieval/reranking |
| SRC-TEA | TEA-Bench | https://github.com/XingYuSSS/TEA-Bench | pin antes de integrar | Apache-2.0 no repo verificado; revisar dataset separadamente | SELECTIVE_PORT | tool-use benchmark/runtime patterns |
| SRC-ENPMR | ENPMR-Bench | https://aclanthology.org/2026.findings-acl.2080/ | release oficial | verificar assets ao integrar | REFERENCE_ONLY | proactive memory benchmark |
| SRC-ESCONV | ESConv | https://github.com/thu-coai/Emotional-Support-Conversation | pin antes de integrar | termos acadêmicos no repo; registrar antes de redistribuir | EXTERNAL_RESEARCH_CLONE | strategy taxonomy/benchmark |
| SRC-MHB | MentalHealthBench | https://openai.com/index/introducing-mentalhealthbench/ | release oficial | usar termos da release oficial | REFERENCE_ONLY | safety/context/agency benchmark |
| SRC-COUNSEL | CounselBench | https://github.com/llm-eval-mental-health/CounselBench | pin antes de integrar | licença de repo não detectada na revisão inicial | EXTERNAL_RESEARCH_CLONE | expert/adversarial eval |
| SRC-CADSS | CADSS / CPsDD | https://github.com/FakerBoom/CPsDD | `f6385fa13223574852bdcff85eb6aa0bd36797dc` | código CADSS ainda não publicado no snapshot; dataset research-oriented | REFERENCE_ONLY | Profiler/Summarizer/Planner/Supporter |
| SRC-SOULCHAT | SoulChat2.0 | https://github.com/scutcyr/SoulChat2.0 | `13ec529c9e3851eacbbf09bec9029621ac40e773` | Apache-2.0 no repo; verificar corpus/checkpoint individual | FULL_DONOR_CANDIDATE | generator/training pipeline |
| SRC-EMOLLM | EmoLLM | https://github.com/SmartFlowAI/EmoLLM | pin antes de usar | MIT no repo; verificar dataset/checkpoint individual | FULL_DONOR_CANDIDATE | model/training/deploy/RAG donor |
| SRC-MINDCHAT | MindChat | https://github.com/X-D-Lab/MindChat | `8309768d156a3c0e719381705a4058fa1ec554d3` | GPL-3.0 no repo; verificar checkpoint individual | FULL_DONOR_CANDIDATE | model/local deployment donor |
| SRC-OPENMAUS | OpenMausBot (NAIA research; selection reset) | https://github.com/milind-soni/OpenMausBot | `947bef311bf5c3f55d3590849abf0eb329408519` (qualification snapshot; upstream had advanced to `7cd31c2a7f780757dd6933ec175d11e06103fd0f` during the 2026-09-29 audit) | Apache-2.0 outside `enterprise/`; `enterprise/` has separate source-available production terms | EXTERNAL_RESEARCH_CLONE | personal-assistant base candidate: persistence, routines, computer/apps, provider/model switching |
| SRC-OPENCLAW | OpenClaw (NAIA research; selection reset) | https://github.com/openclaw/openclaw | `e9571d77e76bd6d35996273d9e8398ad539b26e1` (qualification repin on 2026-09-29; qualification started at `df97da27f07f6655d5678bdbf1f6f9e460678013`) | MIT | EXTERNAL_RESEARCH_CLONE | personal-assistant base candidate: Gateway, restart recovery, persisted approvals, durable outbound delivery; static qualification recorded in `docs/evaluation/openclaw-qualification-2026-09-29.md` |
| SRC-NAIA | NaIa historical implementation/donor (distinct from current NAIA product identity) | https://github.com/oigorbrito/NaIa | `23e4ca55abfaf399844047792018a22415ed3738` | root license not detected in reviewed revision | EXTERNAL_RESEARCH_CLONE | policy/approval/evidence/memory-authority donor and assistant-base comparison |
| SRC-AGENTMENTAL | AgentMental | https://github.com/MindIntLab-HFUT/AgentMental | `0e2fc8ff27552845ae743e3373351120a96e216b` | MIT | EXTERNAL_RESEARCH_CLONE | adaptive information-gap detection, targeted follow-up, uncertainty reduction |
| SRC-PATIENTPSI | PATIENT-Ψ | https://github.com/ruiyiw/patient-psi | `de72a768e5366d3e94f7d8c711c563fb4a5b4d26` | MIT | EXTERNAL_RESEARCH_CLONE | patient-style simulation/evaluation, including reserved/evasive behavior |
| SRC-MHSAFE | MHSafeEval | https://github.com/suhyun565/MHSafeEval | `9889223844464cfa777a7b8066fd14418f287b85` | no root license detected in reviewed revision; verify paper/assets terms before integration | EXTERNAL_RESEARCH_CLONE | adversarial multi-turn mental-health safety evaluation |
| SRC-THERAMIND | TheraMind (Emo-gml; Anna research; distinct from SRC-THERAPYMIND; selection reset) | https://github.com/Emo-gml/TheraMind | `416d0a00ecc8c76229512197765dc95be6513de5` | README: research and educational use only | EXTERNAL_RESEARCH_CLONE | longitudinal dual-loop/adaptive-therapy mechanism donor; not a cleared product base |


## Full donor record template

```yaml
source_id:
adoption_mode: FULL_DONOR | FORK | SELECTIVE_PORT | MODEL_ADAPTER
upstream_repo:
upstream_commit:
upstream_license_or_terms:
copied_paths:
removed_paths:
modified_paths:
notices_preserved:
local_wrapper:
benchmark_report:
safety_report:
upstream_sync_strategy:
redistribution_note:
reviewed_by:
date:
```

## Model/checkpoint record template

```yaml
source_id:
model_name:
model_url:
model_revision:
base_model:
model_terms:
training_data_terms_known:
serving_method:
atento_eval_report:
approved_for:
```

## Dataset record template

```yaml
dataset_name:
source:
version:
terms:
contains_sensitive_data:
stored_in_repo:
external_path_or_hash:
derived_artifacts:
approved_for:
```
