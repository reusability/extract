# helpers.py
# repository
from src.extract import RepositoryGit
from src.extract.github import RepositoryConfigGit
from src.extract.project.build import build_projects

# config
from .config import AppConfigRepository

# apps
from .index import AppGitHub

# others
from src.runner import RunnerMetricConfigSM
from src.runner import RunnerMetricConfigCK
from src.runner import RunnerSM
from src.runner import RunnerCK


def HelperAppGitHubSM(count, sleep, categories, min_maven_usage, versions):
    # init
    name: str = "AppGitHubSourceMeter"

    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(
        dbType=0, sleep=sleep, versions=versions
    )

    # config app
    config_sm = AppConfigRepository(
        name=name,
        metric=RunnerSM,
        metric_config=RunnerMetricConfigSM,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=build_projects(count, categories, min_maven_usage, sleep),
    )

    # build app
    app = AppGitHub(config_sm)

    # return
    return app


def HelperAppGitHubCK(count, sleep, categories, min_maven_usage, versions):
    # init
    name: str = "AppGitHubCK"

    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(
        dbType=0, sleep=sleep, versions=versions
    )

    # config app
    config_ck = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=RunnerMetricConfigCK,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=build_projects(count, categories, min_maven_usage, sleep),
    )

    # build app
    app = AppGitHub(config_ck)

    # return
    return app
