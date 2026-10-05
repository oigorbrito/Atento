# Atento host identity slice

This is the first implementation slice for `SYS-ID-01` (`SOURCE_ID = SRC-ATENTO`,
`ADOPTION_MODE = ATENTO_NATIVE`): short-lived execution identity issued and
validated by the Atento Host Control Plane. A runtime adapter presents the
opaque token to that host boundary; it never receives the HMAC signing key.
Role grants come only from trusted host configuration. The module does not
authenticate users or channels, implement key storage/rotation, provide a
network service, or bind NanoClaw to the Atento product host.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```

The signing key is injected into `IdentityIssuer` and must remain host-side;
production key custody, rotation/revocation, authenticated channel-to-role
mapping, host lifecycle, durable run state, and end-to-end adapter tests remain
release gates.
