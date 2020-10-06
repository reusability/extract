# helpers.py
# repository
from src.repository.project.project import Project
from src.repository import RepositoryGit
from src.repository.github import RepositoryConfigGit

# config
from .config import AppConfigRepository

# apps
from .index import AppGitHub

# others
from src.metrics import RunnerMetricConfigSM
from src.metrics import RunnerMetricConfigCK
from src.metrics import RunnerSM
from src.metrics import RunnerCK


def HelperAppGitHubSM(count, sleep, categories, min_maven_usage):
    # init
    name: str = "AppGitHubSourceMeter"

    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(dbType=0, sleep=sleep)

    # config app
    config_sm = AppConfigRepository(
        name=name,
        metric=RunnerSM,
        metric_config=RunnerMetricConfigSM,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=Project.build_projects(count, categories, min_maven_usage),
    )

    # build app
    app = AppGitHub(config_sm)

    # return
    return app


def HelperAppGitHubCK(count, sleep, categories, min_maven_usage):
    # init
    name: str = "AppGitHubCK"

    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(dbType=0, sleep=sleep)

    # config app
    config_ck = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=RunnerMetricConfigCK,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=Project.build_projects(count, categories, min_maven_usage),
    )

    # build app
    app = AppGitHub(config_ck)

    # return
    return app
