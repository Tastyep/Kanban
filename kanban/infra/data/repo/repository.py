from pypika import (
    Query,
    Table,
)
from pypika import functions as fn

from ..mapper.placeholder import (
    AnonPlaceHolder,
    PlaceHolder,
)


class Repository(object):
    def __init__(self, db, table, entity_factory):
        self._db = db
        self._table = table
        self._entity_factory = entity_factory

    def create(self, entity):
        state = entity.state()
        params = AnonPlaceHolder(len(state))
        q = Query.into(Table(self._table)).insert(params)
        self._write(q, tuple(state.values()))

    def update(self, key, state):
        entity = Table(self._table)
        q = Query.update(entity).set(
            key, PlaceHolder('value')
        ).where(
            entity.id == PlaceHolder('id')
        )
        self._write(q, {'value': state[key], 'id': state['id']})

    def delete(self, id):
        entity = Table(self._table)
        q = Query.from_(entity).where(
            entity.id == PlaceHolder('id')
        ).delete()
        self._write(q, {'id': id})

    def count(self):
        entity = Table(self._table)
        q = Query.from_().select(
            fn.Count(entity.star)
        )
        return self._fetchone(q)

    def list(self):
        entity = Table(self._table)
        q = Query.from_(entity).select(
            entity.Star()
        )
        return self._fetchall(q)

    def find_by_id(self, id):
        entity = Table(self._table)
        q = Query.from_(entity).select(
            entity.star
        ).where(
            entity.id == PlaceHolder('id')
        )
        return self._fetchone(q, {'id': id})

    def _exec_query(self, query, params):
        cursor = self._db.cursor()
        cursor.execute(str(query), params)
        return cursor

    def _create_table(self, layout):
        q = 'CREATE TABLE IF NOT EXISTS {}({})'.format(self._table, layout)
        self._write(q)

    def _fetchone(self, query, params=()):
        entity = self._exec_query(query, params).fetchone()
        found = entity is not None
        if isinstance(entity, tuple):
            found = any(v is not None for v in entity)
        return self._entity_factory(entity) if found else None

    def _fetchmany(self, query, params=()):
        entities = self._exec_query(query, params).fetchmany()
        for i, e in enumerate(entities):
            entities[i] = self._entity_factory(e)
        return entities

    def _fetchall(self, query, params=()):
        entities = self._exec_query(query, params).fetchall()
        for i, e in enumerate(entities):
            entities[i] = self._entity_factory(e)
        return entities

    def _write(self, query, params=()):
        self._exec_query(query, params)
        self._db.commit()
