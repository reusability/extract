# src.py
from src.repository import RepositoryEnum

# utils.py
from src.utils import Logger

# app.py
from .config import AppConfig


class App:
    def __init__(self, config: AppConfig):
        # config files
        self.config: AppConfig = config

        # logger
        self.logger: Logger = Logger(
            "AppGitHub{runner_name}".format(runner_name=self.config.runner.config.name)
        )
        self.logger.l.info("application started!")

        # metrics
        self.runner = self.config.runner
        self.logger.l.info("metrics init -> metrics_type: %s", self.runner.config.name)

        # init
        self.repository = self.config.repository
        self.logger.l.info(
            "starting repository connection -> db_type: %s",
            RepositoryEnum.to_char(self.repository.config.dbType),
        )

    def Run(self):
        # do stuff
        self.logger.l.info("running application")
        self.repository.do_stuff(self.runner)

    def Stop(self):
        pass
