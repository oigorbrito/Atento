import Database from 'better-sqlite3';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawn, type ChildProcess } from 'node:child_process';
import { createServer } from 'node:net';

const roles = [
  { name: 'NAIA', token: 'synthetic-naia-token' },
  { name: 'ANNA', token: 'synthetic-anna-token' },
  { name: 'APOLLO', token: 'synthetic-apollo-token' },
] as const;

let dir: string;
let dbPath: string;
let port: number;
let db: Database.Database;
let worker: ChildProcess | undefined;

async function unusedPort(): Promise<number> {
  return await new Promise((resolve, reject) => {
    const server = createServer();
    server.once('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const address = server.address();
      if (!address || typeof address === 'string') return reject(new Error('No TCP port allocated'));
      const selected = address.port;
      server.close((error) => error ? reject(error) : resolve(selected));
    });
  });
}

async function waitForPortRelease(selectedPort: number, timeoutMs: number): Promise<number> {
  const startedAt = Date.now();
  while (Date.now() - startedAt < timeoutMs) {
    const available = await new Promise<boolean>((resolve, reject) => {
      const probe = createServer();
      probe.once('error', () => resolve(false));
      probe.listen(selectedPort, '0.0.0.0', () => {
        probe.close((error) => error ? reject(error) : resolve(true));
      });
    });
    if (available) return Date.now() - startedAt;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`webhook port ${selectedPort} was not bindable within ${timeoutMs}ms after worker SIGKILL`);
}

async function waitReady(child: ChildProcess): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    let output = '';
    const timeout = setTimeout(() => reject(new Error(`worker readiness timeout; output=${output}`)), 7000);
    child.stdout?.on('data', (chunk: Buffer) => {
      output += chunk.toString();
      if (output.includes('READY')) {
        clearTimeout(timeout);
        resolve();
      }
    });
    child.stderr?.on('data', (chunk: Buffer) => { output += chunk.toString(); });
    child.once('exit', (code) => {
      clearTimeout(timeout);
      reject(new Error(`worker exited before ready (code=${code}); output=${output}`));
    });
  });
}

function startWorker(): ChildProcess {
  const child = spawn(process.execPath, ['--import', 'tsx', 'src/system-chassis-mobile-replay-worker.ts'], {
    cwd: process.cwd(),
    env: { ...process.env, WEBHOOK_PORT: String(port), ATENTO_TEST_DB: dbPath },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  worker = child;
  return child;
}

async function stopWorker(): Promise<void> {
  if (!worker || worker.exitCode !== null) return;
  const child = worker;
  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => {
      child.kill('SIGKILL');
      reject(new Error('worker did not stop after SIGTERM'));
    }, 5000);
    child.once('exit', (code) => {
      clearTimeout(timeout);
      if (code !== 0) reject(new Error(`worker exited with code ${code}`));
      else resolve();
    });
    child.kill('SIGTERM');
  });
  worker = undefined;
}

async function crashWorker(): Promise<void> {
  if (!worker || worker.exitCode !== null) return;
  const child = worker;
  await new Promise<void>((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('worker did not terminate after SIGKILL')), 5000);
    child.once('exit', (code, signal) => {
      clearTimeout(timeout);
      if (code !== null || signal !== 'SIGKILL') {
        reject(new Error(`expected SIGKILL exit, got code=${code}, signal=${signal}`));
      } else {
        resolve();
      }
    });
    child.kill('SIGKILL');
  });
  worker = undefined;
}

async function fetchEvents(token: string, lastEventId: number): Promise<Array<{ id: number; role: string; payload: string }>> {
  const response = await fetch(`http://127.0.0.1:${port}/webhook/atento-mobile/events`, {
    headers: { Authorization: `Bearer ${token}`, 'Last-Event-ID': String(lastEventId) },
  });
  expect(response.status).toBe(200);
  expect(response.headers.get('content-type')).toContain('text/event-stream');
  const body = await response.text();
  const parsed: Array<{ id: number; role: string; payload: string }> = [];
  const blocks = body.trim().split(/\n\n/).filter(Boolean);
  for (const block of blocks) {
    const id = Number(/^id: (\d+)$/m.exec(block)?.[1]);
    const data = /^data: (.+)$/m.exec(block)?.[1];
    if (id && data) parsed.push({ id, ...JSON.parse(data) as { role: string; payload: string } });
  }
  return parsed;
}

beforeAll(async () => {
  dir = mkdtempSync(join(tmpdir(), 'nanoclaw-mobile-replay-'));
  dbPath = join(dir, 'outbox.sqlite');
  port = await unusedPort();
  db = new Database(dbPath);
  db.exec('CREATE TABLE outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, role TEXT NOT NULL, payload TEXT NOT NULL)');
  for (const role of roles) db.prepare('INSERT INTO outbox (role, payload) VALUES (?, ?)').run(role.name, `${role.name}-reply-1`);
  await waitReady(startWorker());
});

afterAll(async () => {
  await stopWorker();
  db?.close();
  if (dir) rmSync(dir, { recursive: true, force: true });
});

describe('NanoClaw mobile SSE replay — disposable feasibility probe', () => {
  it('resumes durable role-scoped replies after one real worker-process restart', async () => {
    const firstDelivery = new Map<string, number>();
    for (const role of roles) {
      const events = await fetchEvents(role.token, 0);
      expect(events).toHaveLength(1);
      expect(events[0].role).toBe(role.name);
      expect(events[0].payload).toBe(`${role.name}-reply-1`);
      firstDelivery.set(role.name, events[0].id);
    }

    for (const role of roles) db.prepare('INSERT INTO outbox (role, payload) VALUES (?, ?)').run(role.name, `${role.name}-reply-2`);
    await crashWorker();
    // Measure bounded OS socket release, then restart on the candidate's fixed port.
    const releaseWaitMs = await waitForPortRelease(port, 5000);
    expect(releaseWaitMs).toBeLessThan(5000);
    await waitReady(startWorker());

    for (const role of roles) {
      const events = await fetchEvents(role.token, firstDelivery.get(role.name)!);
      expect(events).toHaveLength(1);
      expect(events[0].role).toBe(role.name);
      expect(events[0].payload).toBe(`${role.name}-reply-2`);
      expect(events[0].id).toBeGreaterThan(firstDelivery.get(role.name)!);
    }

    const unauthorized = await fetch(`http://127.0.0.1:${port}/webhook/atento-mobile/events`, {
      headers: { Authorization: 'Bearer unknown-synthetic-token', 'Last-Event-ID': '0' },
    });
    expect(unauthorized.status).toBe(401);
  }, 20000);
});
