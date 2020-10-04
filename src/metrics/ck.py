# general
# utils.py
from src.utils import Subprocess
from src.utils import copy_files

# metrics.py
from .index import RunnerMetricConfig, Runner

"""
This function implements the CK runner.

example:
java -jar ck.jar /path/to/direction/<project>
"""


class RunnerCK(Runner):
    def __init__(self, config: RunnerMetricConfig):
        # init
        super().__init__(config)

    def Run(self, project_directory, move_output=False, output_source=None):
        # build metrics
        self._generate_metrics(project_directory)

        # move output
        if move_output:
            self._move_output(output_source)

    def _generate_metrics(self, project_directory):
        # create command
        command = "java -jar {} {}".format(
            self.config.metrics_runner_file, project_directory
        )

        # run
        subprocess = Subprocess(command)
        subprocess.Run()

    def _move_output(self, output_source):
        copy_files(source=output_source + "*.csv", target=self.get_output())


RunnerMetricConfigCK = RunnerMetricConfig(
    name="CK", metrics_runner_file="utils/jar/ck.jar", move_output=True
)
