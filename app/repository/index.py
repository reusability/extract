# index.py
from enum import IntEnum
from dataclasses import dataclass


@dataclass
class RepositoryConfig:
    dbType: int


class RepositoryEnum(IntEnum):
    SQL = 0
    NO_SQL = 1

    @staticmethod
    def to_char(a: int):
        return {0: "SQL Database", 1: "NoSQL Database"}[a]


class Repository:
    # TODO
    # 1. __str__ should return self.config
    def __init__(self, config: RepositoryConfig):
        self.config = config
        self.client = self._setup_client()

    def _setup_client(self):
        pass
