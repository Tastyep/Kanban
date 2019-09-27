from kanban.domain.model.task import Task

from ..command import task_commands
from .service import Service


class TaskService(Service):
    def __init__(self, cmd_dispatcher, repo_facade):
        super(TaskService, self).__init__(cmd_dispatcher)
        self._task_repo = repo_facade.task_repo()
        self._register_handlers({
            task_commands.AddTask: self._add_task,
            task_commands.RemoveTask: self._remove_task,
        })

    def _add_task(self, cmd):
        task = Task(cmd.entity_id, cmd.board_id, cmd.column_id, cmd.task_idx,
                    cmd.task_content, cmd.task_priority, cmd.task_context)
        self._task_repo.create(task)

    def _remove_task(self, cmd):
        self._task_repo.delete(cmd.task_id)
