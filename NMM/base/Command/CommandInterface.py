from abc import ABC, abstractmethod


class AbstractCommand(ABC):
    @abstractmethod
    def execute(self):
        pass
