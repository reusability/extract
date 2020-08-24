# helpers
from .repository import (
    RepositoryBigQuery,
    RepositoryConfigBigQueryAPI,
    RepositoryConfigBigQueryStorage,
)
from .app import App, AppConfig


def AppBigQueryAPI():
    # init
    bigQueryAppConfig = AppConfig(
        repository=RepositoryBigQuery, repository_config=RepositoryConfigBigQueryAPI
    )

    # create app
    app = App(bigQueryAppConfig)

    # return
    return app


def AppBigQueryStorage():
    # init
    bigQueryAppConfig = AppConfig(
        repository=RepositoryBigQuery, repository_config=RepositoryConfigBigQueryStorage
    )

    # create app
    app = App(bigQueryAppConfig)

    # return
    return app
