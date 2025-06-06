from types import SimpleNamespace
from typing import Iterable

try:
    from qiskit_aer import AerSimulator
except Exception:  # pragma: no cover - optional dependency
    AerSimulator = None  # type: ignore


class LocalAerDevice:
    """Wrapper around ``qiskit_aer.AerSimulator`` exposing a minimal interface
    compatible with ``QuantumDevice`` used by metriq-gym."""

    def __init__(self) -> None:
        if AerSimulator is None:
            raise ImportError("qiskit-aer is required for local simulation")
        self._backend = AerSimulator()
        self.id = "aer_simulator"
        self.num_qubits = self._backend.configuration().n_qubits
        self.profile = SimpleNamespace(basis_gates=self._backend.configuration().basis_gates)

    def run(self, circuits: Iterable, shots: int = 1024):
        return self._backend.run(circuits, shots=shots)


def counts_from_job(job) -> list[dict[str, int]]:
    """Extract measurement counts from a qiskit ``Job``."""
    result = job.result()
    counts = []
    for idx in range(len(result.results)):
        counts.append(result.get_counts(idx))
    return counts
