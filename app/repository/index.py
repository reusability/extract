# repository.py
from enum import IntEnum


class Repository:
    def __init__(self):
        self.client = self._setup_client()
        self.type = self._setup_type()

    def _setup_client(self):
        pass

    def _setup_type(self):
        pass


class RepositoryEnum(IntEnum):
    SQL = 0
    NO_SQL = 1

    @staticmethod
    def to_char(a: int):
        return {
            0: 'SQL Database',
            1: 'NoSQL Database',
        }[a]
