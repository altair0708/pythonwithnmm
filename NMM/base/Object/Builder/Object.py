from NMM.base.Object.NmmObjectBase import NmmObjectBase
from NMM.base.Object.Builder.ObjectInterface import AbstractObjectEntity
from abc import ABC


class Object(AbstractObjectEntity, NmmObjectBase, ABC):
    def __init__(self):
        super().__init__()
        self.__property_dict = {}

    def add_property(self, new_property):
        self.__property_dict[new_property.name] = new_property

    def get_property(self, property_name):
        return self.__property_dict[property_name].value
