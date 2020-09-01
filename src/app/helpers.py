# helpers.py
from src.repository import RepositoryBigQuery
from src.repository import RepositoryBigQueryStorage
from src.repository import RepositoryConfigBigQueryAPI
from src.repository import RepositoryConfigBigQueryStorage
from src.repository import Clone, CloneConfig
from src.project import projects
from src.app import App
from src.app import AppConfig
from src.matric import CK, MetricConfig
import os


def AppBigQueryAPI():
    name: str = "AppBigQueryAPI"

    # init
    bigQueryAppConfig = AppConfig(
        name=name,
        repository=RepositoryBigQuery,
        repository_config=RepositoryConfigBigQueryAPI,
    )

    # create src
    app = App(bigQueryAppConfig)

    # return
    return app


def AppBigQueryStorage():
    name: str = "AppBigQueryStorage"

    # init
    bigQueryAppConfigStorage = AppConfig(
        name=name,
        repository=RepositoryBigQueryStorage,
        repository_config=RepositoryConfigBigQueryStorage,
    )

    # create src
    app = App(bigQueryAppConfigStorage)

    # return
    return app


def CloneRepo():
    name: str = "CloneRepo"

    clone_configs = []

    for repo in projects.projects:
        clone_configs.append(
            CloneConfig(
                repo_uri=repo.github, project_name=repo.name, versions=repo.tags
            )
        )

    ck_config = MetricConfig(
        name="CK",
        project_dir=None,
        output_dir=None,
        source_code_dir=os.getenv("ck_path"),
    )

    clone = AppConfig(
        repository=None,
        repository_config=None,
        metric=CK,
        metric_config=ck_config,
        name=name,
        clone_config=clone_configs,
        clone=Clone,
    )

    app = App(clone)

    return app
