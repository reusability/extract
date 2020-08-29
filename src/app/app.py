# src.py
from src.repository import Repository
from src.repository import RepositoryConfig
from src.repository import RepositoryEnum
from src.repository import RepositoryBigQueryEnum

# from src.project import generate_random_query
from typing import NamedTuple
from src.utils import Logger


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
        # github_query = """
        #     SELECT f.repo_name, c.content
        #     FROM bigquery-public-data.github_repos.files f left join bigquery-public-data.github_repos.contents c
        #     on f.id = c.id
        #     where f.path like '%.java' and f.repo_name in ('scala/scala', 'scalatest/scalatest')
        #     limit 100;
        # """

        # job
        query_job = self.repository.query("None")

        # print
        print("The query data:")
        counter = 0
        for row in query_job:
            print(row)  # a bette way to visualise this maybe writing it to a file.
            if counter > 100000:
                break
            counter += 1

        # for row in query_job:
        #     # Row values can be accessed by field name or index.
        #     print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        exit()
