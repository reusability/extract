# helpers.py
# big query
from src.repository.github import RepositoryConfigGitHub

from src.repository import RepositoryBigQuery
from src.repository import RepositoryBigQueryStorage
from src.repository import RepositoryConfigBigQueryAPI
from src.repository import RepositoryConfigBigQueryStorage

# git
from src.repository import RepositoryGit

# config
from .config import AppConfig
from .config import AppConfigRepository

# apps
from .index import App, AppRepositoryGitHub

# others
from src.project import ProjectConfigGson
from src.metrics import RunnerCK, RunnerMetricConfig
import os


def HelperAppBigQueryAPI():
    name: str = "AppBigQueryAPI"

    # init
    config_app_big_query_api = AppConfig(
        name=name,
        repository=RepositoryBigQuery,
        repository_config=RepositoryConfigBigQueryAPI,
    )

    # create src
    app = App(config_app_big_query_api)

    # return
    return app


def HelperAppBigQueryStorage():
    name: str = "AppBigQueryStorage"

    # init
    config_app_big_query_storage = AppConfig(
        name=name,
        repository=RepositoryBigQueryStorage,
        repository_config=RepositoryConfigBigQueryStorage,
    )

    # create src
    app = App(config_app_big_query_storage)

    # return
    return app


def HelperAppGitHub():
    name: str = "AppGitClone"

    # metrics
    # todo: inject source_code_dir as an environment variable
    metric_config = RunnerMetricConfig(
        name="CK", metrics_runner_file=os.getenv("ck_path")
    )

    # projects
    # todo: use mvn script to init this project_config
    project_config = [ProjectConfigGson]

    # config app -- github
    config_app_github = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=metric_config,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGitHub,
        projects_config=project_config,
    )

    app = AppRepositoryGitHub(config_app_github)

    return app
