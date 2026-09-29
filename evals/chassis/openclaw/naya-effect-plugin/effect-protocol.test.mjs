import assert from "node:assert/strict";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import {
  ControlledEffectAdapter,
  FakeExternalProvider,
  SimulatedCrashAfterProvider,
} from "./effect-protocol.mjs";

const root = await fs.mkdtemp(path.join(os.tmpdir(), "atento-naya-effect-"));
const provider = new FakeExternalProvider(path.join(root, "provider"));
const stateDir = path.join(root, "adapter");

const first = new ControlledEffectAdapter({ stateDir, provider });
let crashed = false;
try {
  await first.execute({
    operationId: "op-001",
    payload: { value: "book-appointment" },
    faultAfterProvider: true,
  });
} catch (error) {
  assert.ok(error instanceof SimulatedCrashAfterProvider);
  crashed = true;
}
assert.equal(crashed, true);
assert.equal((await first.readOperation("op-001")).status, "pending");
assert.equal(await provider.callCount(), 1);
assert.equal((await provider.read("op-001")).receiptId, "provider:op-001");

const restarted = new ControlledEffectAdapter({ stateDir, provider });
const reconciled = await restarted.reconcile("op-001");
assert.equal(reconciled.status, "completed");
assert.equal(reconciled.reconciled, true);
assert.equal(await provider.callCount(), 1);

const replay = await restarted.execute({
  operationId: "op-001",
  payload: { value: "book-appointment" },
});
assert.equal(replay.status, "completed");
assert.equal(replay.replayed, true);
assert.equal(await provider.callCount(), 1);

const safeRetry = await restarted.execute({
  operationId: "op-002",
  payload: { value: "send-reminder" },
});
assert.equal(safeRetry.status, "completed");
assert.equal(await provider.callCount(), 2);

process.stdout.write(
  JSON.stringify(
    {
      ok: true,
      crash_point: "provider_effect_succeeded_before_local_terminal_commit",
      recovered_without_duplicate: true,
      provider_calls_after_reconcile: 1,
      second_operation_completed: true,
    },
    null,
    2,
  ) + "\n",
);
