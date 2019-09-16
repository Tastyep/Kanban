from .cmdline.controller import CommandLineController


class InterfaceModule(object):
    def __init__(self, app_facade, repo_facade):
        self._cmdline = CommandLineController(app_facade, repo_facade)

    def run(self):
        if self._cmdline.run() is False:
            None  # Start GUI
