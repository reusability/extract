# from src.metrics import RunnerMetricConfig

from src.project import Project

from .index import Repository
from .index import RepositoryConfig
from dataclasses import dataclass

from ..project.project import ProjectConfig


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

    def do_stuff(self):
        print(self.projects)
        for project in self.projects:
            # clone
            project.setup()

            # for each tag in project.tag
            for tag in project.tags:
                # checkout
                project.checkout_version(tag)

                # make dir
                project.make_dir(project.output_directory + "/{}".format(tag))

                # build metrics
                # RunnerMetricConfig(project.name, project.output_directory, )

                # name: str
                # project_dir: str
                # output_dir: str
                # source_code_dir: str
                # remove dir

            pass

        # for repo in self.clone_config:
        #     new_repo = self.clone(repo)
        #     new_repo.clone_repo()
        #     for v in repo.versions:
        #         new_repo.checkout_version(v)
        #         make_dir(new_repo.dir + "/{}".format(v))
        #         self.metric_config = self.metric_config._replace(
        #             project_dir="{}/{}".format(
        #                 new_repo.dir, new_repo.config.project_name
        #             ),
        #             output_dir="{}/{}".format(new_repo.dir, v),
        #         )
        #
        #         m = self.metric(self.metric_config)
        #         m.Run()
        #         m.move_output(source=str(Path().resolve().parent) + "/src/")
        #     remove_dir("{}/{}".format(new_repo.dir, new_repo.config.project_name))


RepositoryConfigGitHub = RepositoryConfigGit(dbType=2, placeholder=0)
