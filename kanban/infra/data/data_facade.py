class DataFacade(object):
    def __init__(self, repo_factory, db):
        self._task_repo = repo_factory.make_task_repo(db)
        self._board_repo = repo_factory.make_board_repo(db)

    def task_repo(self):
        return self._task_repo

    def board_repo(self):
        return self._board_repo
