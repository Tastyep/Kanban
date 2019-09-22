from dataclasses import dataclass
from uuid import UUID


@dataclass
class BoardState:
    id: UUID
    index: int
    name: str
    active: bool
