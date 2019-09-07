from ..command import task_commands
from .controller import Controller


class TaskController(Controller):
    def __init__(self, cmd_dispatcher, repo_facade):
        super(TaskController, self).__init__(cmd_dispatcher)
        self._task_repo = repo_facade.task_repo()
        self._register_handlers({
            task_commands.AddTask: self._add_task,
        })

    def _add_task(self, task):
        print("add task with content: {}".format(task.content()))
