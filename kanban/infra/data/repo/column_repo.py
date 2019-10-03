from kanban.domain.model.column import make_column
from pypika import (
    Order,
    Query,
    Table,
)
from pypika import functions as fn

from . import table
from ..mapper.placeholder import PlaceHolder
from .repository import Repository


class ColumnRepo(Repository):
    def __init__(self, db):
        super(ColumnRepo, self).__init__(db, table.COLUMN,
                                         lambda s: make_column(s))
        self._create_table('''
                           id GUID PRIMARY KEY,
                           board_id GUID NOT NULL,
                           idx INT UNSIGNED NOT NULL,
                           title CHAR(255)
                           ''')

    def list_by_board(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, t.idx, t.title
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchall(q, {"board_id": board_id})

    def find_leftmost(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, fn.Min(t.idx), t.title
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchone(q, {"board_id": board_id})

    def find_rightmost(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, fn.Max(t.idx), t.title
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchone(q, {"board_id": board_id})

    def find_right_to(self, column_idx):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, fn.Min(t.idx), t.title
        ).where(
            t.idx > column_idx
        ).orderby(
            t.idx, order=Order.desc
        ).limit(1)
        return self._fetchone(q)

    def find_left_to(self, column_idx):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, fn.Max(t.idx), t.title
        ).where(
            t.idx < column_idx
        ).orderby(
            t.idx, order=Order.asc
        ).limit(1)
        return self._fetchone(q)
