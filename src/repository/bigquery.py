# bigquery.py
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1
from .index import Repository
from .index import RepositoryEnum
from .index import RepositoryConfig
from enum import IntEnum
from dataclasses import dataclass


@dataclass
class RepositoryConfigBigQuery(RepositoryConfig):
    apiType: int


class RepositoryEnumBigQuery(IntEnum):
    API = 0
    STORAGE = 1

    @staticmethod
    def to_char(a: int):
        return {0: "BigQuery API", 1: "BigQuery Storage API"}[a]


class RepositoryBigQuery(Repository):
    def __init__(self, config: RepositoryConfigBigQuery):
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
    def __init__(self, config: RepositoryConfigBigQuery):
        super().__init__(config)
        self._setup_client_storage()

    def _setup_client_storage(self):
        self.credentials, self.project_id = google.auth.default(
            scopes=["https://www.googleapis.com/auth/cloud-platform"]
        )
        self.client = bigquery_storage_v1.BigQueryReadClient()
        self.requested_session = bigquery_storage_v1.types.ReadSession()
        self.parent = "projects/{}".format(self.project_id)

    def table(self, table_name, fields=None):
        table = "projects/{}/datasets/{}/tables/{}".format(
            "bigquery-public-data", "github_repos", table_name
        )
        self.requested_session.table = table
        # This API can also deliver data serialized in Apache Arrow format.
        # This example leverages Apache Avro.
        self.requested_session.data_format = bigquery_storage_v1.enums.DataFormat.AVRO

        for field in fields:
            self.requested_session.read_options.selected_fields.append(field)

    def query(self, query):
        self.table("contents", ["id", "content", "size"])
        session = self.client.create_read_session(
            self.parent,
            self.requested_session,
            # We'll use only a single stream for reading data from the table. However,
            # if you wanted to fan out multiple readers you could do so by having a
            # reader process each individual stream.
            max_stream_count=4,
        )
        reader = self.client.read_rows(session.streams[0].name)

        return reader.rows(session)


RepositoryConfigBigQueryAPI = RepositoryConfigBigQuery(
    apiType=RepositoryEnumBigQuery.API, dbType=RepositoryEnum.SQL
)

RepositoryConfigBigQueryStorage = RepositoryConfigBigQuery(
    apiType=RepositoryEnumBigQuery.STORAGE, dbType=RepositoryEnum.SQL
)
