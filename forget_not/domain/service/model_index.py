class ModelIndex(object):
    def __init__(self, repo_facade):
        self._board_repo = repo_facade.board_repo()
        self._task_repo = repo_facade.task_repo()

    def index_board(self):
        board_idx = 0
        newest = self._board_repo.find_newest()
        if newest is not None:
            board_idx = newest.index() + 1
        return board_idx

    def index_task(self, board_id):
        task_idx = 0
        newest = self._task_repo.find_newest(board_id)
        if newest is not None:
            task_idx = newest.index() + 1
        return task_idx
