import types
from unittest.mock import MagicMock

import metriq_gym.local_simulator as ls


def make_backend(monkeypatch):
    backend = MagicMock()
    res = MagicMock()
    res.get_counts.return_value = {"00": 1}
    backend.run.return_value.result.return_value = res
    aer_mod = types.SimpleNamespace(AerSimulator=MagicMock(return_value=backend))
    monkeypatch.setattr(ls, "import_module", lambda _: aer_mod)
    return backend


def test_local_job_status():
    job = ls.LocalJob(ls.GateModelResultData(measurement_counts=ls.MeasCount({})))
    assert job.status() == ls.JobStatus.COMPLETED


def test_local_simulator_run(monkeypatch):
    backend = make_backend(monkeypatch)
    device = ls.LocalSimulatorDevice()
    job = device.run(MagicMock(), shots=10)
    assert isinstance(job, ls.LocalJob)
    assert backend.run.called
