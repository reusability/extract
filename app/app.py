# app.py
from .repository import Repository
from .repository import RepositoryConfig
from .repository import RepositoryEnum
from .repository import RepositoryBigQueryEnum
from .project import generate_random_query
from typing import NamedTuple
from .utils import Logger


class AppConfig(NamedTuple):
    name: str
    repository: Repository
    repository_config: RepositoryConfig


class App:
    def __init__(self, appConfig: AppConfig):
        # init
        self.logger: Logger = Logger(appConfig.name)
        self.logger.l.info("application started!")

        # setup
        repository = appConfig.repository
        repository_config = appConfig.repository_config
        self.logger.l.info(
            "creating repository -> db_type: %s, api_type: %s",
            RepositoryEnum.to_char(repository_config.dbType),
            RepositoryBigQueryEnum.to_char(repository_config.apiType),
        )
        self.repository: Repository = repository(repository_config)
        self.logger.l.info("repository created!")

    def Run(self):
        # generate query
        query = generate_random_query()  # todo: fix/remove

        # job
        query_job = self.repository.query(query)

        # print
        print("The query data:")
        for row in query_job:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        pass
