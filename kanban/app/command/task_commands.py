from dataclasses import dataclass
from uuid import UUID

from .command import Command


@dataclass
class AddTask(Command):
    board_id: UUID
    column_id: UUID
    task_idx: int
    task_content: str
    task_priority: str
    task_context: str


@dataclass
class RemoveTask(object):
    task_id: UUID


@dataclass
class MoveTask(object):
    task_id: UUID
    column_id: UUID
