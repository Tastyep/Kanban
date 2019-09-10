from .command import Command


class AddTask(Command):
    def __init__(self, entity_id, parent_id, task_content):
        super(AddTask, self).__init__(entity_id)
        self._parent_id = parent_id
        self._task_content = task_content

    def board_id(self):
        return self._parent_id

    def task_content(self):
        return self._task_content
