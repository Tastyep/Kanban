from .entity import Entity
from .state.task_state import TaskState


class Task(Entity):
    def __init__(self, id, board_id, content):
        super(Task, self).__init__(
            TaskState(id, board_id, content)
        )

    def board_id(self):
        return self._state.board_id

    def content(self):
        return self._state.content
