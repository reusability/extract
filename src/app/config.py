# general
from dataclasses import dataclass

from src.repository import Repository, RepositoryConfig
from src.runner import Runner, RunnerConfig


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
