from pypika import (
    Query,
    Table,
)
from pypika import functions as fn


class Repository(object):
    def __init__(self, db, table):
        self._db = db
        self._table = table

    def create(self, entity):
        q = Query.into(Table(self._table)).insert(entity.state())
        self._exec_query(q)

    def count(self):
        q = Query.from_(Table(self._table)).select(
            fn.Count('*')
        )
        self._exec_query(q)

    def find_by_id(id):
        return None

    def _exec_query(self, query):
        cursor = self._db.cursor()
        cursor.execute(str(query))
        self._db.commit()

    def _create_table(self, layout):
        self._exec_query("CREATE TABLE IF NOT EXISTS {}({})".format(self._table, layout))
