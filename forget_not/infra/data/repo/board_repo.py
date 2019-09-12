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
                           idx INT UNSIGNED NOT NULL,
                           name TEXT,
                           active TINYINT NOT NULL
                           ''')

    def find_active(self):
        board = Table(self._table)
        q = Query.from_(board).select(
            board.star
        ).where(
            board.active == 1
        )
        self._exec_query(q)
