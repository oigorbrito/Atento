# Engram policy-control failure microprobe plan — 2026-09-30

## Pre-registration

Atento base before execution:

```text
main = 85a8f7eef94fd7d0c5f65154ffc4a4b02d63f446
```

Frozen candidate:

```text
repository = radotsvetkov/engram
pin = 3a43667deec4a680b42f3e880d7d6bac3baf0746
```

This is one residual subcheck from the frozen RP-BROWSER-01 / RP-AUTH-01 intersection. It does not repeat the scheduled-only authority parity probe. It tests only fail-closed behavior when the adapter's authority-control hook is unavailable.

## One property

```text
AUTHORITY_CONTROL_FAILURE = FAIL_CLOSED
```

## Frozen treatment

Keep the exact candidate pin, durable AgentDef, scheduled-only allowed tool identity, ENGRAM_HOME/job shape, destination, action, local deterministic provider, and Atento adapter policy from the previous runtime probe. Set only the adapter test hook to raise a deterministic policy-unavailable error before authorization. The driver is instrumented in the temporary probe harness to append an event only if a browser action is actually invoked.

Use the real `engramd --run-due` process and a due one-shot job. The deterministic local provider issues one scheduled adapter click request and then terminates after receiving its tool result.

## Acceptance

```ini
PASS_WITH_SCOPE = exact pin and run-due path verified; adapter returns explicit authority-control-unavailable error; driver trace records zero effects; task receipt preserves the error; test credential absent from provider-visible/output surfaces
FAIL = any driver event occurs, or the adapter reports/records execution despite policy control being unavailable
INVALID = pin mismatch, due task not created, adapter call not reached, or effect trace cannot distinguish driver invocation
```

A passing result closes only this fail-closed adapter integration subcheck for this exact composition. It does not close browser authority overall, test a real browser or resident scheduler tick, qualify Engram, or change NAIA/Anna selection.

## Evidence and exclusions

Capture task receipt, provider request/response trace sufficient to prove the error was returned, driver-effect trace, daemon log, exact pin, wall time, hashes, and temporary harness diff. The production Engram checkout remains unmodified. No external inference, real browser, adapter suite rerun, generic benchmark, candidate promotion, or product configuration change.
