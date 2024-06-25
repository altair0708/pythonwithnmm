from NMM.base.Object.NmmObjectBase import NmmObjectBase
from NMM.base.CompositeObject.CompostieObjectInterface import AbstractCompositeObject
from NMM.base.Property.Property import Property
from abc import ABC


class CompositeObject(AbstractCompositeObject, NmmObjectBase, ABC):
    def __init__(self):
        super().__init__()
        self._property_dict = {}

    def add_property(self, new_property: Property):
        self._property_dict[new_property.name] = new_property

    def get_property(self, property_name):
        return self._property_dict[property_name]
