from .entity import Entity
from .state.board_state import BoardState


class Board(Entity):
    def __init__(self, id, index, name, active):
        super(Board, self).__init__(
            BoardState(id, index, name, active)
        )

    def index(self):
        return self._state.index

    def name(self):
        return self._state.name

    def active(self):
        return self._state.active
