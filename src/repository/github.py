from src.metrics import Runner

from src.project import Project

from .index import Repository
from .index import RepositoryConfig
from dataclasses import dataclass

from ..project.project import ProjectConfig

# utils
from pathlib import Path
from ..utils import remove_dir


@dataclass
class RepositoryConfigGit(RepositoryConfig):
    placeholder: int


class RepositoryGit(Repository):
    def __init__(self, config: RepositoryConfigGit):
        super().__init__(config)

        # init
        self.projects: [Project] = None

    def build_projects(self, project_configs: [ProjectConfig]):
        self.projects = [
            Project(item.name, item.maven, item.github, item.tags)
            for item in project_configs
        ]

    def do_stuff(self, runner: Runner):
        print(self.projects)
        for project in self.projects:
            # clone
            project.setup()

            # for each tag in project.tag
            for tag in project.tags:
                # init
                project.checkout_version(tag)  # checkout
                tag_output_directory = project.output_directory + "/{}".format(tag)

                # make dir
                project.make_dir(tag_output_directory)

                # build metrics
                runner.Run(project.output_directory + "/{}".format(project.name))

                # move output
                runner.move_output(
                    str(Path().resolve().parent) + "/src/", tag_output_directory
                )  # TODO hey: the csv files are stored under src directory

            # remove project
            # TODO i had to add another dependency to remove the project
            remove_dir("{}/{}".format(project.output_directory, project.name))


RepositoryConfigGitHub = RepositoryConfigGit(dbType=2, placeholder=0)
