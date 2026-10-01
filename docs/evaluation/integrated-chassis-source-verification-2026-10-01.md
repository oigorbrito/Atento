# Exact-pin source verification — integrated chassis candidates — 2026-10-01

## Scope and method

This is a static inspection of source, documentation, migrations, and test definitions at the frozen pins listed below. It records what is present in those files. It does **not** report tests executed in this review, an Atento integration result, a new benchmark, or a cost measurement. Test-file presence is weaker evidence than a passing CI run.

The first sieve remains architecture + chassis. Later metrics stay separate; no values are averaged into a synthetic score.

## Findings

| Candidate / exact pin | Source evidence inspected | What the pin supports | Limitation for Atento |
|---|---|---|---|
| MindRoom — [4f3bd2d](https://github.com/mindroom-ai/mindroom/tree/4f3bd2d108a6f9be28174e0f66d78eeecddca386) | [Agent config](https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/configuration/agents.md), [sandbox proxy](https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/deployment/sandbox-proxy.md), [worker-runtime plan](https://github.com/mindroom-ai/mindroom/blob/4f3bd2d108a6f9be28174e0f66d78eeecddca386/docs/dev/persistent-worker-runtime-plan.md) | Per-agent configuration includes tools, memory, access and delegation; `worker_scope` distinguishes shared, user and user_agent runtime reuse. Canonical agent state remains in one state root. The pinned plan explicitly says agent-isolated filesystem visibility is not fully enforced across all backends: shared-runner and local paths can expose broader shared storage; dedicated Kubernetes workers narrow mounts for selected scopes. | Strong architecture seam, but filesystem boundary is backend-dependent and documented as incomplete. This is a first-sieve risk, not a measured Atento failure. |
| Bob Labs — [a91d6da](https://github.com/boblabs-eu/boblabs/tree/a91d6dad098c8ba6d24436a856556078151db45d) | [Cross-tenant tests](https://github.com/boblabs-eu/boblabs/blob/a91d6dad098c8ba6d24436a856556078151db45d/control-plane/tests/repositories/test_cross_tenant.py), [sandbox HMAC regression](https://github.com/boblabs-eu/boblabs/blob/a91d6dad098c8ba6d24436a856556078151db45d/control-plane/tests/regression/test_cso_2026_06_sandbox_hmac.py), [secret-at-rest regression](https://github.com/boblabs-eu/boblabs/blob/a91d6dad098c8ba6d24436a856556078151db45d/control-plane/tests/regression/test_cso_2026_06_secret_at_rest.py) | Test definitions cover user-visible lab scoping, explicit confirmation for shared memory, signed sandbox requests (HMAC, nonce/timestamp checks), and encrypted provider/MCP secrets. | These tests were inspected, not run here. Coverage is lab/tenant-oriented; it does not establish Atento's Anna/Apollo/secretary role boundary or cross-role handoff. |
| Ontheia — [70802db](https://github.com/Ontheia/ontheia/tree/70802db61eb16533f55efce3d8785d810223d03b) | [Memory namespace tests](https://github.com/Ontheia/ontheia/blob/70802db61eb16533f55efce3d8785d810223d03b/host/src/memory/namespaces.spec.ts), [session RLS migration V43](https://github.com/Ontheia/ontheia/blob/70802db61eb16533f55efce3d8785d810223d03b/migrations/V43__fix_rls_sessions_insert.sql), [session RLS migration V44](https://github.com/Ontheia/ontheia/blob/70802db61eb16533f55efce3d8785d810223d03b/migrations/V44__fix_rls_sessions_lookup.sql) | Namespace tests derive readable agent/user/session/chat namespaces from a user identity and return no readable namespaces without a user ID. The migrations define separate policies for session insert, lookup and modification. | This is implementation/test source evidence, not proof of deployed PostgreSQL policy behavior or Atento domain isolation. Need role-level principal mapping and cross-role negative tests. |
| Clawix — [5aee015](https://github.com/ClawixAI/clawix/tree/5aee015e0bd793102fba69af486dd6e75df6d802) | [Multi-user design](https://github.com/ClawixAI/clawix/blob/5aee015e0bd793102fba69af486dd6e75df6d802/docs/MULTI-USERS.md), [security design](https://github.com/ClawixAI/clawix/blob/5aee015e0bd793102fba69af486dd6e75df6d802/docs/SECURITY.md), UserAgent and Session repository test files | Design docs specify per-user workspaces, sessions keyed by user/agent/channel, ephemeral worker agents, Docker isolation, and mount allowlists. Repository test files exist for user-agent/session behavior. | Inspected repository tests mostly exercise repository calls with mocks; they do not establish end-to-end authorization or container escape resistance. Security doc marks human approval and DB-level append-only enforcement as pending. Terms/license still require separate verification. |
| OpenAkita — [5f5b38d](https://github.com/openakita/openakita/tree/5f5b38da728274f0fd06461a481851be7c0bca6a) | [Agent state tests](https://github.com/openakita/openakita/blob/5f5b38da728274f0fd06461a481851be7c0bca6a/tests/agent/test_state.py), [organization blackboard parity tests](https://github.com/openakita/openakita/blob/5f5b38da728274f0fd06461a481851be7c0bca6a/tests/parity/orgs/test_blackboard_parity.py), [sandbox implementation](https://github.com/openakita/openakita/blob/5f5b38da728274f0fd06461a481851be7c0bca6a/src/openakita/agent/sandbox.py) | State tests cover task lifecycle and session-specific cancellation; blackboard parity tests cover organization/department/node scopes. A sandbox module and organization orchestration are present. | These inspected tests establish lifecycle/parity contracts, not multi-role confidentiality. README security claims were not treated as proof that the OS sandbox enforces Atento's boundary. |

## Existing hosted CI at the frozen pins

These are existing GitHub Actions records whose `head_sha` equals the candidate pin. They were not initiated for Atento. A successful workflow supports only its executed jobs; it does not establish role isolation or Atento acceptance.

| Candidate | Existing run at exact pin | Observed result | Transfer limit |
|---|---|---|---|
| MindRoom | [pytest](https://github.com/mindroom-ai/mindroom/actions/runs/36801369512), [security scan](https://github.com/mindroom-ai/mindroom/actions/runs/36801369497), [smoke stacks](https://github.com/mindroom-ai/mindroom/actions/runs/36801369528) | All completed successfully. Pytest on Python 3.13 passed; dependency audit and Gitleaks steps passed. | Does not settle the documented backend-dependent filesystem visibility gap. |
| Bob Labs | Exact-pin Actions run query returned `total_count = 0`; combined commit statuses also empty. | No hosted run/status found for this SHA through the Actions/status endpoints. | Test definitions remain source evidence only; this is not a candidate failure. |
| Ontheia | [CI](https://github.com/Ontheia/ontheia/actions/runs/35448377114) | Host lint/build/test and WebUI lint/build jobs completed successfully. | Workflow pass; no Atento role-isolation assertion established here. |
| OpenAkita | [CI](https://github.com/openakita/openakita/actions/runs/35951534235) | Overall run successful; setup-center build and full Tauri build passed. Python tests, unit, integration, smoke, and E2E jobs were skipped by path filtering. | Build-scoped result; skipped tests did not pass or fail. |
| Clawix | [CI](https://github.com/ClawixAI/clawix/actions/runs/31412213455) | Lint, format, type-check, and test job completed successfully. | Generic CI success does not by itself validate multi-user or container-security claims. |

All five combined commit status endpoints returned no legacy status entries. GitHub Actions returned exact-SHA runs for MindRoom, Ontheia, OpenAkita, and Clawix; no run was returned for Bob Labs. Treat absent checks as an evidence-availability limit, not a failure.

## Revised first-sieve reading

- **MindRoom:** retain in the queue; exact-pin pytest, security scan and smoke-stack jobs passed, while the documented agent-level filesystem visibility gap remains unresolved.
- **Bob Labs:** retain; test-source evidence exists for tenant/lab scoping, memory-sharing confirmation, sandbox request authentication, and secret storage; no hosted CI run was found for this exact pin.
- **Ontheia:** retain; exact-pin host and WebUI CI jobs passed, and user-derived namespaces/session RLS are inspectable; deployment/runtime proof and Atento role mapping remain open.
- **Clawix:** retain; exact-pin lint/typecheck/test CI passed, but reviewed tests do not validate end-to-end security boundaries.
- **OpenAkita:** retain; exact-pin CI build passed, while Python/unit/integration/smoke/E2E jobs were skipped; orchestration/state contracts do not prove multi-role data isolation.

No candidate passes the Atento whole-system chassis gate from this inspection. The Top 10 remains a priority queue, not a cost ranking. No benchmark was run and no score was created.

## Next evidence gate

Continue sequentially with only the remaining high-value architecture questions: exact principal-to-role binding, cross-role read/write denials, delegated-task authority and output filtering, background-job ownership, and the runtime/deployment boundary. Reuse existing upstream CI results if available; do not convert source inspection into a new benchmark score.

## Provenance

All source references above resolve to the frozen commit pins, not the repositories' moving default branches. This record documents static review performed on 2026-10-01.
