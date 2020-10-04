from src.metrics import Runner

from src.project import Project

from .index import Repository
from .index import RepositoryConfig
from dataclasses import dataclass
import time

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

    def build_projects(self, project_configs: {str: ProjectConfig}):
        self.projects = [
            Project(item.name, item.maven, item.github)
            for key, item in project_configs.items()
        ]

    def do_stuff(self, runner: Runner):
        for project in self.projects:
            # clone
            project.setup()

            # for each tag in project.matched_maven_github releases
            for release in project.matched_maven_gh:
                # init
                project.checkout_version(release.gh_tag)  # checkout
                tag_output_directory = project.output_directory + "/{}".format(
                    release.maven_release
                )

                # make dir
                project.make_dir(tag_output_directory)

                # output directory
                runner.set_output(tag_output_directory)

                # build metrics
                if runner.config.move_output:
                    runner.Run(
                        project.output_directory
                        + "/{}".format(project.github_project_name),  # noqa : W503
                        move_output=True,
                        output_source=str(Path().resolve().parent) + "/src/",
                    )
                else:
                    runner.Run(
                        project.output_directory
                        + "/{}".format(project.github_project_name)  # noqa : W503
                    )

                break
            # remove project
            # TODO i had to add another dependency to remove the project
            remove_dir(
                "{}/{}".format(project.output_directory, project.github_project_name)
            )

            # sleep between projects
            seconds = 10
            print("Sleeping for {}".format((seconds)))
            time.sleep(seconds)


RepositoryConfigGitHub = RepositoryConfigGit(dbType=2, placeholder=0)
