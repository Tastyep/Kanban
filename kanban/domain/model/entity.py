from dataclasses import asdict


class Entity(object):
    def __init__(self, state):
        self._state = state

    @property
    def id(self):
        return self._state.id

    def state(self):
        return asdict(self._state)
