# project.py
from dataclasses import dataclass
from pathlib import Path
from src.utils import Subprocess
from src.utils import make_dir


class Project:
    def __init__(self, name, maven, github, tags):
        # init
        self.name = name
        self.maven: str = maven
        self.github: str = github
        self.tags: [] = tags

        # setup commands and outputs directory
        self._output_directory = "{}/outputs/{}".format(
            str(Path().resolve().parent), self.name
        )
        self._command = "git -C {} clone {}".format(self._output_directory, self.github)

        # setup cloning using subprocess module
        # todo -- remove subprocess init
        self.subprocess = Subprocess(self._command)

    def checkout_version(self, version: str):
        checkout = Subprocess(
            "git -C {}/{} checkout tags/v{}".format(
                self._output_directory, self.name, version
            )
        )
        checkout.Run()

    def setup(self):
        # make the output directory
        make_dir(self._output_directory)

        # run the clone command
        self.subprocess.Run()


@dataclass
class ProjectConfig:
    name: str
    maven: str
    github: str
    tags: []


ProjectConfigScala = ProjectConfig(
    name="scala",
    maven="https://mvnrepository.com/artifact/org.scala-lang/scala-library",
    github="https://github.com/scala/scala.git",
    tags=["2.12.12", "2.13.3", "2.13.2"],
)

ProjectConfigGson = ProjectConfig(
    name="gson",
    maven="https://mvnrepository.com/artifact/com.google.code.gson/gson",
    github="https://github.com/google/gson.git",
    tags=[],
)
