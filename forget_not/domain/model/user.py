from .entity import Entity
from .state.user_state import UserState


class User(Entity):
    def __init__(self, id, board_id):
        super(User, self).__init__(
            UserState(id, board_id)
        )

    def board_id(self):
        return self._state.board_id
