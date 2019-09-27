from kanban.domain.model.task import make_task
from pypika import (
    Query,
    Table,
)
from pypika import functions as fn

from . import table
from ..mapper.placeholder import PlaceHolder
from .repository import Repository


class TaskRepo(Repository):
    def __init__(self, db):
        super(TaskRepo, self).__init__(db, table.TASK,
                                       lambda s: make_task(s))
        self._create_table('''
                           id GUID PRIMARY KEY,
                           board_id GUID NOT NULL,
                           column_id GUID NOT NULL,
                           idx INT UNSIGNED NOT NULL,
                           content TEXT,
                           priority CHAR,
                           context CHAR(255)
                           ''')

    def list_by_board(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.star
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchall(q, {"board_id": board_id})

    def find_newest(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, t.column_id, fn.Max(t.idx), t.content, t.priority, t.context
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchone(q, {"board_id": board_id})
