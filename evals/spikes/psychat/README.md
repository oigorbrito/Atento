# PsyChat Fork Spike

Branch: `spike/psychat-fork-eval`

Pinned donor:
- repo: https://github.com/wink-wink-wink555/PsyChat
- commit: `5bf6f806e0f30e45b4e1dd72282fd6afd83b66f4`

## Test batch 1

Objective: establish the upstream baseline before any adaptation.

The workflow `.github/workflows/psychat-fork-spike.yml` runs:

1. AtentoEval unit tests;
2. clone of the pinned donor;
3. Python compile check;
4. static Chassis Fitness audit;
5. artifact export to `psychat-static-chassis`.

## Chassis Fitness

This test measures architecture evolvability, not conversational quality.

Current static dimensions:
- routing boundary;
- executor abstraction;
- capability registry;
- structured contracts;
- output validation;
- provider boundary;
- state externalization;
- observability hooks;
- resilience boundary;
- independent safety boundary.

## Next batch

After the static baseline:
- run donor with dependencies;
- execute seed AtentoEval cases;
- add Atento adapters without rewriting donor internals;
- measure files touched to swap provider/executor;
- compare upstream vs adapted vs native vertical slice.
