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
        usage = '{} <command>'.format(' '.join(lineage))
        parser = argparse.ArgumentParser(prog=name, usage=usage)
        subparser = parser.add_subparsers(title='commands', dest=self.CMD_ID, metavar='', help='')
        table = Table(self._table, parser, subparser)
        if self._root is None:
            self._root = table
            self._table = self._root
        else:
            self._table.sub_tables[name] = table
            self._table = table

        return self

    def command_table(self, name, aliases=[], help='', *args):
        self.command(name, aliases, help)
        return self.table(name, *args)

    def command(self, name, aliases=[], help=''):
        assert self._table is not None, "a table must be created first"
        self._table.aliases[name] = aliases
        command = self._table.subparser.add_parser(name, aliases=aliases, help=help)
        self._table.commands[name] = command
        return self

    def argument(self, *args, **kwargs):
        assert self._table is not None, "a table must be created first"
        assert len(self._table.commands) > 0, "a command must be created first"
        cmds = self._table.commands
        cmds[list(cmds.keys())[-1]].add_argument(*args, **kwargs)
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
        has_subtables = len(table.sub_tables) > 0
        args = argv[0:1] if has_subtables else argv
        parser = table.parser
        data = vars(parser.parse_args(args))
        if self.CMD_ID not in data:
            parser.print_help()
            return None
        cmd = data[self.CMD_ID]
        keys = table.aliases.keys()
        if cmd not in keys:
            for k in keys:
                if cmd in table.aliases[k]:
                    cmd = k
                    break
        if cmd is None:
            parser.print_help()
            return None
        params[self.PATH_ID].append(parser.prog)
        if has_subtables:
            next = table.sub_tables[cmd]
            return self._parse_table(next, argv[1:], {**params, **data})

        params[self.PATH_ID].append(cmd)
        return {**params, **data}


class Table(object):
    def __init__(self, parent, parser, subparser):
        self.parent = parent
        self.parser = parser
        self.subparser = subparser
        self.aliases = dict()
        self.sub_tables = dict()
        self.commands = OrderedDict()
