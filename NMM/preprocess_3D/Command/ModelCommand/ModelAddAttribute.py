from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Model.Model import Model
from NMM.preprocess_3D.Command.PartCommand.PartAddAttribute import PartAddAttribute


class ModelAddAttribute(AbstractCommand):
    def __init__(self, model: Model, grid_name: str, attribute_name: str):
        self.__model = model
        self.__grid_name = grid_name
        self.__attribute_name = attribute_name

    def execute(self):
        pass
