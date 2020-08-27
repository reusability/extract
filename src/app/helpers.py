# helpers.py
from src.repository import RepositoryBigQuery
from src.repository import RepositoryBigQueryStorage
from src.repository import RepositoryConfigBigQueryAPI
from src.repository import RepositoryConfigBigQueryStorage
from src.app import App
from src.app import AppConfig


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
