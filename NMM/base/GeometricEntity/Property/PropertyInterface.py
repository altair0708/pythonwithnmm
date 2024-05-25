from abc import ABC, abstractmethod


class AbstractProperty(ABC):

    @abstractmethod
    @property
    def name(self):
        pass

    @abstractmethod
    @property
    def type(self):
        pass

    @abstractmethod
    @property
    def value(self):
        pass
