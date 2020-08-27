# bigquery.py
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta1
from .index import Repository
from .index import RepositoryEnum
from .index import RepositoryConfig
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
        # authorization
        self.credentials, self.project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )

        # client
        client = bigquery.Client(credentials=self.credentials, project=self.project_id)

        # ret
        return client

    def query(self, query):
        return self.client.query(query)


class RepositoryBigQueryStorage(RepositoryBigQuery):
    def __init__(self, config: RepositoryBigQueryConfig):
        super().__init__(config)
        self._setup_client_storage()

    def _setup_client_storage(self):
        self.client_storage = bigquery_storage_v1beta1.BigQueryStorageClient(
            credentials=self.credentials
        )

    def query(self, query):
        return self.client.query(query)


RepositoryConfigBigQueryAPI = RepositoryBigQueryConfig(
    apiType=RepositoryBigQueryEnum.API, dbType=RepositoryEnum.SQL
)

RepositoryConfigBigQueryStorage = RepositoryBigQueryConfig(
    apiType=RepositoryBigQueryEnum.STORAGE, dbType=RepositoryEnum.SQL
)
