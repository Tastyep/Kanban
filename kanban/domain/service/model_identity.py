import uuid


class ModelIdentity(object):
    def __init__(self, repo_facade):
        self._board_repo = repo_facade.board_repo()
        self._task_repo = repo_facade.task_repo()

    def identify_board(self, board_idx):
        return uuid.uuid5(uuid.NAMESPACE_OID, str(board_idx))

    def identify_column(self, board_idx, column_idx):
        return uuid.uuid4()
        #return uuid.uuid5(self.identify_board(board_idx), str(column_idx))

    def identify_task(self, board_idx, task_idx):
        return uuid.uuid5(self.identify_board(board_idx), str(task_idx))
