from abc import ABC, abstractmethod


class AbstractNMMObjectBase(ABC):
    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass
