from ..command import board_commands
from .controller import Controller


class BoardController(Controller):
    def __init__(self, cmd_dispatcher, repo_facade):
        super(BoardController, self).__init__(cmd_dispatcher)
        self._board_repo = repo_facade.board_repo()
        self._register_handlers({
            board_commands.AddBoard: self._add_board,
        })

    def _add_board(self, board):
        print("add board with name: {}".format(board.name()))
