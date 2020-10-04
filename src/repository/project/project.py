# project.py
from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import time
import csv

from src.repository.utils.command import command_git_tag_checkout
from src.repository.utils.preprocess import (
    preprocess_github_tags,
    preprocess_match_maven_tags,
    preprocess_maven_reuse,
)
from src.utils import Subprocess
from src.utils import make_dir
from src.utils import Maven_Crawler


class Project:
    def __init__(self, name, maven, github):
        # init
        self.name = name
        self.maven: str = maven
        self.github: str = github
        self.github_project_name: str = self.github.split("/")[-1].split(".git")[0]

        # stores Maven releases (pandas dataFrame). col 0: release, col 2: usage, col 2: date
        self._releases: pd.DataFrame = None
        self._tags: [] = (
            []
        )  # store github tags. index 0: full tag, index 1: release number
        self.matched_maven_gh = []  # stores matched maven releases with GH tags

        # setup commands and outputs directory
        self.output_directory = "{}/src/outputs/{}".format(
            str(Path().resolve().parent), self.name
        )
        self._command = "git -C {} clone {}".format(self.output_directory, self.github)

        # setup cloning using subprocess module
        # todo -- remove subprocess init
        self.subprocess = Subprocess(self._command)

    """
    This function build the three required files.
    1. gh_tags.txt
    2. maven_reuse.csv
    3. unmatched.txt
    """

    def setup(self):
        # make the output directory
        make_dir(self.output_directory)

        # run the clone command
        self.subprocess.Run()

        # retrieve tags
        self._tags = preprocess_github_tags(
            self.name, self.output_directory, self.github_project_name
        )

        # run maven_reuse
        self._releases = preprocess_maven_reuse(
            self.name, self.output_directory, self.maven
        )

        # match maven release with GH tags
        self.matched_maven_gh = preprocess_match_maven_tags(
            self.name, self.output_directory, self._releases, self._tags
        )

    def checkout_version(self, tag: str):
        # init
        command = command_git_tag_checkout(
            self.output_directory, self.github_project_name, tag
        )

        # run
        Subprocess(command).Run()

    @staticmethod
    def make_dir(path):
        make_dir(path)

    @staticmethod
    def build_projects(count: int = 1) -> []:
        # return list
        projects: [ProjectConfig] = []

        maven_crawler = Maven_Crawler(category="open-source/web-assets")
        # get the first page of Popular Projects
        projects_maven_url = maven_crawler.list_projects()

        # TODO remove this in production
        #######################################################
        file = open("GH_from_Maven.csv", "w")
        fieldnames = ["No.", "maven", "usage", "github"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        counter = 1
        #######################################################

        while True:
            for project in projects_maven_url:
                # TODO remove in production
                ############################################################
                tmp = {
                    "No.": counter,
                    "maven": project["link"],
                    "usage": project["usage"],
                    "github": "None",
                }
                ############################################################

                # get GH link from .pom file
                gh_url = maven_crawler.get_GH_url(project["link"])

                # if GH link is found
                if gh_url != "None" and gh_url:
                    tmp["github"] = gh_url
                    projects.append(
                        ProjectConfig(
                            name=project["link"].split("/")[-1],
                            maven=project["link"],
                            github=gh_url,
                        )
                    )

                # TODO remove in production
                ############################################################
                writer.writerow(tmp)
                counter += 1
                ############################################################

                # if number of found projects with GH links reaches Count then break
                if len(projects) >= count:
                    file.close()
                    return projects

                # sleep to avoid being blocked
                time.sleep(10)

            # get the next 10 Projects
            projects_maven_url = maven_crawler.list_projects()

            if len(projects_maven_url) == 0:
                file.close()
                return projects


@dataclass
class ProjectConfig:
    name: str
    maven: str
    github: str


@dataclass
class Match_Maven_GH:
    gh_tag: str
    maven_release: str
