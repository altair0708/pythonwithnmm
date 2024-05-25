from NMM.base.GeometricEntity.GeometricEntityBaseInterface import AbstractGeometricEntityBase
from NMM.base.ObjectBase.NmmObjectBase import NmmObjectBase


class GeometricEntityBase(AbstractGeometricEntityBase, NmmObjectBase):
    def __init__(self):
        super.__init__()
        self.__property_dict = {}

    def add_property(self, new_property):
        self.__property_dict[new_property.name] = new_property

    def get_property(self, property_name):
        return self.__property_dict[property_name]
