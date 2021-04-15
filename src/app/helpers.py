# helpers.py
# repository
from src.repository import RepositoryGit, RepositoryConfigGit
from src.runner import RunnerCK, RunnerSM, RunnerMetricConfigCK

# others
from src.runner import RunnerMetricConfigSM

# config
from .config import AppConfig

# apps
from .index import App
from ..utils import Logger


def HelperAppGitHubSM(count, sleep, categories, min_maven_usage, versions):
    # init
    # name: str = "AppGitHubSourceMeter"

    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(
        dbType=0, sleep=sleep, versions=versions
    )

    # config app
    app_config = AppConfig(
        runner=RunnerSM(RunnerMetricConfigSM),
        repository=RepositoryGit(RepositoryConfigGitHub),
    )

    # build app
    app = App(app_config)

    # return
    return app


def HelperAppGitHubCK(count, sleep, categories, min_maven_usage, versions):
    # config github
    RepositoryConfigGitHub = RepositoryConfigGit(
        dbType=0, sleep=sleep, versions=versions
    )

    # logger
    logger: Logger = Logger("AppCK")
    logger.l.info("application started!")

    # config app
    app_config = AppConfig(
        logger=logger,
        runner=RunnerCK(RunnerMetricConfigCK, logger),
        repository=RepositoryGit(RepositoryConfigGitHub, logger),
    )

    # build app
    app = App(app_config)

    # return
    return app
