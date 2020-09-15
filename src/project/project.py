# project.py
from dataclasses import dataclass
from pathlib import Path
from src.utils import Subprocess
from src.utils import make_dir
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re as regex


class Project:
    def __init__(self, name, maven, github):
        # init
        self.name = name
        self.maven: str = maven
        self.github: str = github
        self._releases: [] = []  # refers to Maven releases

        # variable to store github tags
        self._tags: [] = None

        self.matched_maven_gh: [Match_Maven_GH] = []

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
            "git -C {}/{} tag > {}/{}_gh_tags.txt".format(
                self.output_directory, self.name, self.output_directory, self.name
            )
        )
        tags.Run()

        # store tags in variable
        with open(
            "{}/{}_gh_tags.txt".format(self.output_directory, self.name), "r"
        ) as content:
            # index 0 -> original tag,
            # index 1 -> remove prefix string
            self._tags = [
                (
                    line.strip(),
                    line[regex.search(r"\d", line).start() :].strip(),  # noqa : E203
                )
                for line in content
            ]
            self._tags.reverse()

        # create empty txt file to store unmatched tags
        Subprocess(
            "touch {}/{}_unmatched.txt".format(self.output_directory, self.name)
        ).Run()

    def checkout_version(self, gh_tag: str):

        checkout = Subprocess(
            "git -C {}/{} checkout tags/{}".format(
                self.output_directory, self.name, gh_tag
            )
        )
        checkout.Run()

    def _maven_reuse(self):
        page = requests.get(self.maven)

        # load html page
        soup = BeautifulSoup(page.content, "html.parser")

        data = []
        table = soup.find("table", attrs={"class": "grid versions"})
        table_body = table.find_all("tbody")

        # loop over the releases table: for each major release
        for t in table_body:
            rows = t.find_all("tr")
            # for each minor release
            for row in rows:
                cols = row.find_all("td")
                minor_releases = []
                # for each cell
                for element in cols:
                    cell_data = element.text.strip()
                    try:
                        # 'rowspan' --> means this cell is for major release. e.g 4.X.X
                        data.append(["main", cell_data, int(element["rowspan"]) - 1])
                    except Exception as error:  # noqa : F841
                        # if the cell is not 'rowspan', it means it stores the actual release. e.g 4.2.1
                        minor_releases.append(cell_data)
                data.append(minor_releases)

        # write the data to .csv file
        data_frame = {"version": [], "usage": []}
        for d in data:
            if len(d) == 4:
                data_frame["version"].append(d[0])
                data_frame["usage"].append(int(d[2].replace(",", "")))
                self._releases.append(d[0])

        df = pd.DataFrame(data_frame)
        # .csv format: release number, usage
        df.to_csv(
            "{}/{}_maven_reuse.csv".format(self.output_directory, self.name),
            index=False,
            header=False,
        )

    def _match_maven_release_gh_tags(self):
        for release in self._releases:
            try:
                gh_tag = [i[1] for i in self._tags].index(release)
                self.matched_maven_gh.append(
                    Match_Maven_GH(gh_tag=self._tags[gh_tag][0], maven_release=release)
                )
            except ValueError as error:  # noqa : F841
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

        # run maven_reuse
        # TODO: move this to subprocess
        self._maven_reuse()

        # match maven release with GH tags
        self._match_maven_release_gh_tags()

    @staticmethod
    def make_dir(path):
        make_dir(path)


@dataclass
class ProjectConfig:
    name: str
    maven: str
    github: str


@dataclass
class Match_Maven_GH:
    gh_tag: str
    maven_release: str


ProjectConfigScala = ProjectConfig(
    name="scala",
    maven="https://mvnrepository.com/artifact/org.scala-lang/scala-library",
    github="https://github.com/scala/scala.git",
)

ProjectConfigGson = ProjectConfig(
    name="gson",
    maven="https://mvnrepository.com/artifact/com.google.code.gson/gson",
    github="https://github.com/google/gson.git",
)
