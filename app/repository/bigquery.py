# bigqeury.py
from google.cloud import bigquery
from .index import Repository, RepositoryEnum


class RepositoryBigQuery(Repository):
    def __init__(self):
        super().__init__()

    def _setup_client(self):
        return bigquery.Client()

    def _setup_type(self):
        return RepositoryEnum.SQL

    def query(self, query):
        return self.client.query(query)
