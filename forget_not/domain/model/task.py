from .entity import Entity
from .state.task_state import TaskState


class Task(Entity):
    def __init__(self, *args):
        super(Task, self).__init__(
            TaskState(*args)
        )

    @property
    def board_id(self):
        return self._state.board_id

    @property
    def index(self):
        return self._state.index

    @property
    def content(self):
        return self._state.content

    @property
    def priority(self):
        return self._state.priority

    @property
    def context(self):
        return self._state.context


def make_task(state):
    (id, board_id, index, content, priority, context) = state
    return Task(id, board_id, index, content, priority, context)
