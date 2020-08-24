# helpers.py
from .repository import RepositoryBigQuery
from .repository import RepositoryBigQueryStorage
from .repository import RepositoryConfigBigQueryAPI
from .repository import RepositoryConfigBigQueryStorage
from .app import App
from .app import AppConfig


def AppBigQueryAPI():
    name: str = "AppBigQueryAPI"

    # init
    bigQueryAppConfig = AppConfig(
        name=name,
        repository=RepositoryBigQuery,
        repository_config=RepositoryConfigBigQueryAPI,
    )

    # create app
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

    # create app
    app = App(bigQueryAppConfigStorage)

    # return
    return app
