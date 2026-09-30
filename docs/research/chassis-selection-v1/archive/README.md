# Complete Benchmark Package — Historical Reference

> Historical/reference-only. This directory preserves the exact benchmark package generated during the Atento chassis-selection work. It does not override canonical runtime documentation and contains no instruction to continue execution.

## Integrity

- Original file: `atento_architecture_protocol_v1.zip`
- Bytes: 172098
- SHA-256: `d6c7ec9619fd555f45135693bb609ec5718029d6dc2906ca3a64f1d002f64681`
- ZIP entries: 173
- Base64 parts: 16

## Reconstruct

From this directory:

```bash
cat PACKAGE.b64.part-* | tr -d '\n' | base64 -d > atento_architecture_protocol_v1.zip
sha256sum atento_architecture_protocol_v1.zip
```

The SHA-256 must equal:

`d6c7ec9619fd555f45135693bb609ec5718029d6dc2906ca3a64f1d002f64681`

`FILE_LIST.txt` lists every entry in the preserved package. The package includes protocol/calibration files, candidate evidence packs, parity, probes, executable gates, full-checkout evidence, fork scaffold F0-F5, contract harnesses and handoff/progress artifacts.