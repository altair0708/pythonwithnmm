from abc import ABC, abstractmethod
from NMM.base.Property.PropertyInterface import AbstractProperty


class AbstractCompositeObject(ABC):

    @abstractmethod
    def add_property(self, new_property: AbstractProperty):
        pass

    @abstractmethod
    def get_property(self, name: str):
        pass
