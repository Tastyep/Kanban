class Facade(object):
    def __init__(self, factory, db):
        self._task_repo = factory.make_task_repo(db)
        self._board_repo = factory.make_board_repo(db)
        self._user_repo = factory.make_user_repo(db)

    def task_repo(self):
        return self._task_repo

    def board_repo(self):
        return self._board_repo

    def user_repo(self):
        return self._user_repo
