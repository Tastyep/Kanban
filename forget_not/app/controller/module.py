from .cli_controller import CommandLineController


class ControllerModule(object):
    def setup_controllers(self, app_facade, repo_facade):
        self._cmdline = CommandLineController(app_facade, repo_facade)


    def run(self):
        if self._cmdline.run() is False:
            None  # Start GUI
