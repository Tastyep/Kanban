from dataclasses import dataclass
from uuid import UUID


@dataclass
class UserState:
    id: UUID
    board_id: UUID
