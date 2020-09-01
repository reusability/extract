from src.utils import Subprocess
from src.utils import copy_files
from .index import RunnerMetricConfig, Runner

"""
This function implements the CK runner.

example:
java -jar ck-0.6.3-SNAPSHOT-jar-with-dependencies.jar /path/to/direction/<project>
"""


class RunnerCK(Runner):
    def __init__(self, config: RunnerMetricConfig, **kwargs):
        # init
        super().__init__(config)

    def Run(self, project_directory):
        # create the command
        command = "java -jar {} {}".format(
            self.config.metrics_runner_file, project_directory
        )
        subprocess = Subprocess(command)
        subprocess.Run()

    @staticmethod
    def move_output(source, output):
        copy_files(source=source + "*.csv", target=output)
