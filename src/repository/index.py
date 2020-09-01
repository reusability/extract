# index.py
from enum import IntEnum
from dataclasses import dataclass


@dataclass
class RepositoryConfig:
    dbType: int


class RepositoryEnum(IntEnum):
    SQL = 0
    NO_SQL = 1
    GITHUB = 2

    @staticmethod
    def to_char(a: int):
        return {0: "SQL Database", 1: "NoSQL Database", 2: "GitHub Database"}[a]


class Repository:
    def __init__(self, config: RepositoryConfig):
        self.config = config
