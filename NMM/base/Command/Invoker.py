from NMM.base.Command.InvokerInterface import AbstractInvoker
from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.singleton import singleton
from queue import Queue


class Invoker(AbstractInvoker):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, command: AbstractCommand = None):
        self.__command = command

    def set_command(self, command: AbstractCommand):
        self.__command = command

    def press_button(self):
        result = self.__command.execute()

        if result is not None:
            return result


@singleton
class InvokerQueue(AbstractInvoker):
    def __init__(self, command: AbstractCommand = None):
        self.__command_queue = Queue()
        if command is not None:
            self.__command_queue.put(command)

    def set_command(self, command: AbstractCommand):
        self.__command_queue.put(command)

    def press_button(self):
        for each_command in self.__command_queue.queue:
            each_command.execute()
