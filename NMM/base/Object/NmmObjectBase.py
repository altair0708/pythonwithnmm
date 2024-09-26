from NMM.base.Object.NmmObjectBaseInterface import AbstractNMMObjectBase
from abc import ABC


class NmmObjectBase(AbstractNMMObjectBase, ABC):
    def __init__(self):
        self._type = -1

        self._name = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        from NMM.base.CacheBase.EntranceCache import entrance_cache
        entrance_cache.add_item(value, self)

    @property
    def type(self):
        return self._type
