from dataclasses import dataclass
from uuid import UUID


@dataclass
class ColumnState:
    id: UUID
    board_id: UUID
    index: int
    title: str
