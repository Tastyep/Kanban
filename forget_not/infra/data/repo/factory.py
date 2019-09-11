from .board_repo import BoardRepo
from .task_repo import TaskRepo


class Factory(object):
    def make_task_repo(self, db):
        return TaskRepo(db)

    def make_board_repo(self, db):
        return BoardRepo(db)
