from abc import ABC, abstractmethod
from NMM.base.GeometricEntity.Property.PropertyInterface import AbstractProperty


class AbstractGeometricEntityBase(ABC):

    @abstractmethod
    def add_property(self, new_property: AbstractProperty):
        pass

    @abstractmethod
    def get_property(self, name: str):
        pass

