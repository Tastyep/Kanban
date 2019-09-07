from command.dispatcher import CommandDispatcher


class AppFacade(object):
    def __init__(self):
        self._cmd_dispatcher = CommandDispatcher()

    def command_dispatcher(self):
        return self._cmd_dispatcher
