# Atento host identity slice

This is the first implementation slice for `SYS-ID-01`: short-lived execution
identity issued by the Atento Host Control Plane and verified by a runtime
adapter. Role grants come only from trusted host configuration. The module
does not authenticate users or channels, implement key storage/rotation,
provide a network service, or bind NanoClaw to the Atento product host.

Run the isolated tests from the repository root:

```sh
PYTHONPATH=services/host python -m unittest discover -s services/host/tests -v
```

The signing key is injected into `IdentityIssuer`; production key custody,
rotation/revocation, authenticated channel-to-role mapping, host lifecycle,
durable run state, and end-to-end adapter tests remain release gates.
