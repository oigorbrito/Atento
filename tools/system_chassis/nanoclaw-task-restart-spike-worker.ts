import Database from 'better-sqlite3';
import { _resetStuckProcessingRowsForTesting } from './host-sweep.js';
import { wrapSqliteInbound, wrapSqliteOutbound } from './mailbox/sqlite/index.js';
import { openInboundDb } from './mailbox/sqlite/session-db.js';

const inboundPath = process.env.SPIKE_INBOUND_DB;
const outboundPath = process.env.SPIKE_OUTBOUND_DB;
if (!inboundPath || !outboundPath) throw new Error('SPIKE_INBOUND_DB and SPIKE_OUTBOUND_DB are required');

const inboundRaw = openInboundDb(inboundPath);
const outboundRaw = new Database(outboundPath);
const inbound = wrapSqliteInbound(inboundRaw);
const outbound = wrapSqliteOutbound(outboundRaw);
const taskId = 'naia-restart-retry-spike-task';
const role = inboundRaw.prepare('SELECT role FROM spike_task_owner WHERE task_id = ?').get(taskId) as
  | { role: string }
  | undefined;
if (role?.role !== 'NAIA') throw new Error(`role binding missing or changed: ${role?.role ?? 'none'}`);

function taskRow() {
  return inboundRaw.prepare('SELECT id, kind, status, tries, process_after FROM messages_in WHERE id = ?').get(taskId) as
    | { id: string; kind: string; status: string; tries: number; process_after: string | null }
    | undefined;
}

const mode = process.argv[2];
if (mode === 'claim') {
  const row = taskRow();
  if (!row || row.kind !== 'task' || row.status !== 'pending') throw new Error('due task was not pending at claim');
  outboundRaw
    .prepare('INSERT INTO processing_ack (message_id, status, status_changed) VALUES (?, ?, ?)')
    .run(taskId, 'processing', new Date().toISOString());
  process.stdout.write(`SPIKE_CLAIMED=${JSON.stringify({ taskId, role: role.role, status: 'processing' })}\n`);
  // The parent sends SIGKILL at the exact post-claim/pre-terminal-ack point.
  setInterval(() => undefined, 1000);
} else if (mode === 'recover') {
  const before = taskRow();
  const orphan = outbound.getProcessingClaims().find((claim) => claim.messageId === taskId);
  if (!before || !orphan) throw new Error('restart did not find the persisted claimed task');

  _resetStuckProcessingRowsForTesting(
    inbound,
    outbound,
    {
      id: 'naia-system-task-session',
      agent_group_id: 'atento-naia',
      messaging_group_id: null,
      thread_id: 'system:tasks:naia-restart-retry-spike-task',
      agent_provider: null,
      status: 'active',
      container_status: 'stopped',
      last_active: null,
      created_at: new Date().toISOString(),
    } as never,
    'container not running',
  );

  const recoveryDeadline = Date.now() + 12_000;
  let row = taskRow();
  if (!row || row.tries !== 1 || !row.process_after) throw new Error('candidate recovery did not schedule exactly one retry');
  while (Date.parse(row.process_after) > Date.now() && Date.now() < recoveryDeadline) {
    await new Promise((resolve) => setTimeout(resolve, Math.min(100, Date.parse(row.process_after!) - Date.now())));
    row = taskRow();
    if (!row) throw new Error('task disappeared during retry backoff');
  }
  if (Date.parse(row.process_after!) > Date.now()) throw new Error('retry backoff exceeded spike bound');

  // One inert retry: persist the candidate mailbox claim, then a synthetic
  // terminal effect in the disposable harness (no channel/provider is called).
  outboundRaw
    .prepare('INSERT INTO processing_ack (message_id, status, status_changed) VALUES (?, ?, ?)')
    .run(taskId, 'processing', new Date().toISOString());
  inboundRaw
    .prepare('INSERT OR IGNORE INTO spike_terminal_delivery (task_id, role, attempt) VALUES (?, ?, ?)')
    .run(taskId, role.role, row.tries + 1);
  outboundRaw
    .prepare('UPDATE processing_ack SET status = ?, status_changed = ? WHERE message_id = ?')
    .run('completed', new Date().toISOString(), taskId);
  inbound.applyProcessingAcks(outbound.getTerminalProcessingAcks());

  const finalRow = taskRow();
  const terminalDeliveries = inboundRaw
    .prepare('SELECT COUNT(*) AS count FROM spike_terminal_delivery WHERE task_id = ?')
    .get(taskId) as { count: number };
  const result = {
    taskId,
    role: role.role,
    restartRecovered: true,
    retries: finalRow?.tries,
    terminalStatus: finalRow?.status,
    terminalDeliveries: terminalDeliveries.count,
  };
  process.stdout.write(`SPIKE_RESULT=${JSON.stringify(result)}\n`);
  inboundRaw.close();
  outboundRaw.close();
} else {
  throw new Error(`unknown worker mode: ${mode}`);
}
