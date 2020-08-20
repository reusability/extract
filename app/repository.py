# repository.py
from google.cloud import bigquery
from enum import IntEnum


class RepositoryEnum(IntEnum):
    SQL = 0
    NO_SQL = 1

    # @staticmethod
    # def to_char(a: int):
    #     return {
    #         0: 'SQL Database',
    #         1: 'NoSQL Database',
    #     }[a]


class Repository:
    def __init__(self):
        self.client = self._setup_client()
        self.type = self._setup_type()

    def _setup_client(self):
        pass

    def _setup_type(self):
        pass


class RepositoryBigQuery(Repository):
    def __init__(self):
        super().__init__()

    def _setup_client(self):
        return bigquery.Client()

    def _setup_type(self):
        return RepositoryEnum.SQL

    def query(self, query):
        return self.client.query(query)
