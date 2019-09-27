from .entity import Entity
from .state.column_state import ColumnState


class Column(Entity):
    def __init__(self, *args):
        super(Column, self).__init__(
            ColumnState(*args)
        )

    @property
    def board_id(self):
        return self._state.board_id

    @property
    def index(self):
        return self._state.index

    @property
    def title(self):
        return self._state.title


def make_column(state):
    (id, board_id, index, title) = state
    return Column(id, board_id, index, title)
