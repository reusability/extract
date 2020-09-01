# helpers.py
# big query
from src.repository import RepositoryBigQuery
from src.repository import RepositoryBigQueryStorage
from src.repository import RepositoryConfigBigQueryAPI
from src.repository import RepositoryConfigBigQueryStorage

# git
from src.repository import RepositoryGit
from src.repository import RepositoryConfigGit

# config
from .config import AppConfig
from .config import AppConfigRepository

# apps
from .app import App

# others
from src.project import ProjectConfigScala, ProjectConfigGson
from src.metrics import RunnerCK, RunnerMetricConfig


def AppBigQueryAPI():
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


def AppBigQueryStorage():
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


def AppGitClone():
    name: str = "AppGitClone"

    # metrics
    # todo: inject source_code_dir as an environment variable
    metric_config = RunnerMetricConfig(
        name="CK",
        source_code_dir="/Users/ahmedalasifer/Desktop/FIT4003/CK/ck/target/ck-0.6.3-SNAPSHOT-jar-with-dependencies.jar",
        project_dir="",
        output_dir="",
    )

    # projects
    # todo: use mvn script to init this project_config
    project_config = [ProjectConfigScala, ProjectConfigGson]

    # config app -- github
    config_app_github = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=metric_config,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGit,
        projects_config=project_config,
    )

    app = App(config_app_github)

    return app
