from colorama import (
    Fore,
    Style,
)
from colorama import init as color_init
from tabulate import tabulate


class CommandLineView(object):
    def __init__(self):
        color_init(autoreset=True)

    def display_board(self, board, tasks):
        table = [["index", "task"]]
        for t in tasks:
            table.append([t.index(), t.content()])

        print("- {}\n".format(board.name()))
        print(tabulate(table, headers="firstrow"))

    def report_error(self, err):
        print('{}ERROR{}: {}'.format(Fore.RED, Style.RESET_ALL, err))
