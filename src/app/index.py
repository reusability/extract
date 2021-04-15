# src.py
from src.repository import RepositoryEnum, Repository

# utils.py
from src.utils import Logger

# app.py
from .config import AppConfig
from ..runner import Runner


class App:
    def __init__(self, config: AppConfig):
        # config files
        self.config: AppConfig = config
        self.logger: Logger = config.logger

        # metrics
        self.runner: Runner = self.config.runner
        self.logger.l.info("metrics init -> metrics_type: %s", self.runner.config.name)

        # init
        self.repository: Repository = self.config.repository
        self.logger.l.info(
            "starting repository connection -> db_type: %s",
            RepositoryEnum.to_char(self.repository.config.dbType),
        )

    def Run(self):
        # do stuff
        self.logger.l.info("running repository iterator")
        self.repository.Run(self.runner)

    def Stop(self):
        pass
