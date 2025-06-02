from __future__ import annotations

import uuid
from importlib import import_module
from typing import Iterable
from collections.abc import Sequence

from qbraid.runtime import JobStatus
from qbraid.runtime.result_data import GateModelResultData, MeasCount


class LocalJob:
    """Synchronous job object for local simulators."""

    def __init__(self, result_data: GateModelResultData):
        self.id = str(uuid.uuid4())
        self._result_data = result_data

    def status(self) -> JobStatus:
        return JobStatus.COMPLETED

    def result(self) -> type:
        class _Result:
            def __init__(self, data: GateModelResultData):
                self.data = data

        return _Result(self._result_data)


class LocalSimulatorDevice:
    """Wrapper around a Qiskit Aer simulator for local execution."""

    def __init__(self, backend_name: str = "aer_simulator") -> None:
        if backend_name != "aer_simulator":
            raise ValueError(f"Unsupported local simulator '{backend_name}'")
        aer = import_module("qiskit_aer")
        self._backend = aer.AerSimulator()
        self.submitted_jobs: list[LocalJob] = []

    def run(self, circuits: Iterable, shots: int = 1):
        if isinstance(circuits, Sequence) and not isinstance(circuits, (str, bytes)):
            qc_list = list(circuits)
        else:
            qc_list = [circuits]
        jobs: list[LocalJob] = []
        for qc in qc_list:
            result = self._backend.run(qc, shots=shots).result()
            counts = result.get_counts()
            job = LocalJob(GateModelResultData(measurement_counts=MeasCount(counts)))
            self.submitted_jobs.append(job)
            jobs.append(job)
        return jobs if len(jobs) > 1 else jobs[0]
