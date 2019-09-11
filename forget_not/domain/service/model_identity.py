import uuid


class ModelIdentity(object):
    def __init__(self, repo_facade):
        self._board_repo = repo_facade.board_repo()
        self._task_repo = repo_facade.task_repo()

    def identify_board(self, board_idx=None):
        if board_idx is None:
            newest = self._board_repo.find_newest()
            if newest is None:
                board_idx = 0
            else:
                board_idx = newest.index() + 1
        user = self._user_repo.find()
        return uuid.uuid5(user.id(), str(board_idx))

    def identify_task(self, task_idx=None):
        if task_idx is None:
            newest = self._task_repo.find_newest()
            if newest is None:
                task_idx = 0
            else:
                task_idx = newest.index() + 1
        board = self._board_repo.find_active()
        return uuid.uuid5(board.id(), str(task_idx))
