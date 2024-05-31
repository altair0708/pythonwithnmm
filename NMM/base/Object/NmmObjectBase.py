from NMM.base.Object.NmmObjectBaseInterface import AbstractNMMObjectBase
from abc import ABC


class NmmObjectBase(AbstractNMMObjectBase, ABC):
    def __init__(self):
        self._name = ''
        self._type = -1

    @property
    def name(self):
        return self._name

    @property
    def type(self):
        return self._type
