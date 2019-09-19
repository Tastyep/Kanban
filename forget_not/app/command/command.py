from dataclasses import dataclass
from uuid import UUID


@dataclass
class Command:
    entity_id: UUID
