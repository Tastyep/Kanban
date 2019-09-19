from dataclasses import dataclass
from uuid import UUID

from .command import Command


@dataclass
class AddTask(Command):
    board_id: UUID
    task_idx: int
    task_content: str


@dataclass
class RemoveTask(object):
    task_id: UUID
