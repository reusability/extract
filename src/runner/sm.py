# general
# utils.py
from src.utils import Subprocess
from src.utils import copy_files

# metrics.py
from .index import RunnerConfig
from .index import Runner

"""
SourceMeterJava -projectName=MyProject -projectBaseDir=MyProjectDir -resultsDir=Results
"""


class RunnerSM(Runner):
    def __init__(self, config: RunnerConfig):
        # init
        super().__init__(config)

    def Run(self, project_directory, move_output=False, output_source=None):
        # build metrics
        self._generate_metrics(project_directory)

        # move output
        if move_output:
            self._move_output(output_source)

    def _generate_metrics(self, project_directory):
        # create the command
        command = "{}/SourceMeterJava -projectName={} -projectBaseDir={} -resultsDir={}".format(
            self.config.metrics_runner_file,
            self.get_output().split("/")[-1],
            project_directory,
            self.get_output(),
        )

        # run
        subprocess = Subprocess(command)
        subprocess.Run()

    def _move_output(self, output_source):
        copy_files(source=output_source + "*.csv", target=self.output)


RunnerMetricConfigSM = RunnerConfig(
    name="SM", metrics_runner_file="path/to/sm", move_output=False
)
