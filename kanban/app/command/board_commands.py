from dataclasses import dataclass

from .command import Command


@dataclass
class AddBoard(Command):
    board_idx: int
    board_name: str
