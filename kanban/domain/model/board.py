from .entity import Entity
from .state.board_state import BoardState


class Board(Entity):
    def __init__(self, *args):
        super(Board, self).__init__(
            BoardState(*args)
        )

    @property
    def index(self):
        return self._state.index

    @property
    def name(self):
        return self._state.name

    @property
    def active(self):
        return self._state.active


def make_board(state):
    (id, index, name, active) = state
    return Board(id, index, name, active)
