from .command import Command


class AddBoard(Command):
    def __init__(self, entity_id, board_name):
        super(AddBoard, self).__init__(entity_id)
        self._board_name = board_name

    def board_name(self):
        return self._board_name
