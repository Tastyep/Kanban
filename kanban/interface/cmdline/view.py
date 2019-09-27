from itertools import zip_longest

from colorama import (
    Fore,
    Style,
)
from colorama import init as color_init
from kanban.config import config
from tabulate import tabulate

_config = config['Cli']


class CommandLineView(object):
    def __init__(self):
        color_init(autoreset=True)

    def display_board(self, data, filter):
        headers = []
        columns = {}

        # print("data: {}".format(data))
        for c in data['columns']:
            headers.append(c['title'])
            columns[c['id']] = []
        for t in data['tasks']:
            columns[t['column_id']].append(t)

        table = []
        sorted_columns = []
        for column in columns.values():
            sorted_columns.append(sorted(column, key=lambda task: task[filter]))

        rows = zip_longest(*sorted_columns, fillvalue=None)
        for row in rows:
            table_row = []
            for task in row:
                table_row.append(self._format_task(task))
            table.append(table_row)

        print("> {} <\n".format(data['board']['name']))
        print(tabulate(table, headers=headers, tablefmt="pipe"))

    def report_error(self, err):
        print('{}ERROR{}: {}'.format(Fore.RED, Style.RESET_ALL, err))

    def _format_task(self, task):
        if task is None:
            return None
        context = task['context']
        content = "{}{}_{} {}".format(
            task['index'], self._priority_to_color(task['priority']), Style.RESET_ALL,
            task['content'])
        if context is not None:
            content += ' @' + context
        return content

    def _priority_to_color(self, p):
        code = None
        if p == 'A':
            code = _config.priority_a
        if p == 'B':
            code = _config.priority_b
        if p == 'C':
            code = _config.priority_c
        if p == 'D':
            code = _config.priority_d
        if p == 'E':
            code = _config.priority_e
        assert code is not None, f'Invalid priority {p}'
        return getattr(Fore, code)
