# helpers.py
# repository
from src.repository.project.project import Project
from src.repository import RepositoryGit
from src.repository.github import RepositoryConfigGitHub

# config
from .config import AppConfigRepository

# apps
from .index import AppGitHub

# others
from src.metrics import RunnerMetricConfigSM
from src.metrics import RunnerMetricConfigCK
from src.metrics import RunnerSM
from src.metrics import RunnerCK


def HelperAppGitHubSM():
    name: str = "AppGitHubSourceMeter"
    count: int = 10

    # config app -- github
    config_sm = AppConfigRepository(
        name=name,
        metric=RunnerSM,
        metric_config=RunnerMetricConfigSM,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=Project.build_projects(count),
    )

    app = AppGitHub(config_sm)

    return app


def HelperAppGitHubCK():
    name: str = "AppGitHubCK"
    count: int = 10

    # config app -- github
    config_ck = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=RunnerMetricConfigCK,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=Project.build_projects(count),
    )

    app = AppGitHub(config_ck)

    return app
