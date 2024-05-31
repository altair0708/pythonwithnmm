from abc import ABC, abstractmethod
from NMM.base.Command.CommandInterface import AbstractCommand


class AbstractInvoker(ABC):
    @abstractmethod
    def set_command(self, command: AbstractCommand):
        pass

    @abstractmethod
    def press_button(self):
        pass

