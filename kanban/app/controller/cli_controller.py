#!/usr/bin/env python3

import sys

from kanban.config import config
from kanban.domain.error import DomainError
from kanban.domain.service.model_identity import ModelIdentity
from kanban.domain.service.model_index import ModelIndex
from kanban.infra.cmdline.cli_parser import CliParser
from kanban.interface.cmdline.view import CommandLineView

from ..command.board_commands import AddBoard
from ..command.task_commands import (
    AddTask,
    RemoveTask,
)

_config = config['Cli']


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
                .command('add', ['a']) \
                    .argument('name', help='Name of the board') \
                .command('show', ['s']) \
                .argument('-s', '--sort', dest='column', default='index', help='Sort by column') \
                .prev() \
            .command_table('task', ['tk']) \
                .command('add', ['a']) \
                    .argument('content', help='Content of the task') \
                    .argument('-p', '--priority', help='Priority of the task') \
                    .argument('-c', '--context', help='Context of the task') \
                .command('remove', ['r']).argument('index', help='Index of the task')

    def run(self):
        data = self._parser.parse(sys.argv)
        if data is None:
            return False
        path = data[CliParser.PATH_ID]
        handler = '_{}'.format('_'.join(path[1:]))
        assert hasattr(self, handler), \
            'missing handler {}'.format(handler)
        try:
            getattr(self, handler)(data)
        except (RuntimeError, DomainError) as e:
            self._view.report_error(str(e))

        return True

    def _board_add(self, args):
        board_idx = self._model_index.index_board()
        board_id = self._model_identity.identify_board(board_idx)
        cmd = AddBoard(board_id, board_idx, args['name'])
        self._cmd_dispatcher.dispatch(cmd)

    def _board_show(self, args):
        board = self._active_board()
        tasks = self._task_repo.list_by_board(board.id)
        filter = args['column']
        self._view.display_board(board, tasks, filter)

    def _task_add(self, args):
        board = self._active_board()
        task_idx = self._model_index.index_task(board.id)
        task_id = self._model_identity.identify_task(board.index, task_idx)
        priority = self._opt(args, 'priority', _config.default_priority)
        context = self._opt(args, 'context', None)
        cmd = AddTask(task_id, board.id, task_idx, args['content'], priority, context)
        self._cmd_dispatcher.dispatch(cmd)

    def _task_remove(self, args):
        board = self._active_board()
        try:
            index = int(args['index'])
        except ValueError:
            self._view.report_error("invalid index: '{}'".format(args['index']))
            return

        task_id = self._model_identity.identify_task(board.index, index)
        cmd = RemoveTask(task_id)
        self._cmd_dispatcher.dispatch(cmd)

    def _opt(self, args, key, default):
        return args[key] if (key in args and args[key] is not None) else default

    def _active_board(self):
        board = self._board_repo.find_active()
        if board is None:
            raise RuntimeError('A board must be created first')
        return board
