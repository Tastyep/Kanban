from .command import Command


class AddBoard(Command):
    def __init__(self, entity_id, name):
        super(AddBoard, self).__init__(entity_id)
        self._name = name

    def name(self):
        return self._name
