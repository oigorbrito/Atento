# Atento host identity and Telegram enrollment slices

This directory contains host-owned implementation slices for the trusted identity gate.

Implemented here:

- short-lived execution identity issued and verified by the Atento Host Control Plane;
- Atento-owned Telegram enrollment with six-digit challenges, bounded TTL and attempts;
- durable SQLite principal-to-role mapping and audit trail;
- explicit first-principal bootstrap;
- host-configured authorization for later enrollments;
- revocation of a Telegram principal binding;
- Telegram webhook transport authentication via the configured `X-Telegram-Bot-Api-Secret-Token` value;
- bot-account + user namespace isolation for Telegram principals;
- Telegram event resolution into the host-owned role before identity issuance;
- an integration test spanning authenticated webhook -> enrollment -> host-issued identity;
- a durable SQLite Host Supervisor ledger with generation fencing, leases, state transitions, stale-worker rejection, restart recovery and terminal states;
- fail-closed ambiguous-effect recovery: a crash after runtime dispatch or a durable effect record enters `RECONCILE_REQUIRED`, never blind retry;
- a NanoClaw runtime adapter using only seams present at frozen upstream pin `3f7e13b591a0c8980242b81ceff4b3f542ef839a`;
- cross-platform CLI invocation through `pnpm exec tsx src/cli/client.ts` rather than the Bash-only `bin/ncl` launcher;
- runtime source attestation separating the frozen upstream base pin from an explicitly approved Atento fork head.

The Telegram webhook authenticator verifies the configured webhook secret before parsing any actor identity. It binds the accepted user to a trusted configured `bot_account_id`, producing subjects such as `telegram:bot:777000:user:123456`; raw Telegram user IDs are therefore not merged across bot accounts. NanoClaw pairing state and NanoClaw's `owner` role are never consulted.

The helper `issue_execution_identity_for_telegram` intentionally has no caller-supplied role parameter. It resolves the role from the durable Atento mapping and passes that host-owned binding to `IdentityIssuer`.

This is still not a production host. Missing release gates include deploying/configuring the real Telegram webhook endpoint and proving a live provider delivery, production key/enrollment-secret custody and rotation, authorization of revocation callers, a real process launcher/monitor bound to the ledger, adapter-specific reconciliation against external providers, NanoClaw adapter wiring, approved RTO/RPO targets, and end-to-end execution against the frozen overlay pin.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```

### Frozen-pin deployment boundary

NanoClaw at upstream base pin `3f7e13b591a0c8980242b81ceff4b3f542ef839a` documents Windows support through WSL2, not native Windows. Its host CLI server uses the local `data/ncl.sock` socket and its agents execute in Linux Docker containers. Production qualification on a Windows workstation therefore requires the approved NanoClaw fork checkout and Docker runtime to run inside WSL2/Linux. This is a deployment prerequisite; native-Windows execution is not claimed by this adapter.
