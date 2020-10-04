# general
from dataclasses import dataclass

# metrics
from src.metrics import RunnerMetricConfig
from src.metrics import Runner

# repository
from src.repository import Repository
from src.repository import RepositoryConfig


# todo: encapsulate metric and repository config injection into their respective classes
@dataclass
class AppConfig:
    name: str
    metric_config: RunnerMetricConfig
    metric: Runner


@dataclass
class AppConfigRepository(AppConfig):
    repository: Repository
    repository_config: RepositoryConfig
    projects_configs: None
