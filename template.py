"""Ported from the in-image builtin registry (was added during
the enrichment phase; this file finishes the migration to a standalone
openqc-io/algo-* repo so the algorithm lives in the catalog like every
other one).

Sandbox: no imports — all logic is pure dict construction on Python
built-ins. See vortex_common.algorithm_executor.validate_template_ast
for the full rule set.
"""


class AlgorithmTemplate:

    def build(self, input_data, ctx):
        backend = ctx.get("backend", "auto") if isinstance(ctx, dict) else "auto"
        return {
            "type": "circuit",
            "backend_id": backend,
            "provider": "vortex",
            "qasm": _build_kernel_circuit(
                input_data.get("num_qubits", 4),
                input_data.get("reps", 2),
            ),
            "shots": 4096,
        }

    def interpret(self, raw_result, input_data):
        result = raw_result
        return {
            "kernel_alignment": _compute_kernel_alignment(result),
            "fidelity_samples": result.get("total_shots", 4096),
        }
