# Engram policy-control failure integration — result (2026-09-30)

## Classification

`PASS_WITH_SCOPE` for `AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED` under this exact Engram + Atento adapter composition. The failure traversed the real Engram `--run-due` path and reached the generated task receipt. This closes only the policy-control-error subcheck; `ENGRAM_BROWSER_EFFECT_AUTHORITY` remains `STILL_OPEN`.

## Frozen execution and treatment

- Engram repository/pin: `radotsvetkov/engram@3a43667deec4a680b42f3e880d7d6bac3baf0746`; checkout matched.
- One due one-shot job executed through real `engramd --run-due`.
- Same durable AgentDef shape and scheduled-only MCP identity used by the preceding probe; native browser tools disabled.
- Deterministic treatment: the scheduled adapter's policy hook raised `RuntimeError("policy unavailable")` before authorization.
- Local deterministic OpenAI-compatible provider; 3 calls; no external inference. Fake instrumented driver; no real browser.
- Temporary research harness only. Production Engram source, Atento product runtime, and existing adapter implementation were unchanged.

## Observed evidence

- Engram generated exactly one task from the due job.
- The adapter returned `AuthorityControlUnavailable:browser effect authority control unavailable`; that error appears in the Engram task receipt.
- The adapter audit trace recorded `decision=control_error` and trusted `origin=scheduled`, despite model tool argument `origin=interactive`.
- `driver-effects.jsonl` is empty (0 bytes; SHA-256 is the standard empty-file digest), so no browser-driver effect was invoked after the control error.
- The test credential was not observed in the provider request trace, receipt, or daemon output.
- Task completed after receiving the tool error. This shows fail-closed at the exercised tool boundary; it does not establish broader recovery policy.

## Scope not closed

- Real browser and read/navigation behavior: `NOT_RUN`.
- Resident scheduler tick / zero-idle wake: `NOT_RUN`.
- Other browser/desktop tools and arbitrary external effects: `NOT_TESTED`.
- Candidate qualification, promotion, shortlist/base, or NAIA/Anna topology changes: none.

## Artifact integrity

- `receipt.json`: `7f4d44c8d6d8213a35a4f9cb84fa406e0aeffd93f084f98661c4b2caf5221b94`
- `authority-records.jsonl`: `b3903c870c52fcb48997f18240828ec6b8fe172fdbefbfa6955ad7243439c8f2`
- `driver-effects.jsonl` (empty): `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `provider-trace.json`: `8cd958db7d6a7fa43b6ee1096ff7c3672530ec6f1c5351f917305e3d4cac612a`
- `run-due.log`: `96332c5a7adb91efc7c6ff9ca7763e4bf5cc4e0c5260470c45f23f9a069b3981`
- `summary.txt`: `9b35b3143561a2ded920dd3b9d345d0d90e1a507ba12ccdf05340950a57019ee`
- `mcp_server_policy_probe.py`: `19ddd538355fee6d8939e1d1f3caddfb2d521cbd8d59223041c2afb8152fe34d`
- `run_policy_control_failure_probe.py`: `5b69dfc58591504567787098f90512bf8ec748b6d38ef0309b2a741cb7da5d5f`

Pre-registration: `naia-engram-policy-control-failure-probe-plan-2026-09-30.md`. The additional files are a bounded reproduction harness and raw evidence; no product source/config changes were made.
