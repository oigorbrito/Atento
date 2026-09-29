# Third-Party Provenance Register

## Document contract

Este arquivo é a fonte canônica para **provenance externo**: origem, commit/versão, licença, restrições de dados, status de adoção e attribution.

Ele não decide arquitetura nem progresso. O uso arquitetural é resumido no `roadmap.md`; decisões estruturais pertencem às ADRs.

Quando houver divergência de licença/commit entre documentos, **este arquivo prevalece** e os demais devem ser corrigidos.

Este arquivo registra todo código, prompt, dataset, modelo, benchmark ou asset externo considerado ou incorporado ao Atento.

> Regra: nada externo deve ser copiado/adaptado para produção sem origem, commit/versão, licença e finalidade registradas aqui.

## Status legend

- `REFERENCE_ONLY` — estudo/arquitetura; nenhum código incorporado.
- `SPIKE_ONLY` — usado apenas em experimento isolado.
- `SELECTIVE_PORT` — parte do código será/foi adaptada com licença compatível.
- `VENDORED` — dependência mantida de forma isolada.
- `MODEL_ADAPTER` — consumido como modelo/serviço.
- `REJECTED` — avaliado e não adotado.

## Registry

| ID | Projeto | Repo / fonte | Commit / versão | Licença | Dados | Status inicial | Uso pretendido |
|---|---|---|---|---|---|---|---|
| SRC-PA | PsychAgent | https://github.com/ECNU-ICALK/PsychAgent | `469f45ef468b968b3fccd1936d7e6a0a574e4c5c` | não declarada no repo verificado | parcial/incompleto | REFERENCE_ONLY | memória, skills, multi-session, reward rollout |
| SRC-PSYCHAT | PsyChat | https://github.com/wink-wink-wink555/PsyChat | `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4` | MIT | knowledge base baseada em PsyDTCorpus; revisar separadamente | SPIKE_ONLY | Agentic RAG, query rewrite, context expansion |
| SRC-THERAPYMIND | TherapyMind | https://github.com/zx070326-hash/TherapyMind | `bfed3f5be61bab262bb00a0f3cc9718c4a965243` | MIT + notice contextual | revisar assets/conteúdo | SPIKE_ONLY | prompt modules, grey-zone tests |
| SRC-PE | PsychEval | https://aclanthology.org/2026.findings-acl.1115/ | paper/release oficial | verificar termos dos assets antes de uso | assets públicos incompletos na referência atual | REFERENCE_ONLY | benchmark multi-session |
| SRC-UKA | User-Aware Active Knowledge Acquisition | https://arxiv.org/abs/2605.29715 | preprint | paper; código/dados não presumidos | não incorporado | REFERENCE_ONLY | belief/uncertainty architecture reference |
| SRC-SAGE | SAGE | https://doi.org/10.1016/j.eswa.2026.131524 | paper | paper; código/dados não presumidos | não incorporado | REFERENCE_ONLY | strategy/retrieval/reranking reference |
| SRC-TEA | TEA-Bench | https://github.com/XingYuSSS/TEA-Bench | pin antes de integrar | Apache-2.0 no repo verificado; revisar dataset separadamente | TEA-Scenario/TEA-Dialog: revisar termos específicos | REFERENCE_ONLY | tool-use benchmark/adapter |
| SRC-ENPMR | ENPMR-Bench | https://aclanthology.org/2026.findings-acl.2080/ | paper/release oficial | verificar código/dados antes de incorporar | não vendorizado | REFERENCE_ONLY | proactive memory benchmark |
| SRC-ESCONV | ESConv | https://github.com/thu-coai/Emotional-Support-Conversation | pin antes de integrar | repo com termos próprios/academic research; revisar antes de uso de produto | dataset externo não vendorizado | REFERENCE_ONLY | strategy benchmark/taxonomy |
| SRC-MHB | MentalHealthBench | https://openai.com/index/introducing-mentalhealthbench/ | release oficial | usar termos da release oficial | não vendorizado | REFERENCE_ONLY | safety/context/agency benchmark |
| SRC-COUNSEL | CounselBench | https://github.com/llm-eval-mental-health/CounselBench | pin antes de integrar | nenhuma licença de repo detectada na revisão inicial | não vendorizado | REFERENCE_ONLY | expert/adversarial evaluation |
| SRC-CADSS | CADSS / CPsDD | https://github.com/FakerBoom/CPsDD | `f6385fa13223574852bdcff85eb6aa0bd36797dc` | código CADSS ainda não publicado; dataset research-only | research-only | REFERENCE_ONLY | Profiler/Summarizer/Planner/Supporter |
| SRC-SOULCHAT | SoulChat2.0 | https://github.com/scutcyr/SoulChat2.0 | `13ec529c9e3851eacbbf09bec9029621ac40e773` | Apache-2.0 | verificar licença específica do corpus/checkpoints | MODEL_ADAPTER | candidate response model / training research |
| SRC-EMOLLM | EmoLLM | https://github.com/SmartFlowAI/EmoLLM | pin antes de usar | MIT | verificar dataset/checkpoint individual | MODEL_ADAPTER | candidate response model / fine-tuning recipes |
| SRC-MINDCHAT | MindChat | https://github.com/X-D-Lab/MindChat | `8309768d156a3c0e719381705a4058fa1ec554d3` | GPL-3.0 | verificar checkpoint individual | REFERENCE_ONLY | model comparison |

## Selective-port record template

Copie uma entrada para cada arquivo/função realmente incorporado:

```yaml
source_id:
upstream_repo:
upstream_commit:
upstream_path:
atento_path:
license:
copyright_notice_preserved:
modifications:
reason_for_reuse:
tests:
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
model_license:
training_data_license_known:
serving_method:
atento_eval_report:
approved_for:
```

## Dataset record template

```yaml
dataset_name:
source:
version:
license:
usage_restrictions:
contains_sensitive_data:
commercial_use_allowed:
redistribution_allowed:
derived_artifacts:
approved_for:
```
