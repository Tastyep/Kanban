from dataclasses import dataclass
from uuid import UUID


@dataclass
class TaskState:
    id: UUID
    board_id: UUID
    index: int
    content: str
