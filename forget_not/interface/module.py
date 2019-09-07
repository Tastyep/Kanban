from cmdline.input import CommandLineParser


class InterfaceModule(object):
    def __init__(self, cmd_dispatcher):
        self._cmdline = CommandLineParser(cmd_dispatcher)

    def run(self):
        if self._cmdline.parse() is False:
            None  # Start GUI
