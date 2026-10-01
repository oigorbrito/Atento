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
| SRC-OPENSEARCH-SEC | OpenSearch Security | https://github.com/opensearch-project/security | `75f5c204ae17ed5d1d266953238abdd9a5eb3b50` | Apache-2.0 | EXTERNAL_RESEARCH_CLONE | resource ownership/sharing/access-control mechanism donor for cross-agent authority; local isolation proof still required |
| SRC-OPENSEARCH-ML | OpenSearch ML Commons | https://github.com/opensearch-project/ml-commons | `594445ced5f1473d73586287ddc14fada0bcdf3f` | Apache-2.0 | EXTERNAL_RESEARCH_CLONE | Tool SPI/factories, agent executor, tenant propagation, memory/context mechanism donor; not a complete NAIA base |
| SRC-OPENSEARCH-AGENTHEALTH | OpenSearch Agent Health | https://github.com/opensearch-project/agent-health | `9a7852020e3d1816052238ac1614d681a0028b9c` | Apache-2.0 | EXTERNAL_RESEARCH_CLONE | evaluation/comparison/trace/cost-token-latency instrumentation donor for AtentoEval patterns |
| SRC-OPENSEARCH-BENCH | OpenSearch Benchmark | https://github.com/opensearch-project/opensearch-benchmark | `1e8cd69bb1050b2642a9562c98ad153e68bb8cfb` | Apache-2.0 | EXTERNAL_RESEARCH_CLONE | reproducible macrobenchmark methodology and retrieval-performance reference; benchmark deltas are not transferable proof |



## OpenSearch mechanism-donor benchmark refinement — 2026-09-30

Canonical evidence record:

- `docs/evaluation/opensearch-mechanism-donor-research-2026-09-30.md`

Classification rule:

```text
OPENSEARCH_PROJECT
!=
COMPLETE_NAIA_CHASSIS

UPSTREAM_BENCHMARK
!=
ATENTO_LOCAL_PROOF
```

The OpenSearch sources above are tracked as bounded mechanism/evaluation/retrieval donors. Their presence in this registry does not create a NAIA/Anna shortlist, select the cross-agent topology, or authorize a code port. Any copied code requires path-level license/notice review and an explicit donor record.

## Candidate re-enumeration sources — 2026-09-29

These entries support the post-reset NAIA/Anna universe rebuild. Presence here is provenance only, not shortlist status.

| ID | Agent scope | Project | Repo | Current pin | Terms observed | Current treatment |
|---|---|---|---|---|---|---|
| SRC-QWENPAW | NAIA | QwenPaw | https://github.com/agentscope-ai/QwenPaw | `777441721aa72db8e380d90e4d0481b05cbfd4cc` | Apache-2.0 | technical persistent-assistant base candidate; not selected |
| SRC-AIBUTLER | NAIA | AI Butler | https://github.com/LumabyteCo/aibutler | `c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | Apache-2.0 | technical persistent-assistant base candidate; public-beta maturity audit required |
| SRC-NANOCLAW | NAIA | NanoClaw | https://github.com/nanocoai/nanoclaw | `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | MIT | technical persistent-assistant base candidate; runtime/provider breadth audit required |
| SRC-TRUSTCLAW | NAIA | TrustClaw | https://github.com/ComposioHQ/trustclaw | `c07410bccb916236b45b563e8c4ff76ad83d3855` | MIT | technical persistent-assistant base candidate; external platform/dependency audit required |
| SRC-OPENASSISTANT | NAIA | Open Assistant | https://github.com/open-assistant-org/open-assistant | `32c55d2643f9fe38777f9212588b2eee45392514` | BSL 1.1 | technical candidate only; adoption/legal review required before any code use |
| SRC-OPENCOUCH | ANNA | OpenCouch | https://github.com/whanyu1212/OpenCouch | `ac5af6ee4c9a06b4050c5a912439f343ade2c35c` | AGPL-3.0 | therapeutic/emotional-support base candidate pending domain-fit and product-maturity audit |
| SRC-INNERDIALOGUE | ANNA | Inner Dialogue | https://github.com/ataglianetti/inner-dialogue | `ffc9e8f78d0f15a8d720436f92fb6e0887fe7461` | MIT (verified from repository LICENSE) | unclassified pending audit: complete chassis vs tooling/mechanism package |
| SRC-THERAPIST-REFLECT | ANNA | therapist | https://github.com/matteodante/therapist | `dd9848fe9662ee6ea7f44f1795fe1d6b8114a47d` | AGPL-3.0 | domain-adjacent mechanism donor; project explicitly scopes itself to self-reflection / not therapy |

Current-head repins for existing candidate evidence:

