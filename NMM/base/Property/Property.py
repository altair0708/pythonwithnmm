from NMM.base.Object.NmmObjectBase import NmmObjectBase
from NMM.base.Property.PropertyInterface import AbstractProperty


class Property(NmmObjectBase):
    def __init__(self):
        super(Property, self).__init__()
        self._value = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # Don't put it in the entrance cache.
    def set_name(self, name):
        self._name = name

