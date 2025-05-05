from NMM.base.Command.InvokerInterface import AbstractInvoker
from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.singleton import singleton
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
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


class InvokerCycle(AbstractInvoker):
    def __init__(self, cycle_time: int = None):
        self.__command_list = []
        self.__flag = False  # Read from global_variable_Part

        if cycle_time is None:
            self.__flag = True
            cycle_time: int = global_variable_cache.get_item('total_step')

        self.__cycle_time = cycle_time

    def set_command(self, command: AbstractCommand):
        self.__command_list.append(command)

    def press_button(self):
        for each_step in range(self.__cycle_time):
            for each_command in self.__command_list:
                each_command.execute()
            if self.__flag is True:
                time_step = global_variable_cache.get_item('time_step')
                new_cover_number = global_variable_cache.get_item('new_cover_number')
                new_element_number = global_variable_cache.get_item('new_element_number')
                print(f'new_cover_number: {new_cover_number}')
                print(f'new_element_number: {new_element_number}')
                print(f'time_step: {time_step} end')
                global_variable_cache.add_item('time_step', int(time_step) + 1)
