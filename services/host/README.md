# Atento host identity and Telegram enrollment slices

This directory contains host-owned implementation slices for the trusted identity gate.

Implemented here:

- short-lived execution identity issued and verified by the Atento Host Control Plane;
- Atento-owned Telegram enrollment with six-digit challenges, bounded TTL and attempts;
- durable SQLite principal-to-role mapping and audit trail;
- explicit first-principal bootstrap;
- host-configured authorization for later enrollments;
- revocation of a Telegram principal binding;
- Telegram event resolution into the host-owned role before identity issuance.

The Telegram path starts only after the channel adapter has authenticated the Telegram transport and constructed an `AuthenticatedTelegramEvent`. NanoClaw pairing state and NanoClaw's `owner` role are never consulted.

The helper `issue_execution_identity_for_telegram` intentionally has no caller-supplied role parameter. It resolves the role from the durable Atento mapping and passes that host-owned binding to `IdentityIssuer`.

This is still not a production host. Missing release gates include Telegram transport integration itself, production key/enrollment-secret custody and rotation, authorization of revocation callers, the durable run ledger/process supervisor, NanoClaw adapter wiring, approved RTO/RPO targets, and end-to-end execution against the frozen overlay pin.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```
