# app.py
from .repository import Repository, RepositoryConfig
from .project import generate_random_query
from typing import NamedTuple


class AppConfig(NamedTuple):
    repository: Repository
    repository_config: RepositoryConfig


class App:
    def __init__(self, appConfig: AppConfig):
        repository = appConfig.repository
        repository_config = appConfig.repository_config
        self.repository = repository(repository_config)

    def Run(self):
        # generate query
        query = generate_random_query()  # todo: fix

        # job
        query_job = self.repository.query(query)

        # print
        print("The query data:")
        for row in query_job:
            # Row values can be accessed by field name or index.
            print("name={}, count={}".format(row[0], row["total_people"]))

    def Stop(self):
        pass
