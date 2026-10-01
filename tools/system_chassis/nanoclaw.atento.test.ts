/**
 * Atento's bounded system-chassis probe. This intentionally exercises the
 * pinned NanoClaw Docker driver with three isolated, inert role fixtures. It
 * does not start NanoClaw's provider/channel/application runtime.
 */
import { execFileSync } from 'node:child_process';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';

import { realCli } from './drivers/cli.js';
import { DockerSessionDriver } from './drivers/docker-driver.js';
import type { MountPolicy, SessionHandle, SessionSpec } from './drivers/types.js';

const roles = ['naia', 'anna', 'apollo'] as const;
type Role = (typeof roles)[number];

let root: string;
const handles = new Map<Role, SessionHandle>();
const fixtures = new Map<Role, string>();

function makeSpec(role: Role, stateRoot: string): SessionSpec {
  return {
    key: { installSlug: 'atento-system-probe', agentGroupId: role, sessionId: `${role}-session` },
    labels: { 'nanoclaw-group-folder': role },
    containers: [{
      role: 'agent',
      image: 'node:24-alpine',
      env: { TZ: 'UTC' },
      command: ['/bin/sh'],
      args: ['-c', 'sleep 600'],
      mounts: [{
        class: 'group-state',
        hostPath: stateRoot,
        containerPath: '/workspace',
        mode: 'rw',
        groupScope: role,
      }],
    }],
    network: 'none',
    networkAccess: { endpoint: 'unused', target: { kind: 'host' } },
    hardening: 'standard',
    resources: { pidsLimit: 256 },
    runtimeTier: 'container',
    stopGraceSeconds: 1,
  };
}

function dockerExec(role: Role, command: string[]): string {
  const handle = handles.get(role);
  if (!handle) throw new Error(`missing handle for ${role}`);
  const spec = handle.execSpec(command);
  return execFileSync(spec.bin, spec.argsPlain, { encoding: 'utf8' });
}

describe('Atento three-role mount boundary on the exact NanoClaw pin', () => {
  beforeAll(async () => {
    execFileSync('docker', ['info'], { stdio: 'ignore' });
    root = mkdtempSync(join(tmpdir(), 'atento-system-chassis-'));
    const policy: MountPolicy = {
      groupsRoot: join(root, 'groups'),
      dataRoot: join(root, 'data'),
      surfaceRoots: [],
      materialsRoot: join(root, 'materials'),
      gatewayTrustRoot: join(root, 'gateway-trust'),
    };
    for (const role of roles) {
      const stateRoot = join(policy.dataRoot, 'v2-sessions', role);
      mkdirSync(stateRoot, { recursive: true });
      writeFileSync(join(stateRoot, 'effect.txt'), `inert-effect:${role}\n`, { mode: 0o600 });
      execFileSync('chown', ['-R', '1000:1000', stateRoot]);
      fixtures.set(role, stateRoot);
    }
    const driver = new DockerSessionDriver({
      ...policy,
      cli: realCli('docker'),
      networkArgsFor: () => ['--network', 'none'],
    });
    for (const role of roles) {
      const handle = await driver.prepare(makeSpec(role, fixtures.get(role)!));
      handles.set(role, handle);
      await handle.start();
    }
    for (const role of roles) expect(await handles.get(role)!.status()).toEqual({ phase: 'running' });
  }, 120_000);

  afterAll(async () => {
    for (const role of roles) {
      const handle = handles.get(role);
      if (handle) await handle.stop('atento system-chassis probe cleanup');
    }
    if (root) rmSync(root, { recursive: true, force: true });
  }, 120_000);

  it('keeps role state writable only through that role container mount', () => {
    for (const role of roles) {
      dockerExec(role, ['sh', '-c', `printf 'written:${role}\\n' >> /workspace/effect.txt`]);
      const own = dockerExec(role, ['cat', '/workspace/effect.txt']).trim();
      expect(own.split(/\\r?\\n/)).toEqual([`inert-effect:${role}`, `written:${role}`]);
      expect(readFileSync(join(fixtures.get(role)!, 'effect.txt'), 'utf8')).toContain(`written:${role}`);
      for (const other of roles.filter((candidate) => candidate !== role)) {
        expect(own).not.toBe(`inert-effect:${other}`);
      }
    }
  });

  it('realizes one role-scoped state source per container and no host secret mounts', () => {
    for (const role of roles) {
      const handle = handles.get(role)!;
      const mounts = JSON.parse(
        execFileSync('docker', ['inspect', '--format', '{{json .Mounts}}', handle.name], { encoding: 'utf8' }),
      ) as Array<{ Source: string; Destination: string; RW: boolean }>;
      expect(mounts).toEqual([
        expect.objectContaining({ Source: fixtures.get(role), Destination: '/workspace', RW: true }),
      ]);
      expect(dockerExec(role, ['sh', '-c', 'test ! -e /run/secrets/atento-synthetic && printf absent']).trim())
        .toBe('absent');
    }
  });
});
