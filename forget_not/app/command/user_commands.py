from .command import Command


class AddUser(Command):
    def __init__(self, entity_id, user_name):
        super(AddUser, self).__init__(entity_id)
        self._user_name = user_name

    def user_name(self):
        return self._user_name
