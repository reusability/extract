# __main__.py
# used to the main files in this packageg
from .app import App, AppConfig
from .repository import RepositoryBigQuery, RepositoryConfigBigQueryAPI

if __name__ == "__main__":
    # init
    bigQueryAppConfig = AppConfig(
        repository=RepositoryBigQuery, repository_config=RepositoryConfigBigQueryAPI
    )

    # create app
    app = App(bigQueryAppConfig)

    # run
    app.Run()
