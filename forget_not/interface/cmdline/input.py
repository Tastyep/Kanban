#!/usr/bin/env python3

import argparse

from forget_not.app.command.board_commands import AddBoard
from forget_not.app.command.task_commands import AddTask


class CommandLineParser(object):
    def __init__(self, cmd_dispatcher):
        self._cmd_dispatcher = cmd_dispatcher

        parser = argparse.ArgumentParser(description='Organise your boards, tasks and notes.')
        parser.add_argument('-t', '--task', metavar='task', dest='task', help='Create a task')
        parser.add_argument('-b', '--board', metavar='board', help='Create a board')
        parser.add_argument('-s', '--show', metavar='board', help='Show a board')
        self._parser = parser

        self._arg_handlers = {
            "task": self._add_task,
            "board": self._add_board,
        }

    def parse(self):
        args = vars(self._parser.parse_args())
        if not any(args.values()):
            self._parser.print_help()
            return False

        for k, v in args.items():
            if v is not None:
                assert (k in self._arg_handlers), "missing handler for {} parameter".format(k)
                self._arg_handlers[k](v)

        return True

    def _add_task(self, task):
        cmd = AddTask(None, task)
        self._cmd_dispatcher.dispatch(cmd)

    def _add_board(self, board):
        cmd = AddBoard(None, board)
        self._cmd_dispatcher.dispatch(cmd)
