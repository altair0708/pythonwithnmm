from NMM.base.Command.InvokerInterface import AbstractInvoker
from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.singleton import singleton


@singleton
class Invoker(AbstractInvoker):
    def __init__(self, command: AbstractCommand):
        self.__command = command

    def set_command(self, command: AbstractCommand):
        self.__command = command

    def press_button(self):
        self.__command.execute()
