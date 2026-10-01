import Database from 'better-sqlite3';
import { afterEach, describe, expect, it } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawn, type ChildProcess } from 'node:child_process';
import { ensureSchema, openInboundDb } from './mailbox/sqlite/session-db.js';
import { insertTaskRow } from './mailbox/sqlite/tasks.js';

const taskId = 'naia-restart-retry-spike-task';
let scratch: string | undefined;
let children: ChildProcess[] = [];

function startWorker(mode: 'claim' | 'recover', inboundPath: string, outboundPath: string): ChildProcess {
  const child = spawn(process.execPath, ['--import', 'tsx', 'src/system-chassis-task-restart-spike-worker.ts', mode], {
    cwd: process.cwd(),
    env: { ...process.env, SPIKE_INBOUND_DB: inboundPath, SPIKE_OUTBOUND_DB: outboundPath },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  children.push(child);
  return child;
}

function waitForMarker(child: ChildProcess, marker: string, timeoutMs: number): Promise<string> {
  return new Promise((resolve, reject) => {
    let output = '';
    const timer = setTimeout(() => reject(new Error(`timeout waiting for ${marker}; output=${output}`)), timeoutMs);
    child.stdout?.on('data', (chunk: Buffer) => {
      output += chunk.toString();
      if (output.includes(marker)) {
        clearTimeout(timer);
        resolve(output);
      }
    });
    child.stderr?.on('data', (chunk: Buffer) => { output += chunk.toString(); });
    child.once('exit', (code, signal) => {
      clearTimeout(timer);
      reject(new Error(`worker exited before ${marker}; code=${code}; signal=${signal}; output=${output}`));
    });
  });
}

function waitForExit(child: ChildProcess, timeoutMs: number): Promise<{ code: number | null; signal: NodeJS.Signals | null }> {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error('worker process did not exit within bound')), timeoutMs);
    child.once('exit', (code, signal) => {
      clearTimeout(timer);
      resolve({ code, signal });
    });
  });
}

afterEach(() => {
  for (const child of children) {
    if (child.exitCode === null && child.signalCode === null) child.kill('SIGKILL');
  }
  children = [];
  if (scratch) rmSync(scratch, { recursive: true, force: true });
  scratch = undefined;
});

describe('NanoClaw task-restart seam spike — disposable harness only', () => {
  it('reuses persisted task state and candidate orphan-claim recovery across one worker-process crash', async () => {
    scratch = mkdtempSync(join(tmpdir(), 'nanoclaw-task-restart-spike-'));
    const inboundPath = join(scratch, 'naia-inbound.db');
    const outboundPath = join(scratch, 'naia-outbound.db');
    ensureSchema(inboundPath, 'inbound');
    ensureSchema(outboundPath, 'outbound');

    const inbound = openInboundDb(inboundPath);
    insertTaskRow(inbound, {
      id: taskId,
      seriesId: taskId,
      processAfter: new Date(Date.now() - 1000).toISOString(),
      recurrence: null,
      content: JSON.stringify({ prompt: 'inert restart-recovery probe', spikeOwner: 'NAIA' }),
    });
    inbound.exec('CREATE TABLE spike_task_owner (task_id TEXT PRIMARY KEY, role TEXT NOT NULL)');
    inbound.prepare('INSERT INTO spike_task_owner (task_id, role) VALUES (?, ?)').run(taskId, 'NAIA');
    inbound.exec(`
      CREATE TABLE spike_terminal_delivery (
        task_id TEXT PRIMARY KEY,
        role TEXT NOT NULL,
        attempt INTEGER NOT NULL
      )
    `);
    inbound.close();

    // One host fixture process claims, then the parent SIGKILLs it before ack.
    const first = startWorker('claim', inboundPath, outboundPath);
    const claimOutput = await waitForMarker(first, 'SPIKE_CLAIMED=', 15000);
    expect(claimOutput).toContain(`"taskId":"${taskId}"`);
    expect(claimOutput).toContain('"role":"NAIA"');
    first.kill('SIGKILL');
    const firstExit = await waitForExit(first, 5000);
    expect(firstExit).toEqual({ code: null, signal: 'SIGKILL' });

    // A fresh fixture process opens the exact same mailbox files and invokes
    // NanoClaw's exported host-sweep recovery helper once, then allows one retry.
    const restarted = startWorker('recover', inboundPath, outboundPath);
    const recoveredOutput = await waitForMarker(restarted, 'SPIKE_RESULT=', 20000);
    const recoveredExit = await waitForExit(restarted, 5000);
    expect(recoveredExit).toEqual({ code: 0, signal: null });
    const resultLine = recoveredOutput.split('\n').find((line) => line.startsWith('SPIKE_RESULT='));
    expect(resultLine).toBeDefined();
    const result = JSON.parse(resultLine!.slice('SPIKE_RESULT='.length)) as {
      taskId: string;
      role: string;
      restartRecovered: boolean;
      retries: number;
      terminalStatus: string;
      terminalDeliveries: number;
    };
    expect(result).toEqual({
      taskId,
      role: 'NAIA',
      restartRecovered: true,
      retries: 1,
      terminalStatus: 'completed',
      terminalDeliveries: 1,
    });

    // The terminal-delivery row is a no-effect fixture ledger. It is not a
    // production delivery adapter or proof of duplicate suppression there.
    const verifyDb = new Database(inboundPath, { readonly: true });
    const deliveries = verifyDb.prepare('SELECT task_id, role, attempt FROM spike_terminal_delivery').all();
    verifyDb.close();
    expect(deliveries).toEqual([{ task_id: taskId, role: 'NAIA', attempt: 2 }]);
  }, 30000);
});
