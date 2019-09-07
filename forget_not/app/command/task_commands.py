from .command import Command


class AddTask(Command):
    def __init__(self, entity_id, content):
        super(AddTask, self).__init__(entity_id)
        self._content = content

    def content(self):
        return self._content
