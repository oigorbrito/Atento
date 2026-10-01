# NanoClaw follow-up preflight — runtime seam audit — 2026-10-01

## Question

Can the next bounded NanoClaw follow-up directly test Atento's real provider/gateway credential custody and role-bound scheduled-task recovery without building a broad new product runtime or repeating the passing probe?

## Read-only findings

- The Atento branch root contains .github, docs, evals, tools, README.md, roadmap.md, and AGENTS.md. It has no application source/runtime directory or deployed Atento gateway/provider service to launch.
- The only system-chassis NanoClaw workflow is .github/workflows/system-chassis-nanoclaw-probe.yml. It checks out the exact NanoClaw pin, copies in tools/system_chassis/nanoclaw.atento.test.ts, pulls a digest-pinned test utility image, and runs Vitest.
- The probe explicitly states that it exercises NanoClaw's Docker driver with inert role fixtures and does not start NanoClaw's provider/channel/application runtime.
- Its agent containers run /bin/sh -c 'sleep 600' with network: none. Profile provider/channel identifiers are seeded into test DB fixtures; no provider or messaging adapter is instantiated.
- Its credential assertion mounts role-unique synthetic material read-only in an auxiliary container and checks Docker mount metadata. It does not exercise actual gateway credentials, a live provider call, or application/model-visible context.
- Its state recovery check stops candidate-managed test containers and calls the DockerSessionDriver prepare/start path. It does not terminate/restart an Atento host application process.
- The scheduled-task assertion validates task creation, ownership, scoped reads, and denials. It does not fire the task, retry it, or recover it after host restart.

## NanoClaw mobile-client seam — exact pin source review

A follow-up read-only inspection of NanoClaw `4c1eabd3ddd74cc3d71b1871da857391a9411c8d` found:

- `src/channels/adapter.ts` defines a host-side `ChannelAdapter` contract for inbound messages, outbound delivery, setup/teardown, and connection status.
- `src/webhook-server.ts` routes installed Chat SDK adapters and separately registered raw webhooks.
- `docs/api-details.md` describes adding channels through the adapter contract and installed channel contributions.

These are extensibility seams, not a ready mobile-app API. The inspected pin does not expose a generic authenticated mobile chat endpoint, account/session binding contract, or mobile response-stream contract. A mobile client therefore needs a new Atento-owned adapter/API that authenticates the user, fixes the NAIA role/session server-side, submits inbound messages, and returns or streams outbound replies. Client-provided role or agent-group identifiers must not select authority.

Classification:

```text
NANOCLAW_CHANNEL_EXTENSION_SEAM = PRESENT_STATIC
GENERIC_MOBILE_CHAT_API_AT_PIN = NOT_FOUND
MOBILE_AUTH_AND_NAIA_SESSION_BINDING = NOT_IMPLEMENTED_IN_ATENTO
INITIAL_LONG_POLL_SPIKE_COST = 209_IMPLEMENTATION_LINES (131 TEST LINES)
```

This does not establish a structural failure: NanoClaw explicitly supports channel adapters. It does establish that app connectivity is new adapter work, not an existing capability that can be counted as zero-touch. The adapter must be implemented before a mobile-client integration test can exercise the real path.

The local experiment executor has Node.js 24 but no Docker or Podman binary, and the private Atento repository is not available as a local checkout in this workspace. A disposable local NanoClaw worktree was used for the bounded channel spike below. This did not rerun or alter the prior hosted 7/7 chassi assertions and did not exercise the Atento product runtime.

## Decision

```text
NANOCLAW_CURRENT_BASE = PROVISIONAL_SELECTED
ATENTO_PRODUCT_RUNTIME_PRESENT_IN_BRANCH = NO
REAL_GATEWAY_PROVIDER_CUSTODY_SEAM = ABSENT
HOST_PROCESS_RESTART_SEAM = ABSENT
ROLE_BOUND_TASK_FIRE_RETRY_RECOVERY_SEAM = ABSENT
NEW_TESTS_RUN = 2/2 LOCAL ADAPTER TESTS PASS
BUILD = PASS
LINT = PASS
PREVIOUS_7_ASSERTIONS_REPEATED = 0
NEXT_INTEGRATED_PROBE = BLOCKED_ADAPTER
```

There is no existing Atento application seam to attach a narrow test to. Adding another test around the same driver, fake sleep containers, synthetic credential file, or fixture DB would repeat or rename existing evidence and would not close the decision-relevant gaps. Do not dispatch the existing workflow again for this purpose.

## Smallest concrete prerequisite

