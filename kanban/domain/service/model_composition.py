class ModelComposition(object):
    def __init__(self, repo_facade):
        self._board_repo = repo_facade.board_repo()
        self._column_repo = repo_facade.column_repo()
        self._task_repo = repo_facade.task_repo()

    def board_data(self, id):
        data = {
            "columns": [],
            "tasks": [],
        }
        board = self._board_repo.find_by_id(id)
        columns = self._column_repo.list_by_board(id)
        tasks = self._task_repo.list_by_board(id)

        data["board"] = board.state()
        for c in columns:
            data["columns"].append(c.state())
        for t in tasks:
            data["tasks"].append(t.state())

        return data
