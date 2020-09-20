from src.utils import Subprocess
from src.utils import copy_files
from .index import RunnerMetricConfig, Runner

"""
SourceMeterJava -projectName=MyProject -projectBaseDir=MyProjectDir -resultsDir=Results
"""


class RunnerSourceMeter(Runner):
    def __init__(self, config: RunnerMetricConfig, **kwargs):
        # init
        super().__init__(config)

    def Run(self, project_directory, move_output=False, output_source=None):
        # create the command
        command = "{}/SourceMeterJava -projectName={} -projectBaseDir={} -resultsDir={}".format(
            self.config.metrics_runner_file,
            super().get_output().split("/")[-1],
            project_directory,
            super().get_output(),
        )

        subprocess = Subprocess(command)
        subprocess.Run()
        if move_output:
            copy_files(source=output_source + "*.csv", target=super().output)
