from ..command import user_commands
from .service import Service


class UserService(Service):
    def __init__(self, cmd_dispatcher, repo_facade):
        super(UserService, self).__init__(cmd_dispatcher)
        self._user_repo = repo_facade.user_repo()
        self._register_handlers({
            user_commands.AddUser: self._add_user,
        })

    def _add_user(self, cmd):
        None
