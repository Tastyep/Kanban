import sys
import sqlite3
import os

from .app.app_facade import AppFacade
from .app.service.module import ServiceModule
from .app.controller.module import ControllerModule

from .infra.data.repo.factory import Factory as RepoFactory
from .infra.data.data_manager import DataManager
from .config import config


def _real_main(argv):
    app_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config.load_from_file(f'{app_path}/{__name__}/config.ini')

    app_facade = AppFacade()
    controller_module = ControllerModule()
    service_module = ServiceModule()

    repo_factory = RepoFactory()
    data_manager = DataManager(sqlite3, repo_factory)
    data_facade = data_manager.connect('kanban.db')
    if data_facade is None:
        return 1

    controller_module.setup_controllers(app_facade, data_facade)
    service_module.register_services(app_facade, data_facade)
    controller_module.run()


def main(argv=None):
    try:
        _real_main(argv)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
