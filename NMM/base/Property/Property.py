from NMM.base.Object.NmmObjectBase import NmmObjectBase
from NMM.base.Property.PropertyInterface import AbstractProperty


class Property(AbstractProperty, NmmObjectBase):
    def __init__(self):
        super(Property, self).__init__()
        self._value = None

    @property
    def value(self):
        return self._value
