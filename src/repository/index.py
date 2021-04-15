# index.py
from enum import IntEnum
from dataclasses import dataclass


@dataclass
class RepositoryConfig:
    dbType: int


class RepositoryEnum(IntEnum):
    GITHUB = 0

    @staticmethod
    def to_char(a: int):
        return {0: "GitHub Database"}[a]


class Repository:
    def __init__(self, config: RepositoryConfig):
        self.config = config
