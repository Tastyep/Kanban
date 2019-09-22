from pypika import (
    Query,
    Table,
)
from pypika import functions as fn

from kanban.domain.model.board import make_board

from . import table
from .repository import Repository


class BoardRepo(Repository):
    def __init__(self, db):
        super(BoardRepo, self).__init__(db, table.BOARD, make_board)
        self._create_table('''
                           id GUID PRIMARY KEY,
                           idx INT UNSIGNED NOT NULL,
                           name TEXT,
                           active TINYINT NOT NULL
                           ''')

    def find_active(self):
        b = Table(self._table)
        q = Query.from_(b).select(
            b.id, b.idx, b.name, b.active
        ).where(
            b.active == True
        )
        return self._fetchone(q)

    def find_newest(self):
        b = Table(self._table)
        q = Query.from_(b).select(
            b.id, fn.Max(b.idx), b.name, b.active
        )
        return self._fetchone(q)
