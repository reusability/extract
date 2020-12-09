# general
from dataclasses import dataclass

# metrics
from src.runner import RunnerConfig
from src.runner import Runner

# repository
from src.extract import Repository
from src.extract import RepositoryConfig
from src.extract import ProjectConfig

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
    name: str
    metric: IRunnerConfig
    repository: IRepositoryConfig

@dataclass
class AppConfigRepository(AppConfig):
    repository: Repository
    repository_config: RepositoryConfig
    projects_config: [ProjectConfig]
