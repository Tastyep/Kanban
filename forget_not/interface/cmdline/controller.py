#!/usr/bin/env python3

import argparse

from forget_not.app.command.board_commands import AddBoard
from forget_not.app.command.task_commands import AddTask
from forget_not.domain.service.model_identity import ModelIdentity
from forget_not.domain.service.model_index import ModelIndex


class CommandLineController(object):
    def __init__(self, app_facade, repo_facade):
        self._cmd_dispatcher = app_facade.command_dispatcher()
        self._board_repo = repo_facade.board_repo()
        self._model_index = ModelIndex(repo_facade)
        self._model_identity = ModelIdentity(repo_facade)

        parser = argparse.ArgumentParser(description='Organise your boards, tasks and notes.')
        parser.add_argument('-t', '--task', metavar='task', dest='task', help='Create a task')
        parser.add_argument('-b', '--board', metavar='board', help='Create a board')
        parser.add_argument('-s', '--show', metavar='board', help='Show a board')
        self._parser = parser

        self._arg_handlers = {
            "task": self._add_task,
            "board": self._add_board,
        }

    def run(self):
        args = vars(self._parser.parse_args())
        if not any(args.values()):
            self._parser.print_help()
            return False

        for k, v in args.items():
            if v is not None:
                assert (k in self._arg_handlers), "missing handler for {} parameter".format(k)
                self._arg_handlers[k](v)

        return True

    def _add_task(self, task_content):
        board = self._board_repo.find_active()
        if board is None:
            return
        task_idx = self._model_index.index_task(board.id())
        print("task_idx: {}".format(task_idx))
        task_id = self._model_identity.identify_task(board.index(), task_idx)
        cmd = AddTask(task_id, board.id(), task_idx, task_content)
        self._cmd_dispatcher.dispatch(cmd)

    def _add_board(self, board_name):
        board_idx = self._model_index.index_board()
        board_id = self._model_identity.identify_board(board_idx)
        cmd = AddBoard(board_id, board_idx, board_name)
        self._cmd_dispatcher.dispatch(cmd)
