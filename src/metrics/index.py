from typing import NamedTuple


class RunnerMetricConfig(NamedTuple):
    name: str
    project_dir: str
    output_dir: str
    source_code_dir: str


class Runner:
    def __init__(self, config: RunnerMetricConfig):
        self.config = config

    def Run(self):
        pass
