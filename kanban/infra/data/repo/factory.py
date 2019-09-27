from .board_repo import BoardRepo
from .column_repo import ColumnRepo
from .task_repo import TaskRepo


class Factory(object):
    def make_board_repo(self, db):
        return BoardRepo(db)

    def make_column_repo(self, db):
        return ColumnRepo(db)

    def make_task_repo(self, db):
        return TaskRepo(db)
