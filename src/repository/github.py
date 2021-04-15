import time
from dataclasses import dataclass

# utils
from pathlib import Path

from src.extract.project.project import Project
from src.extract.project.project import ProjectConfig
from src.runner import Runner
from .index import Repository
from .index import RepositoryConfig
from ..utils import remove_dir, Logger


@dataclass
class RepositoryConfigGit(RepositoryConfig):
    sleep: int
    versions: int


class RepositoryGit(Repository):
    def __init__(self, config: RepositoryConfigGit, logger: Logger):
        super().__init__(config)
        self.logger = logger
        self.logger.l.info("successfully initiated git connection")

        # init
        self.projects: [Project] = []

    def set_projects(self, project_configs: {str: ProjectConfig}):
        self.logger.l.info("setting projects in format: (name, maven_url, github_url)")
        self.projects = [
            Project(item.name, item.maven, item.github)
            for key, item in project_configs.items()
        ]

    def is_runnable(self):
        return len(self.projects) != 0

    def Run(self, runner: Runner):
        if not self.is_runnable():
            self.logger.l.error("no projects to iterate")

        for project in self.projects:
            # clone
            project.setup()
            counter = 0
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

                counter += 1
                if counter == self.config.versions:
                    break
            # remove project
            # TODO i had to add another dependency to remove the project
            remove_dir(
                "{}/{}".format(project.output_directory, project.github_project_name)
            )

            # sleep between projects
            print("Sleeping for {}".format((self.config.sleep)))
            time.sleep(self.config.sleep)
