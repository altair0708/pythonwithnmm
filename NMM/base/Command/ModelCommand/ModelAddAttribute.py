from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Command.PartCommand.PartAddAttribute import PartAddAttribute
from NMM.base.Command.Invoker import Invoker
from NMM.preprocess_3D.Model.Model import Model


class ModelAddAttribute(AbstractCommand):
    def __init__(self, model: Model, grid_name: str, attribute_name: str):
        self.__model = model
        self.__grid_name = grid_name
        self.__attribute_name = attribute_name

    def execute(self):
        data_structure = self.__model.get_property('DataStructure')
        new_command = PartAddAttribute(data_structure, self.__grid_name, self.__attribute_name)
        invoker = Invoker(new_command)
        invoker.press_button()
