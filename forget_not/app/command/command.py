class Command(object):
    def __init__(self, entity_id):
        self._entity_id = entity_id

    def entity_id(self):
        return self._entity_id
