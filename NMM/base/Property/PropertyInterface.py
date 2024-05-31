from abc import ABC, abstractmethod


class AbstractProperty(ABC):

    @property
    @abstractmethod
    def value(self):
        pass
