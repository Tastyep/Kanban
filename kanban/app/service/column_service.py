from kanban.domain.model.column import Column

from ..command import column_commands
from .service import Service


class ColumnService(Service):
    def __init__(self, cmd_dispatcher, repo_facade):
        super(ColumnService, self).__init__(cmd_dispatcher)
        self._column_repo = repo_facade.column_repo()
        self._register_handlers({
            column_commands.AddColumn: self._add_column,
            column_commands.RemoveColumn: self._remove_column,
        })

    def _add_column(self, cmd):
        column = Column(cmd.entity_id, cmd.board_id, cmd.column_idx, cmd.column_title)
        self._column_repo.create(column)

    def _remove_column(self, cmd):
        self._column_repo.delete(cmd.column_id)
