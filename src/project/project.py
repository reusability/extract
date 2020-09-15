# project.py
from dataclasses import dataclass
from pathlib import Path
from src.utils import Subprocess
from src.utils import make_dir
import re


class Project:
    def __init__(self, name, maven, github, releases):
        # init
        self.name = name
        self.maven: str = maven
        self.github: str = github
        self.releases: [] = releases  # refers to Maven releases

        # variable to store github tags
        self.tags: [] = None

        # setup commands and outputs directory
        self.output_directory = "{}/src/outputs/{}".format(
            str(Path().resolve().parent), self.name
        )
        self._command = "git -C {} clone {}".format(self.output_directory, self.github)

        # setup cloning using subprocess module
        # todo -- remove subprocess init
        self.subprocess = Subprocess(self._command)

    def _retrieve_github_tags(self):
        # store all tags in .txt file in same directory as the project
        tags = Subprocess(
            "git -C {}/{} tag > {}/{}.txt".format(
                self.output_directory, self.name, self.output_directory, self.name
            )
        )
        tags.Run()

        # store tags in variable
        with open("{}/{}.txt".format(self.output_directory, self.name), "r") as content:
            # index 0 -> original tag, index 1 -> remove all prefix string
            self.tags = [
                (
                    line.strip(),
                    line[re.search(r"\d", line).start() :].strip(),  # noqa : E203
                )
                for line in content
            ]
        print(self.tags)

        # create empty txt file to store unmatched tags
        Subprocess(
            "touch {}/{}_unmatched.txt".format(self.output_directory, self.name)
        ).Run()

    def checkout_version(self, release: str):

        for tag in self.tags:
            if tag[1] == release:
                checkout = Subprocess(
                    "git -C {}/{} checkout tags/{}".format(
                        self.output_directory, self.name, tag[0]
                    )
                )
                checkout.Run()
                return

        with open(
            "{}/{}_unmatched.txt".format(self.output_directory, self.name), "a"
        ) as file:
            file.write(release)

    def setup(self):
        # make the output directory
        make_dir(self.output_directory)

        # run the clone command
        self.subprocess.Run()
        self._retrieve_github_tags()

    @staticmethod
    def make_dir(path):
        make_dir(path)


@dataclass
class ProjectConfig:
    name: str
    maven: str
    github: str
    releases: []


ProjectConfigScala = ProjectConfig(
    name="scala",
    maven="https://mvnrepository.com/artifact/org.scala-lang/scala-library",
    github="https://github.com/scala/scala.git",
    releases=["2.12.12", "2.13.3", "2.13.2"],
)

ProjectConfigGson = ProjectConfig(
    name="gson",
    maven="https://mvnrepository.com/artifact/com.google.code.gson/gson",
    github="https://github.com/google/gson.git",
    releases=["2.8.4", "2.8.5", "2.8.6"],
)
