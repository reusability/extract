# helpers.py
# repository
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

    # projects
    # todo: use mvn script to init this project_config
    project_config = []

    # config app -- github
    config_app_github = AppConfigRepository(
        name=name,
        metric=RunnerSM,
        metric_config=RunnerMetricConfigSM,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=project_config,
    )

    app = AppGitHub(config_app_github)

    return app


def HelperAppGitHubCK():
    name: str = "AppGitHubCK"

    # projects
    # todo: use mvn script to init this project_config
    project_config = []

    # config app -- github
    config_app_github = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=RunnerMetricConfigCK,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=project_config,
    )

    app = AppGitHub(config_app_github)

    return app
