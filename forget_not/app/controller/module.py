from .board_controller import BoardController
from .task_controller import TaskController


class ControllerModule(object):
    def register_controllers(self, app_facade, repo_facade):
        cmd_dispatcher = app_facade.command_dispatcher()
        self._task_controller = TaskController(cmd_dispatcher, repo_facade)
        self._board_controller = BoardController(cmd_dispatcher, repo_facade)
