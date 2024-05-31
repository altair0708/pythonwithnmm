from abc import ABC, abstractmethod


class AbstractProperty(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    @property
    @abstractmethod
    def value(self):
        pass
