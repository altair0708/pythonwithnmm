from abc import ABC, abstractmethod


class AbstractConstructor(ABC):
    @abstractmethod
    def build(self, *args):
        pass
