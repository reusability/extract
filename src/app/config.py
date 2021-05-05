# general
from dataclasses import dataclass

from src.repository import Repository, RepositoryConfig
from src.runner import Runner, RunnerConfig
from src.utils import Logger


@dataclass
class IRepositoryConfig:
    type: Repository
    config: RepositoryConfig


@dataclass
class IRunnerConfig:
    type: Runner
    config: RunnerConfig


@dataclass
class AppConfig:
    logger: Logger
    repository: Repository
    runner: Runner
