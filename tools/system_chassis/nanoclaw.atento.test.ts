/**
 * Atento's bounded system-chassis probe. This intentionally exercises the
 * pinned NanoClaw Docker driver with three isolated, inert role fixtures. It
 * does not start NanoClaw's provider/channel/application runtime.
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';

import { realCli } from './drivers/cli.js';
