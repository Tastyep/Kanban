from .board_repo import BoardRepo
from .task_repo import TaskRepo
from .user_repo import UserRepo


class Factory(object):
    def make_task_repo(self, db):
        return TaskRepo(db)

    def make_board_repo(self, db):
        return BoardRepo(db)

    def make_user_repo(self, db):
        return UserRepo(db)
