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
from src.project import projects
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

    clone_configs = []

    for repo in projects.projects:
        clone_configs.append(
            RepositoryConfigGit(
                repo_uri=repo.github, project_name=repo.name, versions=repo.tags
            )
        )

    # todo: inject source_code_dir as an environment variable
    runner_ck_config = RunnerMetricConfig(
        name="CK",
        source_code_dir="/Users/ahmedalasifer/Desktop/FIT4003/CK/ck/target/ck-0.6.3-SNAPSHOT-jar-with-dependencies.jar",
        project_dir="",
        output_dir="",
    )

    config_app_git_clone = AppConfigRepository(
        name=name,
        metric=RunnerCK,
        metric_config=runner_ck_config,
        repository=RepositoryGit,
        repository_config=RepositoryConfigGit,
    )

    app = App(config_app_git_clone)

    return app
