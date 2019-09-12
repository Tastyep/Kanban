from .command import Command


class AddBoard(Command):
    def __init__(self, entity_id, board_idx, board_name):
        super(AddBoard, self).__init__(entity_id)
        self._board_name = board_name
        self._board_idx = board_idx

    def board_idx(self):
        return self._board_idx

    def board_name(self):
        return self._board_name
