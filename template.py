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


# ── helpers restored from the retired in-image builtin registry (18187b8^) ──


def _build_kernel_circuit(num_qubits: int = 4, reps: int = 2) -> str:
    """Build a quantum kernel estimation circuit (ZZ feature map + inverse)."""
    lines = [
        "OPENQASM 2.0;",
        'include "qelib1.inc";',
        f"qreg q[{num_qubits}];",
        f"creg c[{num_qubits}];",
        "// Data encoding (ZZ feature map)",
    ]
    for _ in range(reps):
        for i in range(num_qubits):
            lines.append(f"h q[{i}];")
            lines.append(f"rz(0.5) q[{i}];")
        for i in range(num_qubits - 1):
            lines.append(f"cx q[{i}],q[{i+1}];")
            lines.append(f"rz(0.3) q[{i+1}];")
            lines.append(f"cx q[{i}],q[{i+1}];")
    # Inverse for fidelity test
    lines.append("// Inverse encoding (fidelity test)")
    for _ in range(reps):
        for i in range(num_qubits - 2, -1, -1):
            lines.append(f"cx q[{i}],q[{i+1}];")
            lines.append(f"rz(-0.3) q[{i+1}];")
            lines.append(f"cx q[{i}],q[{i+1}];")
        for i in range(num_qubits - 1, -1, -1):
            lines.append(f"rz(-0.5) q[{i}];")
            lines.append(f"h q[{i}];")
    for i in range(num_qubits):
        lines.append(f"measure q[{i}] -> c[{i}];")
    return "\n".join(lines)


def _compute_kernel_alignment(result: dict) -> float:
    """Estimate kernel alignment from measurement result."""
    counts = result.get("counts", {})
    total = sum(counts.values()) if counts else 1
    first_key = list(counts)[0] if counts else "0"  # sandbox has no next/iter
    zero_state = counts.get("0" * len(first_key), 0)
    return zero_state / total if total > 0 else 0.0
