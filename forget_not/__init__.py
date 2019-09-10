import sys
import sqlite3

from .interface.module import InterfaceModule
from .app.facade import AppFacade
from .app.service.module import ServiceModule
from .app.command.user_commands import AddUser

from infra.repo.factory import Factory as RepoFactory
from infra.repo.facade import Facade as RepoFacade


def _real_main(argv):
    app_facade = AppFacade()
    interface = InterfaceModule(app_facade)
    service_module = ServiceModule()

    db = _connect_to_db('forget_not.db')
    repo_factory = RepoFactory()
    repo_facade = RepoFacade(repo_factory, db)
    service_module.register_services(app_facade, repo_facade)

    interface.run()


def _connect_to_db(name):
    try:
        db = sqlite3.connect(name)
    except sqlite3.Error as e:
        print("Could not connect to database '{}': {}".format(name, e))
        sys.exit(1)
    return db


def main(argv=None):
    try:
        _real_main(argv)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
