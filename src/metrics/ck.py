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

        # create the command
        self._command = "java -jar {} {}".format(
            self.config.source_code_dir, self.config.project_dir
        )
        self.subprocess = Subprocess(self._command)

    def Run(self):
        self.subprocess.Run()

    def move_output(self, source):
        copy_files(source=source + "*.csv", target=self.config.output_dir)
