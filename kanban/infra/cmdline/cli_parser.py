import argparse
from collections import OrderedDict


class CliParser(object):
    CMD_ID = '_cmd_id'
    PATH_ID = '_path'

    def __init__(self):
        self._aliases = {}
        self._root = None
        self._table = None

    def table(self, name, *args):
        def compose_lineage(table):
            lineage = []
            if table.parent is not None:
                lineage = compose_lineage(table.parent)
            lineage.append(table.parser.prog)
            return lineage

        lineage = [name]
        if self._table is not None:
            lineage = compose_lineage(self._table) + lineage
        usage = '{}'.format(' '.join(lineage))
        parser = argparse.ArgumentParser(prog=name, usage=usage)
        subparser = parser.add_subparsers(title='commands', dest=self.CMD_ID, metavar='', help='')
        table = _Table(self._table, parser, subparser)
        if self._root is None:
            self._root = table
            self._table = self._root
        else:
            self._table.commands[-1].sub_table = table
            self._table = table
            self._command = None

        return self

    def command_table(self, name, aliases=[], help='', *args):
        self.command(name, aliases, help)
        return self.table(name, *args)

    def command(self, name, aliases=[], help=''):
        assert self._table is not None, "a table must be created first"
        parser = self._table.subparser.add_parser(name, aliases=aliases, help=help)
        self._table.commands.append(_Command(name, aliases, parser))
        return self

    def argument(self, *args, **kwargs):
        assert self._table is not None, "a table must be created first"
        assert len(self._table.commands) > 0, "a command must be created first"
        cmd = self._table.commands[-1]
        cmd.parser.add_argument(*args, **kwargs)
        return self

    def prev(self):
        assert self._table is not None and self._table.parent is not None, \
            "can't prev on root node"
        self._table = self._table.parent
        return self

    def parse(self, argv):
        assert self._root is not None, "parser is empty"
        return self._parse_table(self._root, argv[1:], {self.PATH_ID: []})

    def _parse_table(self, table, argv, params):
        def command_name(argv):
            for v in argv:
                if v[0] != '-':
                    return v
            return None

        def command_by_name(table, cmd_name):
            for cmd in table.commands:
                if cmd.name == cmd_name or cmd_name in cmd.aliases:
                    return cmd
            return None

        parser = table.parser
        cmd_name = command_name(argv)
        cmd = None if cmd_name is None else command_by_name(table, cmd_name)
        if cmd is None:
            parser.print_help()
            return None

        args = argv if cmd.sub_table is None else argv[0:1]
        data = vars(parser.parse_args(args))
        params[self.PATH_ID].append(parser.prog)
        if cmd.sub_table is not None:
            next = cmd.sub_table
            return self._parse_table(next, argv[1:], {**params, **data})

        params[self.PATH_ID].append(cmd.name)
        return {**params, **data}


class _Command(object):
    def __init__(self, name, aliases, parser):
        self.name = name
        self.aliases = aliases
        self.parser = parser
        self.sub_table = None


class _Table(object):
    def __init__(self, parent, parser, subparser):
        self.parent = parent
        self.parser = parser
        self.subparser = subparser
        self.commands = list()
