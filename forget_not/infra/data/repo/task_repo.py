from pypika import (
    Query,
    Table,
)
from pypika import functions as fn

from forget_not.domain.model.task import make_task

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
                           idx INT UNSIGNED NOT NULL,
                           content TEXT
                           ''')

    def find_newest(self, board_id):
        t = Table(self._table)
        q = Query.from_(t).select(
            t.id, t.board_id, fn.Max(t.idx), t.content
        ).where(
            t.board_id == PlaceHolder("board_id")
        )
        return self._fetchone(q, {"board_id": board_id})
