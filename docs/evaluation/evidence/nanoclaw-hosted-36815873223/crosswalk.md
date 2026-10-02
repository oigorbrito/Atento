# NanoClaw hosted probe evidence crosswalk

Source: [run 36815873223](https://github.com/oigorbrito/Atento/actions/runs/36815873223), exact upstream pin `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d`. The preserved raw JUnit and provenance receipt are in this directory. This crosswalk interprets the already executed test cases; it does not constitute a new run or a candidate-neutral common-matrix execution.

| JUnit test case | Directly observed property | Common assertion slice supported | Remaining scope limit |
|---|---|---|---|
| `keeps role state writable only through that role container mount` | Each role container writes to and reads its configured group-state mount; other role sentinels are absent from that file. | `SYS-STATE-01`: distinct role roots and configured owner mapping, with scope. | No shared Atento host/runtime; no full common assertion body rerun. |
| `retains each group state root across a driver stop and prepare cycle` | Candidate driver stop/prepare reuses the same host state root. | State persistence component evidence. | Not an Atento host-process restart and not proof of chat-session continuity after that restart. |
| `resolves role-scoped chat sessions and blocks unregistered native cross-role sends` | Own role sessions resolve; lookup under another role's group is absent; unbrokered native cross-role send is denied. | `SYS-CHAT-01`: own/cross-role session slices; `SYS-TOOL-01`: narrow unbrokered-send denial. | No host restart continuity assertion; not the complete common tool-authority matrix. |
| `keeps scheduled-task ownership and task-session creation within the profile role` | Task and generated task-session remain owned by the caller's profile role; cross-role task creation is rejected. | `SYS-BG-01`: ownership slice. | Does not fire a task or measure claim, restart, retry count, grants after restart, or terminal-delivery count. |
| `delivers typed Anna/Apollo requests to NAIA for receiver-side reauthorization` | Anna/Apollo typed minimal requests reach the NAIA mailbox; receiver-side task creation is authorized; sender-side unauthorized creation, malformed/overbroad/wrong-recipient paths, and unbrokered direct sends are rejected. | Existing `SYS-HANDOFF-01/02 = PASS_WITH_SCOPE` and receiver-reauthorization slice. | Synthetic broker/reference fixture only; no production provider/model wiring. Do not rerun these equivalent handoff assertions. |
| `keeps synthetic identity material in the per-session auxiliary container` | Synthetic material is readable in the auxiliary holder and absent from the agent container's mounts. | `SYS-CRED-01`: narrow synthetic mount-isolation evidence. | Not real provider credential custody; no complete foreign-lookup, prompt, workspace, and log scan. |
| `realizes one role-scoped state source per container and no host secret mounts` | Agent container receives exactly its role's configured state mount and no host secret mount. | `SYS-STATE-01`: state-source/owner mapping; narrow credential-mount exclusion. | Does not establish the integrated host's global storage or provider-gateway policy. |



## Reuse boundary against common-runner v1

The existing handoff disposition remains `PASS_WITH_SCOPE` for the hosted probe's recorded broker/mailbox behavior. This does not mean the JUnit artifact satisfies every case in `tools/system_chassis/common_runner.py`:

- Common `SYS-HANDOFF-01` also requires `handoff_audit_record=PRESENT`; the pinned probe has no audit-record assertion or write.
- Common `SYS-HANDOFF-02` expects malformed, overbroad, and wrong-recipient denials for both Anna and Apollo. The pinned probe tests those three negative payloads with Anna as sender; the unbrokered direct-send denial is exercised for both.

If this artifact is imported into the stricter common runner, those handoff rows remain incomplete. That is an equivalence boundary for this artifact, not a reversal of the prior scoped result and not a candidate failure. Do not repeat the hosted handoff tests to fill the documentation gap; any future common round must use its frozen oracle and capture the missing observations only when an authorized adapter/runtime path exists.

## Normalized disposition

```text
SOURCE_RUN = 36815873223
SOURCE_TESTS = 7 PASSED / 0 FAILED / 0 ERRORS / 0 SKIPPED
NEW_TESTS_RUN = 0
SYS-HANDOFF-01/02 = PASS_WITH_SCOPE (existing scoped result); common-runner v1 exact coverage = INCOMPLETE
SYS-STATE-01 = PASS_WITH_SCOPE (test-harness scope)
SYS-CHAT-01 = PARTIAL; restart continuity remains unobserved
SYS-BG-01 = PARTIAL; host restart/retry/delivery remain unobserved
SYS-CRED-01 = PARTIAL; production custody and full scans remain unobserved
COMMON_11_CANDIDATE_ROUND = BLOCKED_ADAPTER
```

Do not turn these component slices into a full three-role Atento runtime pass. This crosswalk reuses the exact artifact and leaves the frozen cohort status unchanged.
