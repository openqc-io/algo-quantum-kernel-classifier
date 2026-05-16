# Quantum Kernel Classifier

Classify data using quantum kernel estimation. Encodes data into quantum states and computes kernel matrix entries via fidelity tests.

## Provenance

This algorithm was ported from the in-image builtin registry in
`vortex-common/vortex_common/algorithm_executor.py` during the
M-DoD-B (Migration Done) phase. The algorithm itself is unchanged;
it now lives in this standalone repo so it ingests through the
canonical catalog sync pipeline (algorithm.json + template.py at a
pinned commit), like every other algorithm.

## Input

```json
{
  "type": "object",
  "required": [],
  "properties": {
    "num_qubits": {
      "type": "integer",
      "description": "Feature map qubits (default 4)"
    },
    "reps": {
      "type": "integer",
      "description": "Feature map repetitions (default 2)"
    }
  }
}
```

## Output

```json
{
  "type": "object",
  "properties": {
    "kernel_alignment": {
      "type": "number"
    },
    "fidelity_samples": {
      "type": "number"
    }
  }
}
```

## License

Apache-2.0 — see [LICENSE](./LICENSE).
