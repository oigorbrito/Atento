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
import { routeAgentMessage } from './modules/agent-to-agent/agent-route.js';
import type { Session } from './types.js';

const roles = ['naia', 'anna', 'apollo'] as const;
type Role = (typeof roles)[number];
type RoleProfile = { agent_group: string; channel_instance: string; provider: string };

let groupByRole: Record<Role, RoleProfile>;
let effectByRole: Record<Role, string>;

let root: string;
let policy: MountPolicy;
let driver: DockerSessionDriver;
const handles = new Map<Role, SessionHandle>();
const fixtures = new Map<Role, string>();
const credentialFixtures = new Map<Role, { spec: SessionSpec; handle: SessionHandle; materialPath: string }>();

function makeSpec(role: Role, stateRoot: string): SessionSpec {
  return {
    key: { installSlug: 'atento-system-probe', agentGroupId: groupByRole[role].agent_group, sessionId: `${role}-session` },
    labels: { 'nanoclaw-group-folder': groupByRole[role].agent_group },
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
        groupScope: groupByRole[role].agent_group,
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

async function waitForRunning(handle: SessionHandle): Promise<void> {
  const deadline = Date.now() + 15_000;
  while (Date.now() < deadline) {
    const status = await handle.status();
    if (status.phase === 'running') return;
    if (status.phase === 'failed') throw new Error(`container failed before running: ${JSON.stringify(status.failure)}`);
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  throw new Error(`container did not reach running state: ${handle.name}`);
}

function dockerExec(role: Role, command: string[]): string {
  const handle = handles.get(role);
  if (!handle) throw new Error(`missing handle for ${role}`);
  return dockerExecHandle(handle, command);
}

describe('Atento three-role mount boundary on the exact NanoClaw pin', () => {
  beforeAll(async () => {
    execFileSync('docker', ['info'], { stdio: 'ignore' });
    const profilePath = process.env.ATENTO_SYSTEM_PROFILE;
    if (!profilePath) throw new Error('ATENTO_SYSTEM_PROFILE must point to the frozen Atento system profile');
    const profile = JSON.parse(readFileSync(profilePath, 'utf8')) as {
      upstream_repo: string;
      upstream_sha: string;
      profile_hash: string;
      policy_hash: string;
      topology: {
        roles: { NAIA: RoleProfile; Anna: RoleProfile; Apollo: RoleProfile };
        role_test_effects: { NAIA: string; Anna: string; Apollo: string };
      };
    };
    expect(profile.upstream_repo).toBe('nanocoai/nanoclaw');
    expect(profile.upstream_sha).toBe('4c1eabd3ddd74cc3d71b1871da857391a9411c8d');
    expect(profile.profile_hash).toBe('c6e815289488daace646e7d9123b2638c6f245eaf4ef4dff357d6b3c50c1d289');
    expect(profile.policy_hash).toBe('02de0f5540c1c638c0553dc8261cfd0e53ffb4727a0636a50a4653d2e15a7132');
    expect(profile.topology.roles.NAIA.agent_group).toBe('atento-naia');
    expect(profile.topology.roles.Anna.agent_group).toBe('atento-anna');
    expect(profile.topology.roles.Apollo.agent_group).toBe('atento-apollo');
    groupByRole = { naia: profile.topology.roles.NAIA, anna: profile.topology.roles.Anna, apollo: profile.topology.roles.Apollo };
    effectByRole = { naia: profile.topology.role_test_effects.NAIA, anna: profile.topology.role_test_effects.Anna, apollo: profile.topology.role_test_effects.Apollo };
    root = mkdtempSync(join(tmpdir(), 'atento-system-chassis-'));
    policy = {
      groupsRoot: join(root, 'groups'),
      dataRoot: join(root, 'data'),
      surfaceRoots: [],
      materialsRoot: join(root, 'materials'),
      gatewayTrustRoot: join(root, 'gateway-trust'),
    };
    for (const role of roles) {
      const groupId = groupByRole[role].agent_group;
      const stateRoot = join(policy.dataRoot, 'v2-sessions', groupId);
      mkdirSync(stateRoot, { recursive: true });
      writeFileSync(join(stateRoot, 'effect.txt'), `inert-effect:${effectByRole[role]}\n`, { mode: 0o600 });
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
      dockerExec(role, ['sh', '-c', `printf 'written:${effectByRole[role]}\\n' >> /workspace/effect.txt`]);
      const own = dockerExec(role, ['cat', '/workspace/effect.txt']).trim();
      expect(own.split(String.fromCharCode(10))).toEqual([`inert-effect:${effectByRole[role]}`, `written:${effectByRole[role]}`]);
      expect(readFileSync(join(fixtures.get(role)!, 'effect.txt'), 'utf8')).toContain(`written:${effectByRole[role]}`);
      for (const other of roles.filter((candidate) => candidate !== role)) {
        expect(own).not.toBe(`inert-effect:${effectByRole[other]}`);
      }
    }
  });

  it('retains each group state root across a driver stop and prepare cycle', async () => {
    for (const role of roles) {
      const previous = handles.get(role)!;
      await previous.stop('atento state-recovery probe');
      const restarted = await driver.prepare(makeSpec(role, fixtures.get(role)!));
      handles.set(role, restarted);
      await restarted.start();
      await waitForRunning(restarted);
      expect(dockerExec(role, ['cat', '/workspace/effect.txt']).trim().split(String.fromCharCode(10))).toEqual([
        `inert-effect:${effectByRole[role]}`,
        `written:${effectByRole[role]}`,
      ]);
    }
  });

  it('resolves role-scoped chat sessions and blocks unregistered native cross-role sends', async () => {
    const db = await initTestDb();
    await runMigrations(db);
    try {
      const createdAt = new Date().toISOString();
      const sessionIds = new Map<Role, string>();
      for (const role of roles) {
        const groupId = groupByRole[role].agent_group;
        const messagingGroupId = groupByRole[role].channel_instance;
        const sessionId = `session-${role}`;
        await createAgentGroup({
          id: groupId,
          name: role,
          folder: groupId,
          agent_provider: groupByRole[role].provider,
          created_at: createdAt,
        });
        await createMessagingGroup({
          id: messagingGroupId,
          channel_type: 'telegram',
          platform_id: messagingGroupId,
          instance: messagingGroupId,
          name: null,
          is_group: 0,
          unknown_sender_policy: 'public',
          created_at: createdAt,
        });
        const session: Session = {
          id: sessionId,
          agent_group_id: groupId,
          messaging_group_id: messagingGroupId,
          thread_id: null,
          agent_provider: groupByRole[role].provider,
          status: 'active',
          container_status: 'running',
          last_active: createdAt,
          created_at: createdAt,
        };
        await createSession(session);
        sessionIds.set(role, sessionId);
      }

      for (const role of roles) {
        const groupId = groupByRole[role].agent_group;
        const ownMessagingGroup = groupByRole[role].channel_instance;
        const own = await findSessionForAgent(groupId, ownMessagingGroup, null);
        expect(own?.id).toBe(sessionIds.get(role));
        expect(own?.agent_provider).toBe(groupByRole[role].provider);
        expect((await getSessionsByAgentGroup(groupId)).map((session) => session.id)).toEqual([sessionIds.get(role)]);

        for (const other of roles.filter((candidate) => candidate !== role)) {
          expect(await findSessionForAgent(groupByRole[other].agent_group, ownMessagingGroup, null)).toBeUndefined();
        }

        if (role === 'naia') {
          await expect(
            routeAgentMessage(
              {
                id: 'atento-unbrokered-native-handoff',
                platform_id: groupByRole.anna.agent_group,
                content: JSON.stringify({ text: 'synthetic cross-role request' }),
                in_reply_to: null,
              },
              {
                id: sessionIds.get(role)!,
                agent_group_id: groupByRole[role].agent_group,
                messaging_group_id: ownMessagingGroup,
                thread_id: null,
                agent_provider: groupByRole[role].provider,
                status: 'active',
                container_status: 'running',
                last_active: createdAt,
                created_at: createdAt,
              },
            ),
          ).rejects.toThrow(/unauthorized agent-to-agent/);
        }
      }
    } finally {
      await closeDb();
    }
  });

  it('keeps synthetic identity material in the per-session auxiliary container', async () => {
    for (const role of roles) {
      const groupId = groupByRole[role].agent_group;
      const materialDir = join(policy.materialsRoot, groupId);
      mkdirSync(materialDir, { recursive: true });
      const materialPath = join(materialDir, 'credential.txt');
      writeFileSync(materialPath, `synthetic-grant:${effectByRole[role]}`, { mode: 0o600 });

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
          groupScope: groupByRole[role].agent_group,
        }],
      });

      const handle = await driver.prepare(spec);
      credentialFixtures.set(role, { spec, handle, materialPath });
      await handle.start();
      await waitForRunning(handle);

      const auxName = auxiliaryContainerName(spec, 'credential-holder');
      const visibleToHolder = execFileSync(
        'docker',
        ['exec', '-i', auxName, 'cat', '/run/session/credential.txt'],
        { encoding: 'utf8' },
      ).trim();
      expect(visibleToHolder).toBe(`synthetic-grant:${effectByRole[role]}`);
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
