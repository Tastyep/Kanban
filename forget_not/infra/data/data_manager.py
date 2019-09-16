from .data_facade import DataFacade
from .mapper import type_adapter


class DataManager(object):
    def __init__(self, sql, data_factory):
        self._sql = sql
        self._data_factory = data_factory
        self._db = None

    def __del__(self):
        if self._db is not None:
            self._db.close()

    def connect(self, db_name):
        type_adapter.register_adapters(self._sql)
        try:
            self._db = self._sql.connect(db_name, detect_types=self._sql.PARSE_DECLTYPES)
        except self._sql.Error as e:
            print("Could not connect to database '{}': {}".format(db_name, e))
            return None
        return DataFacade(self._data_factory, self._db)
