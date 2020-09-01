from typing import NamedTuple


class RunnerMetricConfig(NamedTuple):
    name: str
    metrics_runner_file: str


class Runner:
    def __init__(self, config: RunnerMetricConfig):
        self.config = config

    def Run(self, output_directory):
        pass