Implement or expose the actual narrow Atento host adapter that owns the provider/gateway grant and receives scheduled work, with a test mode that can run against synthetic credentials and inert tasks. It must expose one host-process lifecycle boundary. Only then run one focused delta:

1. Verify a role cannot observe/use another role's gateway credential through the actual adapter path.
2. Queue one inert role-bound task per role.
3. Stop/restart the host process once and allow one bounded retry.
4. Verify each task resumes under the same role and cross-role state/credential reads remain denied.

This prerequisite is product runtime implementation work; the current comparison PR and probe harness do not contain that runtime. Until it exists, retain NanoClaw as the provisional direction and report its composition gate as NOT_PASSED, with this follow-up BLOCKED_ADAPTER. Do not count this missing seam as a NanoClaw failure or as a test pass.

## Evidence inspected

- Atento branch root listing: https://github.com/oigorbrito/Atento/tree/codex/atento-bounded-sequential-chassis-test-20261001
- Existing NanoClaw probe: [nanoclaw.atento.test.ts](../../tools/system_chassis/nanoclaw.atento.test.ts)
- Existing workflow: [system-chassis-nanoclaw-probe.yml](../../.github/workflows/system-chassis-nanoclaw-probe.yml)
- Frozen three-role profile: [system_chassis_nanoclaw_v1.json](../../evals/config/system_chassis_nanoclaw_v1.json)
- Existing 7/7 hosted evidence and scope: [Gate 2 continuation](system-chassis-gate2-continuation-2026-10-01.md)
- User-directed provisional selection: [provisional NanoClaw chassis direction](../decisions/provisional-system-chassis-nanoclaw-2026-10-01.md)


## Bounded local mobile-adapter spike — 2026-10-01

On the pinned NanoClaw checkout, a disposable local-only spike registered an opt-in `atento-mobile` ChannelAdapter and exercised it through NanoClaw's real webhook server and channel-delivery registry. The spike contains 209 implementation lines, 131 test lines, and one import line in the channel barrel (340 added lines total). It is not committed to NanoClaw or Atento and is not a production integration.

Results:

- Focused Vitest: 2/2 passed. It verified bearer-token rejection, server-fixed owner identity, rejection of client-supplied role/group selection, inbound message routing, and a simulated agent response returned to an open long-poll request.
- `pnpm run build`: passed.
- ESLint on the changed files: passed.
- During initialization, the unrelated CLI adapter logged `listen EPERM` when attempting to bind its Unix socket in this sandbox. The HTTP webhook and mobile adapter still started, and both focused tests passed.

Scope limits:

- The bearer secret was synthetic and shared; no user/account authentication or production credential custody was tested.
- The “agent” response was a test callback using NanoClaw's real delivery registry, not a model/provider invocation.
- Pending responses live only in process memory and require an open poll. There is no durable queue, reconnect delivery, mobile session binding, host-restart recovery, or hosted Docker run.
- Docker and Podman are absent in this executor. The PR's existing hosted 7/7 chassi evidence was not repeated.

Updated classification:

```text
MOBILE_ADAPTER_SEAM = PROTOTYPE_LOCAL_PASS
INITIAL_LONG_POLL_SPIKE_COST = 209_IMPLEMENTATION_LINES + 131_TEST_LINES + 1_REGISTRATION_LINE
MOBILE_PRODUCTION_AUTH_AND_SESSION_BINDING = NOT_TESTED
MOBILE_DURABLE_DELIVERY_AND_RESTART_RECOVERY = NOT_IMPLEMENTED
ATENTO_PRODUCT_INTEGRATION = NOT_PRESENT
NANOCLAW_COMPOSITION_GATE = NOT_PASSED
```

The spike reduces uncertainty about whether NanoClaw's channel seam can carry a basic authenticated HTTP mobile path: it can. It does not qualify NanoClaw for the product and its handwritten transport/auth shape is not an approved architecture. The next decision-relevant step is to select an integration pattern with traceable empirical evidence or an applicable established standard, implement only the minimum adapter behind Atento's real user/session and credential boundary, then run a falsifiable hosted integration test including delivery and one process restart.


## User-directed evidence requirement for the integrator

The integration layer is a separate decision from the provisional NanoClaw chassis. Do not select the hand-written spike merely because it passed its narrow feasibility tests. The integrator must meet one of these evidence routes before it is accepted:

