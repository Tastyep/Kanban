from .board_service import BoardService
from .task_service import TaskService
from .user_service import UserService


class ServiceModule(object):
    def register_services(self, app_facade, repo_facade):
        cmd_dispatcher = app_facade.command_dispatcher()
        self._user_service = UserService(cmd_dispatcher, repo_facade)
        self._board_service = BoardService(cmd_dispatcher, repo_facade)
        self._task_service = TaskService(cmd_dispatcher, repo_facade)
