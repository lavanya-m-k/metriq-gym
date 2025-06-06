import argparse

from pydantic import BaseModel
from dataclasses import dataclass

from qbraid import GateModelResultData, QuantumDevice, QuantumJob


@dataclass
class BenchmarkData:
    """Stores intermediate data from pre-processing and dispatching."""

    provider_job_ids: list[str]
    # For local simulator backends the execution is synchronous and no provider
    # jobs are created. In this case we store the raw measurement counts so that
    # the results can be processed later during ``poll``.
    #
    # ``local_counts`` cannot have a default value because subclasses of
    # ``BenchmarkData`` add non-default fields. If ``local_counts`` had a default,
    # dataclass would raise a ``TypeError`` when instantiating those subclasses
    # ("non-default argument follows default argument").
    local_counts: list[dict[str, int]] | None


class BenchmarkResult(BaseModel):
    """Stores the final results of the benchmark"""

    pass


class Benchmark[BD: BenchmarkData, BR: BenchmarkResult]:
    def __init__(
        self,
        args: argparse.Namespace,
        params: BaseModel,
    ):
        self.args = args
        self.params: BaseModel = params

    def dispatch_handler(self, device: QuantumDevice) -> BD:
        raise NotImplementedError

    def poll_handler(
        self,
        job_data: BD,
        result_data: list[GateModelResultData],
        quantum_jobs: list[QuantumJob],
    ) -> BR:
        raise NotImplementedError