1. **Benchmark-backed model:** identify a version-pinned, comparable implementation/pattern with a benchmark whose workload actually covers the relevant property. Record source, benchmark protocol, raw result, applicability, and known gaps.
2. **Established standard plus local empirical qualification:** use a published standard for the relevant boundary, then prove Atento's required behavior with predeclared, falsifiable tests. A standard is design evidence, not a benchmark score or a pass for Atento.

For a native mobile client, OAuth for native apps (RFC 8252) and current OAuth security BCP (RFC 9700) are relevant starting points; OWASP MASVS supplies mobile authentication, authorization, and network-security verification controls. These sources do not benchmark a particular Atento adapter and do not establish that NanoClaw or the spike passes them. OpenAPI may make the HTTP contract explicit, but it also does not prove security or runtime behavior.

For the Atento boundary, local acceptance evidence must at minimum cover: user/session-to-NAIA binding on the server; denial of caller-selected role/group; cross-role isolation; authorization on every request; response delivery after client reconnect; idempotent inbound retry; and task/message recovery after one host restart. Use synthetic identities and provider credentials in the test environment. Keep the benchmark signal separate from these local proof results.

```text
INTEGRATOR_SELECTION = NOT_SELECTED
SPIKE_TRANSPORT_AND_AUTH_SHAPE = EXPLORATORY_ONLY
EVIDENCE_ROUTE_REQUIRED = APPLICABLE_STANDARD_PLUS_LOCAL_TESTS OR DIRECTLY_RELEVANT_BENCHMARK_PLUS_LOCAL_GAP_TESTS
NANOCLAW_CHASSIS_BENCHMARK = DOES_NOT_QUALIFY_INTEGRATOR
```

