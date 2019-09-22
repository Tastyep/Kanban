from colorama import (
    Fore,
    Style,
)
from colorama import init as color_init
from tabulate import tabulate

from forget_not.config import config

task_config = config['Task']


class CommandLineView(object):
    def __init__(self):
        color_init(autoreset=True)

    def display_board(self, board, tasks):
        table = [["index", "task"]]
        for t in tasks:
            table.append([t.index, self._format_content(t)])

        print("- {}\n".format(board.name))
        print(tabulate(table, headers="firstrow", tablefmt="pipe"))

    def report_error(self, err):
        print('{}ERROR{}: {}'.format(Fore.RED, Style.RESET_ALL, err))

    def _format_content(self, task):
        context = task.context
        content = "{}{}{} {}".format(
            self._priority_to_color(task.priority), '#', Style.RESET_ALL,
            task.content)
        if context is not None:
            content += ' @' + context
        return content

    def _priority_to_color(self, p):
        code = None
        if p == 'A':
            code = task_config.priority_a
        if p == 'B':
            code = task_config.priority_b
        if p == 'C':
            code = task_config.priority_c
        if p == 'D':
            code = task_config.priority_d
        if p == 'E':
            code = task_config.priority_e
        assert code is not None, f"Invalid priority {p}"
        return getattr(Fore, code)
