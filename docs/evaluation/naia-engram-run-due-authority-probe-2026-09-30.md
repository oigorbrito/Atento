# Engram external scheduler trigger probe — 2026-09-30

## Purpose and scope

This follow-up targets the only remaining scheduler runtime boundary recorded after PR #50: execute the exact frozen Engram pin through the outer one-shot --run-due entrypoint, with a task created from a due scheduler payload, then compare it with the attended task API path.

It does not select, qualify, accept, promote, or globally fail Engram.

Frozen candidate:
- Repository: radotsvetkov/engram
- Pin: 3a43667deec4a680b42f3e880d7d6bac3baf0746

Atento base before this block: ecadff232f2c60fdb6bc2f09626edee1e8b04608 (PR #50 merge).

## Execution

Runner:
- evals/probes/engram_browser_authority/run_real_run_due_probe.py

The test used a persisted due one-shot job fixture in the candidate's scheduler store. The real Engram --run-due process opened it, passed its payload through production task_from_schedule, ran the resulting task and consumed the one-shot job. A separate fresh Engram daemon served the attended control task through POST /v1/tasks/{id}/run.

One durable agent had both Atento MCP tool identities in its static allowlist. The MCP subprocesses had separate trusted origin settings. The deterministic provider deliberately supplied origin="scheduled" in tool arguments; authority was determined by each MCP subprocess's configured origin.

The native browser tools browser_click and browser_type were disabled through the candidate config and verified absent from the provider's effective tool lists. The MCP adapter used a fake reversible driver. No browser was launched.

Provider and build details:
- Local OpenAI-compatible HTTP test server on loopback; no external LLM request, paid inference, or network egress.
- Cargo build used Engram's production binary path with feature http enabled; test-only #[cfg(test)] probe additions present in the isolated candidate checkout were not included in the binary.
- Seven provider HTTP calls in the recorded final replay.
- CARGO offline build found the dependencies already cached.

## Observed result

The real --run-due task receipt recorded this sequence:

1. Scheduled MCP identity attempted type and received AuthorityDenied.
2. The same unattended task then called the interactive MCP identity.
3. The fake adapter executed the type effect under its trusted interactive origin grant.
4. The job was consumed and the scheduler-created task finished with status done.

The attended comparison used the real daemon task-run HTTP route. Its task called the interactive identity and executed the same effect under the trusted interactive grant.

The provider-visible effective tool lists omitted browser_click and browser_type. The test credential did not appear in daemon output, tool observations, or either task receipt.

Raw logs and receipts are preserved in the evidence directory. Reproduction assets:
- evidence/engramd-run-due-2026-09-30.txt
- evidence/engramd-run-due-2026-09-30.log
- evidence/engramd-interactive-control-2026-09-30.log
- evidence/task-receipts-2026-09-30.json

Runner SHA-256: b6c9422db5d8fb024f2506ccaa4d2aa115fc874402302d85f2e83d6b404bfc23
Run summary SHA-256: e3dcebb7f5b557b7ee06e23e68fce4604953e12195238820816dc50163692d13
Scheduled receipt SHA-256: aa77d51fb0b6b11f73f05c30aed152f5dd71cf7619e19cee95d136c990d8808d

## Classification

~~~ini
REAL_RUN_DUE_ENTRYPOINT = EXECUTED
SCHEDULER_PAYLOAD_TO_TASK = OBSERVED
DUAL_IDENTITY_UNATTENDED_SEPARATION = FAIL_EMPIRICAL_FOR_TESTED_COMPOSITION
ATTENDED_HTTP_CONTROL = PASS_WITH_SCOPE
NATIVE_UNMEDIATED_BROWSER_TOOLS = ABSENT_FROM_EFFECTIVE_TOOLSET
TEST_CREDENTIAL_LEAK = NOT_OBSERVED
RESIDENT_SCHEDULER_TICK = NOT_RUN
REAL_BROWSER_EFFECT = NOT_RUN
ENGRAM_BROWSER_EFFECT_AUTHORITY = STILL_OPEN
ENGRAM_CANDIDATE_FAIL = NOT_CLAIMED
CURRENT_PIN_QUALIFIED = 0
NAIA_SHORTLIST = NOT_SELECTED
NAIA_BASE = NOT_SELECTED
~~~

The observed failure applies to this dual-identity AgentDef composition: --run-due did not prevent the unattended task from calling the interactive adapter identity. It is not a global Engram failure classification. The interactive result is a fake-driver boundary observation, not evidence of a real browser effect. The resident scheduler tick, policy-control failure through this exact CLI path, and a real browser remain untested. No candidate decision state changed.
