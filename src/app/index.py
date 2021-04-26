# src.py
from src.repository import RepositoryEnum, Repository

# utils.py
from src.utils import Logger

# app.py
from .config import AppConfig
from ..extract.project.build import build_projects
from ..runner import Runner


class App:
    def __init__(self, config: AppConfig, n):
        self.config: AppConfig = config
        self.logger: Logger = config.logger
        self.n = n
        self.projects = None

        # metrics
        self.runner: Runner = self.config.runner
        self.logger.l.info("metrics init -> metrics_type: %s", self.runner.config.name)

        # init
        self.repository: Repository = self.config.repository
        self.logger.l.info(
            "starting repository connection -> db_type: %s",
            RepositoryEnum.to_char(self.repository.config.dbType),
        )

    def Pre(self):
        # initialize projects
        self.logger.l.info("initialising project config")
        self.projects = build_projects(
            self.n["count"],
            self.n["categories"],
            self.n["min_maven_usage"],
            self.n["sleep"],
        )

    def Run(self):
        # do stuff
        self.logger.l.info("running repository iterator")
        self.repository.Run(self.runner)

    def Stop(self):
        pass
