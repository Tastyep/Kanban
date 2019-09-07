from .entity import Entity


class Board(Entity):
    def __init__(self, id, name):
        super(Board, self).__init__(id)
        self.name = name

    def name(self):
        return self._name
