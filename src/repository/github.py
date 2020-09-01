from src.project import Project

from .index import Repository
from .index import RepositoryConfig
from dataclasses import dataclass

from ..project.project import ProjectConfig


@dataclass
class RepositoryConfigGit(RepositoryConfig):
    repo_uri: str
    project_name: str
    versions: list


@dataclass
class RepositoryConfigGitHub(RepositoryConfig):
    clone_config: []


class RepositoryGit(Repository):
    def __init__(self, config: RepositoryConfigGit):
        super().__init__(config)

        # init
        self.projects: [Project] = None

    def build_projects(self, project_configs: [ProjectConfig]):
        self.projects = [
            Project(item[0], item[1], item[2], item[3]) for item in project_configs
        ]


RepositoryConfigGitClone = RepositoryConfigGit(dbType=2)
