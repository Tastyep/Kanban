from . import table
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
