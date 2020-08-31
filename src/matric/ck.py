from src.utils import Subprocess
from src.utils import copy_files
from .index import MetricConfig


class CK:
    """
    example:
    java -jar ck-0.6.3-SNAPSHOT-jar-with-dependencies.jar /Users/ahmedalasifer/Desktop/FIT4003/scala
    """

    def __init__(self, metric_config: MetricConfig, **kwargs):
        self.config = metric_config
        self._command = "java -jar {} {}".format(
            self.config.source_code_dir, self.config.project_dir
        )
        self.subprocess = Subprocess(self._command)

    def run_ck(self):
        self.subprocess.run()

    def move_output(self, source):
        copy_files(source=source + "*.csv", target=self.config.output_dir)
