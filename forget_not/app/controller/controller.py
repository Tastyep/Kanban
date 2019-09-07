class Controller(object):
    def __init__(self, cmd_dispatcher):
        self._cmd_dispatcher = cmd_dispatcher

    def _register_handlers(self, cmd_handlers):
        for cmd, handler in cmd_handlers.items():
            self._cmd_dispatcher.attach(cmd, handler)
