# index.py
from dataclasses import dataclass
from enum import IntEnum

from src.extract import ProjectConfig
from src.runner import Runner
from src.utils import Logger


@dataclass
class RepositoryConfig:
    dbType: int


class RepositoryEnum(IntEnum):
    GITHUB = 0

    @staticmethod
    def to_char(a: int):
        return {0: "GitHub Database"}[a]


class Repository:
    def __init__(self, config: RepositoryConfig, logger: Logger = None):
        self.config = config
        self.logger = logger

    def Pre(self, project_configs: {str: ProjectConfig}):
        pass

    def Run(self, runner: Runner):
        pass