Sources:
- [RFC 8252 — OAuth 2.0 for Native Apps](https://www.rfc-editor.org/rfc/rfc8252.html)
- [RFC 9700 — OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html)
- [OWASP MASVS](https://mas.owasp.org/MASVS/)
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html)


## External transport benchmark triage — 2026-10-01

A directly comparable external benchmark was located for the response transport only: one Node server sent the same event stream through WebSocket, SSE, and long polling. The report includes benchmark code and a reported independent byte-count rerun within 0.1%; it is an author-run benchmark, not a peer-reviewed or mobile-device benchmark.

| Transport | External result in that benchmark | Fit to NAIA mobile chat | Evidence status |
|---|---|---|---|
| REST input + SSE response | For 1,000 ~117-byte events: 131,596 wire bytes; at 10 events/s and simulated 50 ms RTT, mean delivery 26.52 ms. Automatic reconnect/resume is available when the server honors event IDs. | Strong candidate for one-way streamed assistant output; user messages can remain ordinary authenticated HTTP requests. | Benchmark signal only; not tested against Atento or mobile radio networks. |
| WebSocket | For the same events: 119,692 bytes; at 10 events/s, mean 26.46 ms. At 50 events/s, mean 26.16 ms. Lowest idle server memory in that specific Node run. | Candidate if the app requires true bidirectional streaming/presence. More connection/reconnect state must be qualified. | Benchmark signal only; no Atento integration proof. |
| REST input + long-poll response | 884,698 bytes over HTTP/1.1 or 182,475 over HTTP/2 for the same events. At 10 events/s, mean 26.75 ms; at 50 events/s, mean 52.44 ms and p95 76.96 ms. | Viable low-rate fallback, but not the leading candidate for token-by-token streamed answers. | Benchmark signal only; the existing spike's two tests prove only basic feasibility. |

Test setup and limits: one Node server on Apple M5/macOS 26.6.1/Node 26.6.0; 1,000 JSON events; a fixed simulated 50 ms RTT; 500 idle connections for memory; no real WAN jitter/loss, TLS cost, mobile-radio wakeups, or Atento auth, persistence, or restart path. HTTP/2 materially reduces long-poll header bytes. The results cannot be generalized as a universal ranking.

**Bounded next implementation:** use the selected REST+SSE contract for all three app destinations, with per-agent adapters and isolation. Do not build a WebSocket comparator absent a concrete requirement or measured failure. First adapt the already selected NanoClaw path for NAIA; keep Anna and Apollo adapter slots explicit but disabled until their base/status decisions permit implementation. Test the common gateway with inert fixtures for all three agent namespaces before connecting any additional live runtime.

```text
EXTERNAL_TRANSPORT_SIGNAL = SSE_AND_WEBSOCKET_MEASURED; LONG_POLL_MEASURED
TRANSPORT_SHORTLIST = [REST_PLUS_SSE, WEBSOCKET]
FIRST_LOCAL_IMPLEMENTATION = REST_PLUS_SSE_COMMON_GATEWAY_CONTRACT
TRANSPORT_DECISION = REST_PLUS_SSE_SELECTED_FOR_ALL_THREE_AGENT_ROUTES
CURRENT_SPIKE_SCOPE = NAIA_ONLY; SHARED_TRANSPORT_MECHANICS_PROTOTYPED
EXTERNAL_BENCHMARK_REPLACES_LOCAL_SECURITY_AND_RECOVERY_TESTS = NO
```

External benchmark source: [WebSocket vs SSE vs Long Polling: The Real Cost of 1,000 Events](https://theinfinity.dev/articles/websocket-vs-sse-vs-polling), including test method and limitations (2026-08-12). Its results are used only to prune the initial transport set and define measurements; they do not qualify the Atento integrator.

### Bounded integration ordering from available evidence

**REST+SSE is the selected mobile transport pattern for all three agent routes.** The external benchmark applies to the shared one-way assistant-output transport; the local NanoClaw test is only a NAIA-seam feasibility check. This does not select NanoClaw for Anna or Apollo. The external benchmark found near-equal latency at 10 events/s and a measurable long-poll penalty at 50 events/s; SSE also has a standard reconnect mechanism carrying `Last-Event-ID`. The event log/replay itself still has to be implemented and tested by Atento; protocol reconnect alone does not provide durable delivery.

The mobile client must authenticate the stream without placing bearer credentials in a URL. A native SSE implementation that can set the Authorization header (or another reviewed OAuth-compatible credential mechanism) is a hard feasibility check. The browser `EventSource` interface does not expose arbitrary request headers in its constructor, so do not assume the browser API is sufficient for the future app.

Implement the shared gateway contract once, then test isolation across three inert agent adapters using distinct state sentinels and the same requests. Keep the WebSocket comparator deferred. Apply full persistence/restart acceptance when the Atento host runtime exists.



## Follow-up local SSE protocol test — 2026-10-01

The disposable NanoClaw worktree was updated from the initial long-poll sketch to test the benchmark-prioritized REST+SSE path through the same real NanoClaw webhook server and channel-delivery registry. Current experimental footprint is 223 adapter lines + 193 test lines + 1 channel-barrel registration line (417 lines total). This supersedes the initial worktree source; it does not change the initial long-poll result recorded above.

Results:

- Focused Vitest: 2/2 passed.
- `pnpm run build`: passed.
- ESLint on changed files: passed.
- `git diff --check`: passed.
- The SSE test authenticated with a bearer header and confirmed the URL had no query string; client-selected role/group fields remained rejected.
- It delivered one reply on an open stream, disconnected, delivered another reply during the gap, reconnected with `Last-Event-ID`, received only the missing second event, then reconnected at the latest ID and confirmed no duplicate event.

Limits:

- This is a protocol-level local test on NanoClaw's seam, not the actual Atento host runtime or a real mobile app/client library.
- Auth is a shared synthetic token; no OAuth user/session identity, token lifecycle, provider credentials, or account isolation was tested.
- The 256-event replay queue is in process memory. Restart recovery is not implemented; event IDs reset on process restart. Durable outbox and host-restart proof remain blockers.
- No WebSocket prototype was built. External benchmark results prioritize REST+SSE for the next test, while WebSocket remains conditional.
- The CLI adapter still logs sandbox `EPERM` while binding its unrelated Unix socket; the SSE adapter starts and focused tests pass.

Updated status:

```text
REST_PLUS_SSE = LOCAL_PROTOCOL_REPLAY_PASS
WEB_SOCKET = NOT_IMPLEMENTED
SSE_DURABLE_REPLAY = NOT_IMPLEMENTED
MOBILE_CLIENT_AUTH_COMPATIBILITY = NOT_TESTED
MOBILE_APP_INTEGRATOR = NOT_SELECTED
ATENTO_PRODUCT_RUNTIME_GATE = BLOCKED
```

This supports proceeding with REST+SSE as the first integration candidate, based on an external transport benchmark plus local protocol replay tests. It is not sufficient to select or qualify the production integrator. Next gate is to place the event log behind the actual Atento authenticated session boundary and prove recovery across one real host-process restart; only build the WebSocket comparator if that path fails or the product requires bidirectional high-rate traffic.


## Bounded transport decision — 2026-10-01

**Decision: use REST for app-to-assistant messages and SSE for assistant-to-app responses across the Atento mobile app for NAIA, Anna, and Apollo.** The transport is shared; each agent must have a separate registered adapter and isolated identity, session, memory, and tool authority. The external same-workload benchmark supports the transport choice. The local NanoClaw-seam test proves only a synthetic NAIA path, not all three agent boundaries.

Do not build a WebSocket comparator unless the product adds a concrete requirement that SSE cannot meet or production measurements show a material problem. The benchmark does not need to be repeated to make this bounded transport choice.

This selects the transport pattern; it does not claim the production Atento integrator is implemented or security-qualified. Complete the ordinary implementation checks for real user/session authorization, TLS, bounded persistent event replay, and one restart recovery test when the Atento host runtime exists. Keep those as delivery acceptance criteria, not reasons to reopen the transport comparison by default.

```text
ATENTO_MOBILE_APP_TRANSPORT = REST_PLUS_SSE_SELECTED_FOR_ALL_THREE_AGENTS
SELECTION_BASIS = EXTERNAL_COMPARATIVE_BENCHMARK + LOCAL_RECONNECT_REPLAY_TEST
WEBSOCKET_COMPARATOR = DEFERRED_UNLESS_REQUIREMENT_OR_MEASURED_FAILURE
PRODUCTION_INTEGRATOR_IMPLEMENTED = NO
PRODUCTION_INTEGRATOR_SECURITY_AND_RESTART_ACCEPTANCE = PENDING_IMPLEMENTATION
```


## Minimal API contract for implementation — proposed, not implemented

This proposed app-facing contract covers all three product agents. It does not imply that all three runtime adapters exist or are qualified.

**Authentication and authority**

- Both endpoints require an authenticated access token in the `Authorization: Bearer` header over TLS. The authentication provider is not selected here.
- The host derives the owner from the validated token. The app may request one canonical agent slug (`naia`, `anna`, or `apollo`) as its destination; the server checks that agent's registry state and the owner's authorization before routing. The slug grants no authority by itself. Unknown, disabled, or unqualified adapters fail closed; they are never silently routed to another agent.
- Do not accept group, role, credential, or runtime-session authority from the client. Do not put tokens in URLs.
- Bind each authenticated owner to separate agent-specific session, memory, and tool-authority namespaces. Authorize every message and stream request against that mapping.

**Endpoints**

| Operation | Contract |
|---|---|
| `POST /v1/agents/{agent_id}/messages` | `agent_id` is one of `naia`, `anna`, or `apollo`. Accept `Idempotency-Key` plus JSON `{"text":"..."}`; return `202` and a server-generated `message_id`. Reject unknown fields and invalid/oversized text. Scope idempotency to authenticated owner + agent. |
| `GET /v1/agents/{agent_id}/events` | Return `text/event-stream` only for the authenticated owner's selected agent session. Each event has a stable `id`, typed event name, and JSON data. Honor `Last-Event-ID` and replay retained events in order within that agent's stream only. |

The minimal event types are `message.delta`, `message.completed`, and `message.failed`; each carries the server-generated `message_id` and canonical `agent_id`. Native SSE client support for an Authorization header is a compatibility check before selecting the app library. A web `EventSource` implementation that cannot set the required header is not sufficient by itself.

Current adapter readiness is per agent: NAIA → NanoClaw provisional, qualification pending; Anna → base not selected; Apollo → deferred. The app contract covers all three now, while unconfigured routes return `agent_unavailable` until that agent's adapter is selected and passes its own gates.

**Acceptance checks**

1. Missing/invalid token is rejected; a valid owner reaches only adapters authorized for that account.
2. The app can request each canonical agent, but unknown/disabled adapters fail closed and never fall back to NAIA.
3. Role/group/credential/session injection is rejected or ignored by schema and cannot alter server-side routing.
4. Inert NAIA/Anna/Apollo fixtures use distinct sentinel state; a request or event for one agent cannot read or enter another agent's session, memory, or tools.
5. A repeated idempotency key creates one inbound turn within the same owner + agent scope.
6. Disconnect after event `N`, produce `N+1`, reconnect with `Last-Event-ID: N`, and receive `N+1` in order without duplicate delivery within that agent stream.
7. Restart the host once, reconnect as the same owner and agent, and recover the outstanding persisted event.
8. Explicit failure behavior exists for expired/invalid cursors and unavailable storage; it must not silently acknowledge lost data.

The local NanoClaw SSE spike covers only a synthetic NAIA version of streaming/reconnect checks at the channel seam. It does not cover Anna/Apollo dispatch, cross-agent isolation, real token validation, owner mapping, persisted idempotency, storage failure, or host restart. The benchmark informs transport ordering, not authority. No Project Point or production qualification is claimed by this proposed contract.
