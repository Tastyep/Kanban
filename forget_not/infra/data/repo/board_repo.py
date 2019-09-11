from pypika import (
    Query,
    Table,
)

from . import table
from .repository import Repository


class BoardRepo(Repository):
    def __init__(self, db):
        super(BoardRepo, self).__init__(db, table.BOARD)
        self._create_table('''
                           id BINARY(16) PRIMARY KEY,
                           name TEXT
                           ''')
