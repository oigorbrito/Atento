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
- an integration test spanning authenticated webhook -> enrollment -> host-issued identity.

The Telegram webhook authenticator verifies the configured webhook secret before parsing any actor identity. It binds the accepted user to a trusted configured `bot_account_id`, producing subjects such as `telegram:bot:777000:user:123456`; raw Telegram user IDs are therefore not merged across bot accounts. NanoClaw pairing state and NanoClaw's `owner` role are never consulted.

The helper `issue_execution_identity_for_telegram` intentionally has no caller-supplied role parameter. It resolves the role from the durable Atento mapping and passes that host-owned binding to `IdentityIssuer`.

This is still not a production host. Missing release gates include deploying/configuring the real Telegram webhook endpoint and proving a live provider delivery, production key/enrollment-secret custody and rotation, authorization of revocation callers, the durable run ledger/process supervisor, NanoClaw adapter wiring, approved RTO/RPO targets, and end-to-end execution against the frozen overlay pin.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```
