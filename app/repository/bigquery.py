# bigquery.py
from google.cloud import bigquery
from .index import Repository, RepositoryEnum, RepositoryConfig
from enum import IntEnum
from dataclasses import dataclass


@dataclass
class RepositoryBigQueryConfig(RepositoryConfig):
    apiType: int


class RepositoryBigQueryEnum(IntEnum):
    API = 0
    STORAGE = 1

    @staticmethod
    def to_char(a: int):
        return {0: "BigQuery API", 1: "BigQuery Storage API"}[a]


class RepositoryBigQuery(Repository):
    def __init__(self, config: RepositoryBigQueryConfig):
        super().__init__(config)

    def _setup_client(self):
        return bigquery.Client()

    def query(self, query):
        return self.client.query(query)


RepositoryConfigBigQueryAPI = RepositoryBigQueryConfig(
    apiType=RepositoryBigQueryEnum.API, dbType=RepositoryEnum.SQL
)

RepositoryConfigBigQueryStorage = RepositoryBigQueryConfig(
    apiType=RepositoryBigQueryEnum.STORAGE, dbType=RepositoryEnum.SQL
)
