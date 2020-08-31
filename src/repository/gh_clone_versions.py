from typing import NamedTuple
from pathlib import Path

from src.utils import Subprocess
from src.utils import make_dir


class CloneConfig(NamedTuple):
    repo_uri: str
    project_name: str
    versions: list


class Clone:
    def __init__(self, cloneConfig: CloneConfig):
        self.config = cloneConfig
        self.dir = "{}/outputs/{}".format(
            str(Path().resolve().parent), self.config.project_name
        )
        make_dir(self.dir)

        self._command = "git -C {} clone {}".format(self.dir, self.config.repo_uri)

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