| ID | Previous Atento qualification pin | Current observed head | Required treatment |
|---|---|---|---|
| SRC-OPENCLAW | `e9571d77e76bd6d35996273d9e8398ad539b26e1` | `ca8f24d05fc49a224adab0c9426077fd8d93801d` | targeted transfer/delta audit only |
| SRC-OPENMAUS | `947bef311bf5c3f55d3590849abf0eb329408519` | `6005b1bf5883a7ffa639c07e729321f89b9532e1` | targeted transfer/delta audit only |
| SRC-PA | `469f45ef468b968b3fccd1936d7e6a0a574e4c5c` | same | reuse existing evidence |
| SRC-THERAPYMIND | `bfed3f5be61bab262bb00a0f3cc9718c4a965243` | same | reuse existing evidence |
| SRC-THERAMIND | `416d0a00ecc8c76229512197765dc95be6513de5` | same | reuse existing evidence |
| SRC-PSYCHAT | `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4` | same | reuse existing evidence; complete-base status still unproven |

Rule:

```text
PROVENANCE_ENTRY != SHORTLIST
CURRENT_HEAD != QUALIFIED_HEAD
TECHNICAL_CANDIDATE != LEGAL_ADOPTION_CLEARED
```


## Historical chassis benchmark candidates — 2026-09-29

These entries preserve shared chassis/evolvability evidence from PR #11. They do not assign an agent base and do not create a NAIA shortlist.

| ID | Project | Frozen revision | Canonical use |
|---|---|---|---|
| SRC-LETTA | Letta Code | `a75111ea610eff9b4a37baba4fbc6ee24bb73c79` | historical architecture-scaffold/evolvability evidence; **not NAIA base selection** |
| SRC-LIBRECHAT | LibreChat | `63363a777612e0d37956cc5d233ac489f3a302c3` | executable control in historical chassis benchmark |
| SRC-DIFY | Dify | `7b0660b45b127a44b6467533ec6a8cd949586770` | plugin/model/RAG/forkability evidence |
| SRC-RASA | Rasa OSS | `60a3cff9c08183760355b07bd60f5223d8916d6b` | channel/state-seam evidence |
| SRC-OPENWEBUI | Open WebUI | `8bd8b4fac5e059578ac0c74b3c18d11139f88b7d` | tools/filters/memory/storage seam evidence |
| SRC-ANYTHINGLLM | AnythingLLM | `a355703427c67c5be17bc57c4c5d5d034e275444` | skills/MCP/RAG/memory evidence |

Canonical reconciled evidence:
- `docs/evaluation/chassis-selection-research-2026-09-29.md`
- `docs/evaluation/chassis-selection-research-2026-09-29.yaml`
- `docs/research/CHASSIS-LETTA-SELECTION-V1.md`

Raw archive provenance remains traceable at PR #11 head `bc2d16be396e92b10ca15b98ccb2f9099058d9ae`; package hash is `d6c7ec9619fd555f45135693bb609ec5718029d6dc2906ca3a64f1d002f64681`.

```text
HISTORICAL_CHASSIS_BENCHMARK
!=
CURRENT_AGENT_BASE_SELECTION
```

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


## NAIA persistent-agent discovery expansion — 2026-09-29

These are provenance entries for technical discovery. Terms/license are intentionally **not used as a technical exclusion or ordering criterion in this phase**. Where terms were not independently reviewed in this pass, that is recorded rather than guessed.

| ID | Agent scope | Project | Repo | Observed pin | Terms in this discovery pass | Current treatment |
|---|---|---|---|---|---|---|
| SRC-RAKAZO | NAIA | Rakazo | https://github.com/elie222/rakazo | `f4583525d632fcd8643fd6e24c7f51e3e04cb990` | not used as technical filter | persistent-agent base candidate; direct Grok-Bot-class match |
| SRC-GOBII | NAIA | Gobii | https://github.com/gobii-ai/gobii-platform | `c9929bf8ea59b4695b99dcab59aa6c97a09c5bdb` | not used as technical filter | persistent AI-employee candidate with durable queue/event/eval surface |
| SRC-OCTOP | NAIA | Octop | https://github.com/TencentCloud/Octop | `e473dd3c4a4741618ffde1a42a3492341a189e8e` | not used as technical filter | multi-user/multi-agent persistent assistant candidate |
| SRC-PERSONALJARVIS | NAIA | PersonalJarvis | https://github.com/PersonalJarvis/PersonalJarvis | `1be33c457739ca7e161ee6fbaf298ec10d4dad3b` | not used as technical filter | desktop persistent-assistant candidate with computer-use |
| SRC-LETTACODE | NAIA | Letta Code | https://github.com/letta-ai/letta-code | `21daa38a8cdd74f2d03b634c8312253080bacfc1` | not used as technical filter | persistent-agent runtime/product-harness candidate |
| SRC-KORTIX | NAIA | Kortix / Suna | https://github.com/kortix-ai/suna | `270c4a57c8ae5ffb85eff6d5b9700c5713612f28` | not used as technical filter | persistent agent-management/platform candidate |
| SRC-ROME | NAIA | Rome | https://github.com/rome-os/rome | `ef523c4659149e2711744deb04ec42c3be339907` | not used as technical filter | persistent-agent base candidate; Grok Bot/Muse class |
| SRC-AGENTZERO | NAIA | Agent Zero | https://github.com/agent0ai/agent-zero | `e3051fb584b1a36be2b0a0c90606f1c2c2d356ec` | not used as technical filter | framework/product boundary candidate with full computer runtime |
| SRC-OPENGROKBOT | NAIA | OpenGrokBot | https://github.com/wolfqing/OpenGrokBot | `43ba51fc0487b7adbb23861a1062a113390833d9` | not used as technical filter | early persistent-agent candidate; direct Grok-Bot-class match |
| SRC-SELFAGENT | NAIA | SelfAgent | https://github.com/oezercet/SelfAgent | `c86b0b1fbc0e177e67b59b8d26cc2ce9c18406d1` | not used as technical filter | provisional persistent-assistant candidate |
| SRC-GOCLAW | NAIA | GoClaw | https://github.com/sausheong/goclaw | `c24c50ba2d16daff6aa2809b6c1a6f592977ae54` | not used as technical filter | provisional persistent-assistant candidate |
| SRC-NEBO | NAIA | Nebo | https://github.com/NeboLoop/nebo-go | `d566d27ec7c5ab36f3b95fdfda371bb45994dfd7` | not used as technical filter | provisional persistent desktop-assistant candidate |
| SRC-GROKBOT-REF | NAIA | Grok Bot | https://docs.x.ai/grok-bot/overview | current product docs observed 2026-09-29 | closed product reference; terms not relevant to source admission | reference product shape only |
| SRC-MUSE-REF | NAIA | Meta Muse | https://ai.meta.com/muse/ | current product docs observed 2026-09-29 | closed product reference; terms not relevant to source admission | reference product shape only |

