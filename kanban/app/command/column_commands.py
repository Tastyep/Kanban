from dataclasses import dataclass
from uuid import UUID

from .command import Command


@dataclass
class AddColumn(Command):
    board_id: UUID
    column_idx: int
    column_title: str


@dataclass
class RemoveColumn(object):
    task_id: UUID
