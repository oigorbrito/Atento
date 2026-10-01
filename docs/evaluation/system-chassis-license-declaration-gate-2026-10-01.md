# Frozen-pin license declaration preflight — 2026-10-01

## Scope

This is a read-only eligibility preflight performed while the Atento host-restart/retry gate remains pending. It checks whether a `LICENSE` file is retrievable at the exact frozen source pin for the remaining system cohort. It does not decide legal compatibility, inspect dependency licenses, or qualify a chassis. No code was downloaded or executed.

SelfAgent is excluded because the earlier Gate 1 stopped it as a complete NAIA base at its frozen pin. OpenClaw remains in the fixed system cohort, although it is excluded from the mobile-focused view.

## Results

| Candidate | Frozen pin | `LICENSE` at pin | Observation |
|---|---|---|---|
| NanoClaw | `nanocoai/nanoclaw@4c1eabd3ddd74cc3d71b1871da857391a9411c8d` | FOUND | MIT |
| AI Butler | `LumabyteCo/aibutler@c35d3af20f78f1a71ffe9cae76f8be6c8828fe6c` | FOUND | Apache-2.0 |
| OpenClaw | `openclaw/openclaw@e9571d77e76bd6d35996273d9e8398ad539b26e1` | FOUND | MIT |
| QwenPaw | `agentscope-ai/QwenPaw@777441721aa72db8e380d90e4d0481b05cbfd4cc` | FOUND | Apache-2.0 |
| MindRoom | `mindroom-ai/mindroom@4f3bd2d108a6f9be28174e0f66d78eeecddca386` | FOUND | Apache-2.0 |
| Bob Labs | `boblabs-eu/boblabs@a91d6dad098c8ba6d24436a856556078151db45d` | FOUND | Apache-2.0 |
| Ontheia | `Ontheia/ontheia@70802db61eb16533f55efce3d8785d810223d03b` | FOUND | AGPL-3.0 |
| OpenAkita | `openakita/openakita@5f5b38da728274f0fd06461a481851be7c0bca6a` | FOUND | AGPL-3.0 |
| Clawix | `ClawixAI/clawix@5aee015e0bd793102fba69af486dd6e75df6d802` | NOT_FOUND | `LICENSE`, `LICENSE.md`, `LICENSE.txt`, `COPYING`, and `COPYING.md` were not retrievable at this pin. |
| Memoh | Pin required | NOT_RUN | No immutable pin is recorded for this cohort entry; do not use a floating branch for this result. |
| Letta Code | `letta-ai/letta-code@21daa38a8cdd74f2d03b634c8312253080bacfc1` | FOUND | Apache-2.0 |

```text
LICENSE_FILES_FOUND_AT_FROZEN_PIN = 9/10_PINNED_CANDIDATES
LICENSE_DECLARATION_NOT_FOUND = Clawix
PIN_REQUIRED = Memoh
NEW_HARD_CANDIDATE_ELIMINATIONS = 0
LEGAL_COMPATIBILITY_DECISION = NOT_MADE
```

## Gate result and limits

The gate passes only for the narrow property “a license declaration file exists at the frozen source pin.” Clawix is blocked for license review until the exact pin's repository terms are identified; this is not an elimination. Memoh remains blocked until its pin is frozen. AGPL-3.0 observations are flagged for a project-specific compatibility review, not treated as incompatible or as candidate failures. No legal or product distribution requirements were supplied for this screen.

A future legal-compatibility gate needs a declared deployment/distribution model, whether Atento modifies or redistributes candidate code, and dependency-level license inventory. Do not infer a legal outcome from the short license identifier alone.

## Raw provenance

The source was read through GitHub Contents API at each exact commit. Blob SHAs returned:

- NanoClaw: `e5b4bee92ed2127744cea681fa103521298e3b9a`
- AI Butler: `137985cacb4794a1ae6ed6a8a00c0d82265e4f38`
- OpenClaw: `ebaebf7c416761a32f932ad70ebe5d1d2e214f68`
- QwenPaw: `bb587daba1617c37cb8b783bc5e096bbf438543c`
- MindRoom and Bob Labs: `d645695673349e3947e8e5ae42332d0ac3164cd7`
- Ontheia: `be3f7b28e564e7dd05eaf59d64adba1a4065ac0e`
- OpenAkita: `db1f8c1094da032bcf1ae8d4a2552b02b062418b`
- Letta Code: `e72f5de5dd5610ee3fee7feb791ebff246cc931e`
- Clawix alternate-file probes at the same pin: all 404.

This preflight does not change the frozen system-test sequence or the provisional NanoClaw direction. The restart/retry gate remains pending and `BLOCKED_ADAPTER`; no tests were run against PR #58.
