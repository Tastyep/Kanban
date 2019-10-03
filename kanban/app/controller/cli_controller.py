import sys

from kanban.config import config
from kanban.domain.error import DomainError
from kanban.domain.service.model_composition import ModelComposition
from kanban.domain.service.model_identity import ModelIdentity
from kanban.domain.service.model_index import ModelIndex
from kanban.infra.cmdline.cli_parser import CliParser
from kanban.interface.cmdline.view import CommandLineView

from ..command.board_commands import AddBoard
from ..command.column_commands import AddColumn
from ..command.task_commands import (
    AddTask,
    MoveTask,
    RemoveTask,
)

_config = config['Cli']


class _InvalidArgument(Exception):
    pass


class CommandLineController(object):
    CMD_ID = '_cmd_id'
    NS_ID = '_namespace'

    def __init__(self, app_facade, repo_facade):
        self._cmd_dispatcher = app_facade.command_dispatcher()
        self._board_repo = repo_facade.board_repo()
        self._column_repo = repo_facade.column_repo()
        self._task_repo = repo_facade.task_repo()

        self._view = CommandLineView()
        self._model_index = ModelIndex(repo_facade)
        self._model_identity = ModelIdentity(repo_facade)
        self._model_composition = ModelComposition(repo_facade)

        self._parser = CliParser().table('fn') \
            .command_table('board', ['bd']) \
                .command('add', ['a']) \
                    .argument('name', help='Name of the board') \
                .command('show', ['s']) \
                    .argument('-s', '--sort', dest='opt', default='index', help='Sort by option') \
                .prev() \
            .command_table('column', ['cl']) \
                .command('add', ['a']) \
                    .argument('title', help='Title of the column') \
                .command('remove', ['r']) \
                    .argument('index', help='Index of the column') \
                .prev() \
            .command_table('task', ['tk']) \
                .command('add', ['a']) \
                    .argument('content', help='Content of the task') \
                    .argument('-p', '--priority', help='Priority of the task') \
                    .argument('-c', '--context', help='Context of the task') \
                .command('remove', ['r']) \
                    .argument('index', help='Index of the task') \
                .command_table('move', ['mv']) \
                    .command('right', ['r']) \
                        .argument('index', help='Index of the task') \
                    .command('left', ['l']) \
                        .argument('index', help='Index of the task')

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
        except (RuntimeError, DomainError, _InvalidArgument) as e:
            self._view.report_error(str(e))

        return True

    def _board_add(self, args):
        board_idx = self._model_index.index_board()
        board_id = self._model_identity.identify_board(board_idx)
        add_board = AddBoard(board_id, board_idx, args['name'])
        self._cmd_dispatcher.dispatch(add_board)
        for i, title in enumerate(_config.default_columns):
            column_id = self._model_identity.identify_column(board_idx, i)
            add_column = AddColumn(column_id, board_id, i, title)
            self._cmd_dispatcher.dispatch(add_column)
        self._display_board(board_id)

    def _board_show(self, args):
        board = self._active_board()
        filter = self._stropt(args, 'opt', None)
        self._display_board(board.id, filter)

    def _task_add(self, args):
        board = self._active_board()
        column = self._column_repo.find_leftmost(board.id)
        task_idx = self._model_index.index_task(board.id)
        task_id = self._model_identity.identify_task(board.index, task_idx)
        priority = self._stropt(args, 'priority', _config.default_priority)
        context = self._stropt(args, 'context', None)
        cmd = AddTask(task_id, board.id, column.id, task_idx, args['content'], priority, context)
        self._cmd_dispatcher.dispatch(cmd)
        self._display_board(board.id)

    def _task_remove(self, args):
        board = self._active_board()

        task_id = self._model_identity.identify_task(board.index, index)
        cmd = RemoveTask(task_id)
        self._cmd_dispatcher.dispatch(cmd)

    def _task_move_right(self, args):
        board = self._active_board()
        task_idx = self._intopt(args, 'index', None)
        task_id = self._model_identity.identify_task(board.index, task_idx)
        task = self._expect(self._task_repo, task_id, f'invalid index {task_idx}')
        column = self._column_repo.find_by_id(task.column_id)
        next = self._column_repo.find_right_to(column.index)
        if next is None:
            raise _InvalidArgument('already in rightmost column')
        cmd = MoveTask(task.id, next.id)
        self._cmd_dispatcher.dispatch(cmd)
        self._display_board(board.id)

    def _task_move_left(self, args):
        board = self._active_board()
        task_idx = self._intopt(args, 'index', None)
        task_id = self._model_identity.identify_task(board.index, task_idx)
        task = self._expect(self._task_repo, task_id, f'invalid index {task_idx}')
        column = self._column_repo.find_by_id(task.column_id)
        next = self._column_repo.find_left_to(column.index)
        if next is None:
            raise _InvalidArgument('already in leftmost column')
        cmd = MoveTask(task.id, next.id)
        self._cmd_dispatcher.dispatch(cmd)
        self._display_board(board.id)

    def _stropt(self, args, key, default):
        return args[key] if (key in args and args[key] is not None) else default

    def _intopt(self, args, key, default):
        if not (key in args) or args[key] is None:
            return default
        try:
            return int(args[key])
        except ValueError as e:
            raise ValueError("invalid {}: '{}'".format(key, args[key])) from e

    def _display_board(self, id, filter='index'):
        data = self._model_composition.board_data(id)
        self._view.display_board(data, filter)

    def _expect(self, repo, id, errmsg):
        entity = repo.find_by_id(id)
        if entity is None:
            raise _InvalidArgument(errmsg)
        return entity

    def _active_board(self):
        board = self._board_repo.find_active()
        if board is None:
            raise RuntimeError('A board must be created first')
        return board
