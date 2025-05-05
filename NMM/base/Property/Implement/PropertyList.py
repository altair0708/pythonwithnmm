from NMM.base.Property.Property import Property
from typing import List


class PropertyList(Property):
    def __init__(self, value):
        super(PropertyList, self).__init__()
        self._type = 'PropertyList'
        self._name = ''
        self._value: List = value

    def __iter__(self):
        return iter(self._value)

    def append(self, value):
        self._value.append(value)

    def clear(self):
        self._value.clear()



