# Common system-chassis runner

The runner consumes the frozen 11-candidate manifest at `evals/config/system_chassis_cohort_v1.json`. It processes candidates serially in manifest order and verifies the exact donor SHA before invoking any adapter. It never treats missing adapters, checkouts, observations, or evidence as a candidate failure.

## Adapter process contract

An adapter is a candidate-specific translation layer. It must exercise the pinned runtime with the manifest's same synthetic NAIA, Anna, and Apollo fixtures. It may translate APIs and collect observations; it may not choose a gate result or change the common expected outcomes.

The runner invokes the registered command with a JSON request on stdin. The request includes candidate identity/pin, the three-role profile, frozen assertion cases, the artifact directory, and explicit synthetic-only/no-live-provider constraints. The runner passes only `PATH` and UTF-8 encoding through the subprocess environment; it does not forward provider credentials or other ambient secrets.

The adapter emits one JSON object on stdout:

```json
{
  "protocol_version": 1,
  "candidate_id": "candidate-id",
  "upstream_sha": "40-character-pinned-sha",
  "adapter_id": "stable-adapter-id",
  "adapter_version": "source-revision",
  "observations": {
    "SYS-MEM-01": {
      "own_marker_read": {
        "observed": [{"role": "NAIA", "outcome": "FOUND"}],
        "evidence_file": "raw/memory.json"
      }
    }
  },
  "evidence": [{"path": "raw/memory.json"}]
}
```

The example is structural only. A real adapter must emit every required case, with the same JSON type as the common oracle. It must write raw, synthetic-only evidence below the supplied artifact directory and reference each file from the observations. The runner validates paths and records SHA-256 hashes. It computes assertion outcomes from frozen expected values; an adapter-supplied `PASS` or `FAIL` field is ignored.

## Outcomes

- `PASS_WITH_SCOPE`: every required case matched the common oracle and has a verified evidence file.
- `FAIL_WITH_SCOPE`: an observed case contradicted the frozen oracle; this is a path-level result, not family elimination.
- `BLOCKED`: pin, execution, protocol, or evidence could not be verified.
- `BLOCKED_ENVIRONMENT`: checkout or execution environment is unavailable.
- `BLOCKED_ADAPTER`: no adapter is registered or the adapter cannot be launched.

No adapter is registered for this cohort yet. Running the runner now is a contract check that returns eleven `BLOCKED_ADAPTER` rows. That output is not a candidate test result. Adapters should be implemented only where an existing candidate surface supports the contract without building a new Atento product runtime or making broad donor changes; otherwise retain `BLOCKED_ADAPTER`.

## Local contract checks

```bash
python -m unittest discover -s tools/system_chassis -p 'test_common_runner.py' -v
python tools/system_chassis/common_runner.py \
  --manifest evals/config/system_chassis_cohort_v1.json \
  --atento-sha <atento-commit-sha> \
  --checkout-root <pinned-checkout-root> \
  --adapter-root tools/system_chassis/adapters \
  --artifact-root <run-artifact-directory>
```

The unit tests exercise only runner contract behavior. They do not qualify any candidate.
