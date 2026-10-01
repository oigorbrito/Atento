import Database from 'better-sqlite3';
import { afterEach, describe, expect, it } from 'vitest';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { ensureSchema, openInboundDb } from './mailbox/sqlite/session-db.js';
import { getDeliveredIds, markDelivered } from './mailbox/sqlite/session-db.js';

let scratch: string | undefined;

afterEach(() => {
  if (scratch) rmSync(scratch, { recursive: true, force: true });
  scratch = undefined;
});

describe('NanoClaw delivered-ledger reopen spike — disposable component test', () => {
  it('retains the terminal delivery marker and ignores a duplicate write after SQLite reopen', () => {
    scratch = mkdtempSync(join(tmpdir(), 'nanoclaw-delivery-ledger-reopen-'));
    const dbPath = join(scratch, 'inbound.db');
    ensureSchema(dbPath, 'inbound');

    let db = openInboundDb(dbPath);
    markDelivered(db, 'synthetic-outbound-1', 'synthetic-platform-message-1');
    db.close();

    db = openInboundDb(dbPath);
    expect(getDeliveredIds(db)).toEqual(new Set(['synthetic-outbound-1']));

    // Retry the same terminal ID after reopen. The candidate's SQLite helper
    // must preserve the first marker and avoid a second ledger row.
    markDelivered(db, 'synthetic-outbound-1', 'synthetic-platform-message-duplicate');
    const row = db
      .prepare('SELECT message_out_id, platform_message_id, status FROM delivered WHERE message_out_id = ?')
      .get('synthetic-outbound-1') as
      | { message_out_id: string; platform_message_id: string | null; status: string }
      | undefined;
    const count = (db.prepare('SELECT COUNT(*) AS count FROM delivered').get() as { count: number }).count;
    db.close();

    expect(row).toEqual({
      message_out_id: 'synthetic-outbound-1',
      platform_message_id: 'synthetic-platform-message-1',
      status: 'delivered',
    });
    expect(count).toBe(1);
  });
});
