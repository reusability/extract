from typing import NamedTuple


class RunnerMetricConfig(NamedTuple):
    name: str
    metrics_runner_file: str
    move_output: bool  # todo: remove this


class Runner:
    output: str = None

    def __init__(self, config: RunnerMetricConfig):
        self.config = config

    def Run(self, output_directory, move_output=False, output_source=None):
        pass

    # todo: remove project_directory
    def _generate_metrics(self, project_directory):
        pass

    def set_output(self, output):
        self.output = output

    def get_output(self):
        return self.output
