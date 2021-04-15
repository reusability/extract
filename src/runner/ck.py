# general
# utils.py
from src.utils import Subprocess, Logger
from src.utils import copy_files

# metrics.py
from .index import RunnerConfig, Runner

"""
This function implements the CK runner.

example:
java -jar ck.jar /path/to/direction/<project>
"""


class RunnerCK(Runner):
    def __init__(self, config: RunnerConfig, logger: Logger):
        # init
        super().__init__(config)
        self.logger = logger
        self.logger.l.info("successfully initiated ck runner")

    # variablesAndFields:False
    def Run(self, project_directory, move_output=False, output_source=None):
        # build metrics
        self._generate_metrics(project_directory)

        # move output
        if move_output:
            self._move_output(output_source)

    def _generate_metrics(self, project_directory):
        # create the command
        # looking at CK source code, the parse arguments by index not by identifier
        # https://github.com/mauricioaniche/ck/blob/master/src/main/java/com/github/mauricioaniche/ck/Runner.java
        command = "java -jar {} {} false 0 false".format(
            self.config.metrics_runner_file, project_directory
        )

        # run
        subprocess = Subprocess(command)
        subprocess.Run()

    def _move_output(self, output_source):
        copy_files(source=output_source + "*.csv", target=self.get_output())


RunnerMetricConfigCK = RunnerConfig(
    name="CK", metrics_runner_file="utils/jar/ck.jar", move_output=True
)
