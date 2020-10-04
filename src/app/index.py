# src.py
from src.repository import RepositoryEnum

# app.py
from .config import AppConfig
from .config import AppConfigRepository

# utils.py
from src.utils import Logger


class App:
    def __init__(self, config: AppConfig):
        # config files
        self.config: AppConfig = config

        # logger
        self.logger: Logger = Logger(config.name)
        self.logger.l.info("application started!")

        # metrics
        self.metric = config.metric(config.metric_config)
        self.logger.l.info(
            "metrics init -> metrics_type: %s", config.metric_config.name
        )

        # setup
        repository = config.repository
        repository_config = config.repository_config

        # init
        self.logger.l.info(
            "starting repository connection -> db_type: %s",
            RepositoryEnum.to_char(repository_config.dbType),
        )
        self.repository: config = repository(repository_config)
        self.logger.l.info("repository created!")

    def Run(self):
        pass

    def Stop(self):
        pass


class AppGitHub(App):
    def __init__(self, config: AppConfigRepository):
        # init
        super().__init__(config)

        # setup projects
        self.repository.build_projects(config.projects_config)

    def Run(self):
        # do stuff
        self.repository.do_stuff(self.metric)
