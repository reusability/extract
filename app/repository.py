# repository.py
from google.cloud import bigquery


class Repository:
    def __init__(self):
        self.client = self._setup_client()

    def _setup_client(self):
        pass


class RepositoryBigQuery(Repository):
    def __init__(self):
        super().__init__()

    def _setup_client(self):
        return bigquery.Client()

    def query(self, query):
        return self.client.query(query)
