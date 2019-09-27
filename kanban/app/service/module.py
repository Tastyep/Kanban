from .board_service import BoardService
from .column_service import ColumnService
from .task_service import TaskService


class ServiceModule(object):
    def register_services(self, app_facade, repo_facade):
        cmd_dispatcher = app_facade.command_dispatcher()
        self._board_service = BoardService(cmd_dispatcher, repo_facade)
        self._column_service = ColumnService(cmd_dispatcher, repo_facade)
        self._task_service = TaskService(cmd_dispatcher, repo_facade)
