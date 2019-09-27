class DataFacade(object):
    def __init__(self, repo_factory, db):
        self._board_repo = repo_factory.make_board_repo(db)
        self._column_repo = repo_factory.make_column_repo(db)
        self._task_repo = repo_factory.make_task_repo(db)

    def board_repo(self):
        return self._board_repo

    def column_repo(self):
        return self._column_repo

    def task_repo(self):
        return self._task_repo
