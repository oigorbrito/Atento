import Database from 'better-sqlite3';
import { registerWebhookHandler, getWebhookStatus, stopWebhookServer } from './webhook-server.js';

const db = new Database(process.env.ATENTO_TEST_DB);
db.exec(`
  CREATE TABLE IF NOT EXISTS outbox (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    payload TEXT NOT NULL
  )
`);

const roleByToken = new Map([
  ['synthetic-naia-token', 'NAIA'],
  ['synthetic-anna-token', 'ANNA'],
  ['synthetic-apollo-token', 'APOLLO'],
]);

registerWebhookHandler('atento-mobile', async (req, res) => {
  if (req.method !== 'GET' || req.url?.split('?')[0] !== '/webhook/atento-mobile/events') {
    res.writeHead(404);
    res.end();
    return;
  }
  const match = /^Bearer (.+)$/.exec(req.headers.authorization || '');
  const role = match ? roleByToken.get(match[1]) : undefined;
  if (!role) {
    res.writeHead(401);
    res.end();
    return;
  }
  const rawCursor = req.headers['last-event-id'] || '0';
  if (!/^\d+$/.test(rawCursor)) {
    res.writeHead(400);
    res.end();
    return;
  }
  const cursor = Number(rawCursor);
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-store',
    Connection: 'close',
  });
  const rows = db.prepare('SELECT id, role, payload FROM outbox WHERE role = ? AND id > ? ORDER BY id')
    .all(role, cursor) as Array<{ id: number; role: string; payload: string }>;
  for (const row of rows) {
    res.write(`id: ${row.id}\nevent: message\ndata: ${JSON.stringify({ role: row.role, payload: row.payload })}\n\n`);
  }
  res.end();
});

const deadline = Date.now() + 5000;
while (!getWebhookStatus()) {
  if (Date.now() > deadline) throw new Error('NanoClaw webhook server did not become ready');
  await new Promise((resolve) => setTimeout(resolve, 10));
}
console.log('READY');

process.once('SIGTERM', () => {
  void stopWebhookServer().finally(() => {
    db.close();
    process.exit(0);
  });
});
