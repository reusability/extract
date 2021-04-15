# general
from dataclasses import dataclass

from src.extract import Repository
from src.extract import RepositoryConfig
from src.runner import Runner
from src.runner import RunnerConfig


# todo: encapsulate metric and repository config injection into their respective classes
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
    repository: Repository
    runner: Runner
