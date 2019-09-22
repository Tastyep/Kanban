from dataclasses import astuple


class Entity(object):
    def __init__(self, state):
        self._state = state

    @property
    def id(self):
        return self._state.id

    def state(self):
        return astuple(self._state)
