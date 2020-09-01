from pathlib import Path
from src.utils import Subprocess
from src.utils import make_dir
from .index import Repository
from .index import RepositoryConfig
from dataclasses import dataclass


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
        # init
        super().__init__(config)

        # output dir
        self._build_output_dir()
        self._command = "git -C {} clone {}".format(self.dir, self.config.repo_uri)

    # todo: move clone_repo to init
    def clone_repo(self):
        self.clone = Subprocess(self._command)
        self.clone.run()

    def checkout_version(self, version: str):
        checkout = Subprocess(
            "git -C {}/{} checkout tags/v{}".format(
                self.dir, self.config.project_name, version
            )
        )
        checkout.run()

    def _build_output_dir(self):
        self.dir = "{}/outputs/{}".format(
            str(Path().resolve().parent), self.config.project_name
        )
        make_dir(self.dir)


RepositoryConfigGitClone = RepositoryConfigGit(dbType=2)
