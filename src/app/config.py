from typing import NamedTuple

from src.metrics import RunnerMetricConfig
from src.metrics import RunnerCK
from src.repository import Repository
from src.repository import RepositoryConfig


# todo: encapsulate metric and repository config injection into their respective classes
class AppConfig(NamedTuple):
    name: str
    metric_config: RunnerMetricConfig
    metric: RunnerCK


class AppConfigRepository(AppConfig):
    repository: Repository
    repository_config: RepositoryConfig