## Atento system-chassis discovery sources — 2026-09-30

These repositories were inspected at README/documentation level during the whole-product chassis rescreen. `REFERENCE_ONLY` means no code was cloned or adopted and grants no candidate status. Verify the exact terms at the frozen pin before any code transfer.

| SRC-SYS-MINDROOM | MindRoom — system-chassis discovery | https://github.com/mindroom-ai/mindroom | `4f3bd2d108a6f9be28174e0f66d78eeecddca386` | Apache-2.0 verified in LICENSE at pin | REFERENCE_ONLY | multi-agent runtime, Matrix identities, worker scopes, delegated sessions; system composition probe only |
| SRC-SYS-ONTHEIA | Ontheia — system-chassis discovery | https://github.com/Ontheia/ontheia | `70802db61eb16533f55efce3d8785d810223d03b` | AGPL-3.0 LICENSE; upstream also advertises commercial terms | REFERENCE_ONLY | multi-agent platform, RLS/memory namespaces, workflow and handoff probes |
| SRC-SYS-BOBLABS | Bob Labs — system-chassis discovery | https://github.com/boblabs-eu/boblabs | `a91d6dad098c8ba6d24436a856556078151db45d` | Apache-2.0 verified in LICENSE at pin | REFERENCE_ONLY | multi-agent labs, typed handoff bus, per-agent grants and per-lab sandbox probe |
| SRC-SYS-CLAWIX | Clawix — system-chassis discovery | https://github.com/ClawixAI/clawix | `5aee015e0bd793102fba69af486dd6e75df6d802` | README badge claims MIT; LICENSE path not verified at this pin | REFERENCE_ONLY | isolated agent containers, memory scope, RBAC and approval probe |
| SRC-SYS-MEMOH | Memoh — system-chassis discovery | https://github.com/felinics/Memoh | exact commit not frozen; README blob `df463bf149d14483ce388ae89cfcb3b5dde9be90` | README states AGPLv3; verify at frozen commit | REFERENCE_ONLY | per-agent computer/workspace/network/memory and self-hosted deployment probe |
| SRC-SYS-OPENAKITA | OpenAkita — system-chassis discovery | https://github.com/openakita/openakita | `5f5b38da728274f0fd06461a481851be7c0bca6a` | AGPL-3.0 verified in LICENSE at pin | REFERENCE_ONLY | multi-agent assistant, scheduler, computer tools, advertised sandbox; role-boundary probe |
| SRC-SYS-ASTERISM | Asterism — system-architecture reference | https://github.com/qmilab/asterism | `a8383b45f64a9a9c1923053b0f3894efb4672aba` | Apache-2.0 per upstream README; verify before adoption | REFERENCE_ONLY | explicit per-agent state/autonomy and one-way handoff design; current isolation described as logical |
| SRC-SYS-AGENTSPACE | AgentSpace — system-platform watch/reference | https://github.com/HKUDS/AgentSpace | `0f9da1b125def4d5a0d05b34bf7c5cec0686bbf2` | Apache-2.0 per upstream README; verify before adoption | REFERENCE_ONLY | multi-user workspace/control-plane design; sandbox/isolation feature was listed as planned |
