import sys
import sqlite3
import os

from .interface.module import InterfaceModule
from .app.facade import AppFacade
from .app.service.module import ServiceModule

from .infra.data.repo.factory import Factory as RepoFactory
from .infra.data.data_manager import DataManager
from .config import config


def _real_main(argv):
    app_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config.load_from_file('{}/config.ini'.format(app_path))

    app_facade = AppFacade()
    service_module = ServiceModule()

    repo_factory = RepoFactory()
    data_manager = DataManager(sqlite3, repo_factory)
    data_facade = data_manager.connect('forget_not.db')
    if data_facade is None:
        return 1

    service_module.register_services(app_facade, data_facade)
    interface = InterfaceModule(app_facade, data_facade)
    interface.run()


def main(argv=None):
    try:
        _real_main(argv)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
