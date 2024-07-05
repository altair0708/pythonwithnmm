from NMM.base.Command.CommandInterface import AbstractCommand


class ModelBuilderEntity(AbstractCommand):
    def __init__(self, element_list, data_structure):
        self.__element_list = element_list
        self.__data_structure = data_structure

    # TODO
    def execute(self):
        pass
