from src.utils import Subprocess
from src.utils import copy_files
from .index import RunnerMetricConfig, Runner

"""
This function implements the CK runner.

example:
java -jar ck.jar /path/to/direction/<project>
"""


class RunnerCK(Runner):
    def __init__(self, config: RunnerMetricConfig, **kwargs):
        # init
        super().__init__(config)

    # variablesAndFields:False
    def Run(self, project_directory, move_output=False, output_source=None):
        # create the command
        # looking at CK source code, the parse arguments by index not by identifier
        # https://github.com/mauricioaniche/ck/blob/master/src/main/java/com/github/mauricioaniche/ck/Runner.java
        command = "java -jar {} {} false 0 false".format(
            self.config.metrics_runner_file, project_directory
        )
        subprocess = Subprocess(command)
        subprocess.Run()
        if move_output:
            copy_files(source=output_source + "*.csv", target=super().get_output())
