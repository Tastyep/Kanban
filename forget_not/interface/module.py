from .cmdline.input import CommandLineParser


class InterfaceModule(object):
    def __init__(self, app_facade, repo_facade):
        self._cmdline = CommandLineParser(app_facade, repo_facade)

    def run(self):
        if self._cmdline.parse() is False:
            None  # Start GUI
