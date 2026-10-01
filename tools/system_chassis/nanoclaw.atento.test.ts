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
import { auxiliaryContainerName, DockerSessionDriver } from './drivers/docker-driver.js';
import type { MountPolicy, SessionHandle, SessionSpec } from './drivers/types.js';
import { closeDb, createAgentGroup, createMessagingGroup, initTestDb, runMigrations } from './db/index.js';
import { createSession, findSessionForAgent, getSessionsByAgentGroup } from './db/sessions.js';
import type { Session } from './types.js';

const roles = ['naia', 'anna', 'apollo'] as const;
type Role = (typeof roles)[number];

let root: string;
let policy: MountPolicy;
let driver: DockerSessionDriver;
const handles = new Map<Role, SessionHandle>();
const fixtures = new Map<Role, string>();
const credentialFixtures = new Map<Role, { spec: SessionSpec; handle: SessionHandle; materialPath: string }>();

function makeSpec(role: Role, stateRoot: string): SessionSpec {
  return {
    key: { installSlug: 'atento-system-probe', agentGroupId: role, sessionId: `${role}-session` },
    labels: { 'nanoclaw-group-folder': role },
    containers: [{
      role: 'agent',
      image: 'node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1',
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
    runAs: { uid: process.getuid(), gid: process.getgid() },
    stopGraceSeconds: 1,
  };
}

function dockerExecHandle(handle: SessionHandle, command: string[]): string {
  const spec = handle.execSpec(command);
  return execFileSync(spec.bin, spec.argsPlain, { encoding: 'utf8' });
}

function dockerExec(role: Role, command: string[]): string {
  const handle = handles.get(role);
  if (!handle) throw new Error(`missing handle for ${role}`);
  return dockerExecHandle(handle, command);
}

describe('Atento three-role mount boundary on the exact NanoClaw pin', () => {
  beforeAll(async () => {
    execFileSync('docker', ['info'], { stdio: 'ignore' });
    root = mkdtempSync(join(tmpdir(), 'atento-system-chassis-'));
    policy = {
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
      fixtures.set(role, stateRoot);
    }
    driver = new DockerSessionDriver({
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
      const credential = credentialFixtures.get(role);
      if (credential) await credential.handle.stop('atento credential-boundary probe cleanup');
      const handle = handles.get(role);
      if (handle) await handle.stop('atento system-chassis probe cleanup');
    }
    if (root) rmSync(root, { recursive: true, force: true });
  }, 120_000);

  it('keeps role state writable only through that role container mount', () => {
    for (const role of roles) {
      dockerExec(role, ['sh', '-c', `printf 'written:${role}\\n' >> /workspace/effect.txt`]);
      const own = dockerExec(role, ['cat', '/workspace/effect.txt']).trim();
      expect(own.split(String.fromCharCode(10))).toEqual([`inert-effect:${role}`, `written:${role}`]);
      expect(readFileSync(join(fixtures.get(role)!, 'effect.txt'), 'utf8')).toContain(`written:${role}`);
      for (const other of roles.filter((candidate) => candidate !== role)) {
        expect(own).not.toBe(`inert-effect:${other}`);
      }
    }
  });

  it('resolves active chat sessions only inside the owning agent group', async () => {
    const db = await initTestDb();
    await runMigrations(db);
    try {
      const createdAt = new Date().toISOString();
      const sessionIds = new Map<Role, string>();
      for (const role of roles) {
        const messagingGroupId = `channel-${role}`;
        const sessionId = `session-${role}`;
        await createAgentGroup({
          id: role,
          name: role,
          folder: role,
          agent_provider: null,
          created_at: createdAt,
        });
        await createMessagingGroup({
          id: messagingGroupId,
          channel_type: 'telegram',
          platform_id: `atento-${role}-fixture`,
          instance: `probe-${role}`,
          name: null,
          is_group: 0,
          unknown_sender_policy: 'public',
          created_at: createdAt,
        });
        const session: Session = {
          id: sessionId,
          agent_group_id: role,
          messaging_group_id: messagingGroupId,
          thread_id: null,
          agent_provider: null,
          status: 'active',
          container_status: 'running',
          last_active: createdAt,
          created_at: createdAt,
        };
        await createSession(session);
        sessionIds.set(role, sessionId);
      }

      for (const role of roles) {
        const ownMessagingGroup = `channel-${role}`;
        const own = await findSessionForAgent(role, ownMessagingGroup, null);
        expect(own?.id).toBe(sessionIds.get(role));
        expect((await getSessionsByAgentGroup(role)).map((session) => session.id)).toEqual([sessionIds.get(role)]);

        for (const other of roles.filter((candidate) => candidate !== role)) {
          expect(await findSessionForAgent(other, ownMessagingGroup, null)).toBeUndefined();
        }
      }
    } finally {
      await closeDb();
    }
  });

  it('keeps synthetic identity material in the per-session auxiliary container', async () => {
    for (const role of roles) {
      const materialDir = join(policy.materialsRoot, role);
      mkdirSync(materialDir, { recursive: true });
      const materialPath = join(materialDir, 'credential.txt');
      writeFileSync(materialPath, `synthetic-grant:${role}`, { mode: 0o600 });

      const spec = makeSpec(role, fixtures.get(role)!);
      spec.key = { ...spec.key, sessionId: `${role}-credential-probe` };
      spec.networkAccess = {
        endpoint: 'credential-holder',
        target: { kind: 'session-container', role: 'credential-holder' },
      };
      spec.containers.push({
        role: 'credential-holder',
        image: 'node:24-alpine@sha256:ebfe2f90462722a7a4de65e91990e97fe0d401c70e0e762c5b53302f905ec1c1',
        env: {},
        command: ['/bin/sh'],
        args: ['-c', 'sleep 600'],
        mounts: [{
          class: 'identity-material',
          hostPath: materialPath,
          containerPath: '/run/session/credential.txt',
          mode: 'ro',
          groupScope: role,
        }],
      });

      const handle = await driver.prepare(spec);
      credentialFixtures.set(role, { spec, handle, materialPath });
      await handle.start();
      expect(await handle.status()).toEqual({ phase: 'running' });

      const auxName = auxiliaryContainerName(spec, 'credential-holder');
      const visibleToHolder = execFileSync(
        'docker',
        ['exec', '-i', auxName, 'cat', '/run/session/credential.txt'],
        { encoding: 'utf8' },
      ).trim();
      expect(visibleToHolder).toBe(`synthetic-grant:${role}`);
      expect(dockerExecHandle(handle, ['sh', '-c', 'test ! -e /run/session/credential.txt && printf absent']).trim())
        .toBe('absent');

      const agentMounts = JSON.parse(
        execFileSync('docker', ['inspect', '--format', '{{json .Mounts}}', handle.name], { encoding: 'utf8' }),
      ) as Array<{ Source: string; Destination: string; RW: boolean }>;
      expect(agentMounts).toEqual([
        expect.objectContaining({ Source: fixtures.get(role), Destination: '/workspace', RW: true }),
      ]);
      const auxiliaryMounts = JSON.parse(
        execFileSync('docker', ['inspect', '--format', '{{json .Mounts}}', auxName], { encoding: 'utf8' }),
      ) as Array<{ Source: string; Destination: string; RW: boolean }>;
      expect(auxiliaryMounts).toEqual([
        expect.objectContaining({ Source: materialPath, Destination: '/run/session/credential.txt', RW: false }),
      ]);
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
