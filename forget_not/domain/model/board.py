from .entity import Entity
from .state.board_state import BoardState


class Board(Entity):
    def __init__(self, id, name):
        super(Board, self).__init__(
            BoardState(id, name)
        )

    def name(self):
        return self._state.name

    def active(self):
        return self._state.active
