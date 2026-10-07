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
- fail-closed ambiguous-effect recovery: dispatch intent is persisted before the external runtime call, and loss during dispatch, after accepted dispatch, or after a durable effect record enters `RECONCILE_REQUIRED`, never blind retry;
- a NanoClaw runtime adapter bound to approved upstream baseline `d7175d0dee42a1130c17ced09220b983257696a4` (`v2026.10.0-rc.2`);
- cross-platform CLI invocation through `pnpm exec tsx src/cli/client.ts` rather than the Bash-only `bin/ncl` launcher;
- runtime source attestation separating the frozen upstream base pin from an explicitly approved Atento fork head.

The Telegram webhook authenticator verifies the configured webhook secret before parsing any actor identity. It binds the accepted user to a trusted configured `bot_account_id`, producing subjects such as `telegram:bot:777000:user:123456`; raw Telegram user IDs are therefore not merged across bot accounts. NanoClaw pairing state and NanoClaw's `owner` role are never consulted.

The helper `issue_execution_identity_for_telegram` intentionally has no caller-supplied role parameter. It resolves the role from the durable Atento mapping and passes that host-owned binding to `IdentityIssuer`.

This is still not a production host. Missing release gates include deploying/configuring the real Telegram webhook endpoint and proving a live provider delivery, production key/enrollment-secret custody and rotation, authorization of revocation callers, a real process launcher/monitor bound to the ledger, adapter-specific reconciliation against external providers, NanoClaw adapter wiring, approved RTO/RPO targets, and end-to-end execution through the real Atento adapter against the approved RC2 runtime head.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```

### Approved runtime deployment boundary

NanoClaw at approved upstream baseline `d7175d0dee42a1130c17ced09220b983257696a4` is qualified here only through WSL2/Linux + Docker, not native Windows. Its host CLI server uses the local `data/ncl.sock` socket and its agents execute in Linux Docker containers. Production qualification on a Windows workstation therefore requires the approved NanoClaw fork checkout and Docker runtime to run inside WSL2/Linux. This is a deployment prerequisite; native-Windows execution is not claimed by this adapter.
