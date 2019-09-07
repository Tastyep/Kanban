from .entity import Entity


class Task(Entity):
    def __init__(self, id, content):
        super(Task, self).__init__(id)
        self._content = content

    def content(self):
        return self._content
