#!/usr/bin/env python3

import sys

from forget_not.app.command.board_commands import AddBoard
from forget_not.app.command.task_commands import AddTask
from forget_not.domain.service.model_identity import ModelIdentity
from forget_not.domain.service.model_index import ModelIndex
from forget_not.infra.cmdline.cli_parser import CliParser

from .view import CommandLineView


class CommandLineController(object):
    CMD_ID = '_cmd_id'
    NS_ID = '_namespace'

    def __init__(self, app_facade, repo_facade):
        self._cmd_dispatcher = app_facade.command_dispatcher()
        self._board_repo = repo_facade.board_repo()
        self._task_repo = repo_facade.task_repo()

        self._view = CommandLineView()
        self._model_index = ModelIndex(repo_facade)
        self._model_identity = ModelIdentity(repo_facade)

        self._parser = CliParser().table('fn') \
            .command_table('board', ['bd']) \
                .command('add', ['a']).argument('name', help='Name of the board') \
                .command('show', ['s']) \
                .prev() \
            .command_table('task', ['tk']) \
                .command('add', ['a']).argument('content', help='Content of the task')

    def run(self):
        data = self._parser.parse(sys.argv)
        if data is None:
            return False
        path = data[CliParser.PATH_ID]
        handler = '_{}'.format('_'.join(path[1:]))
        assert hasattr(self, handler), \
            'missing handler {}'.format(handler)
        getattr(self, handler)(data)
        return True

    def _add_parser(self, sub_parser, name, aliases=[], help=''):
        self._aliases[name] = aliases
        return sub_parser.add_parser(name, aliases=aliases, help=help)

    def _board_add(self, args):
        board_idx = self._model_index.index_board()
        board_id = self._model_identity.identify_board(board_idx)
        cmd = AddBoard(board_id, board_idx, args['name'])
        self._cmd_dispatcher.dispatch(cmd)

    def _board_show(self, args):
        board = self._board_repo.find_active()
        if board is None:
            self._view.report_error('no board available to display')
            return
        tasks = self._task_repo.list_by_board(board.id())
        self._view.display_board(board, tasks)

    def _task_add(self, args):
        board = self._board_repo.find_active()
        if board is None:
            return
        task_idx = self._model_index.index_task(board.id())
        task_id = self._model_identity.identify_task(board.index(), task_idx)
        cmd = AddTask(task_id, board.id(), task_idx, args['content'])
        self._cmd_dispatcher.dispatch(cmd)
