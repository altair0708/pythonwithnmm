from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelAddAttribute(AbstractCommand):
    def __init__(self, grid_name: str, attribute_name: str, data_structure: DataStructure):
        self.__data_structure = data_structure
        self.__grid_name = grid_name
        self.__attribute_name = attribute_name

    def execute(self):
        self.__data_structure.add_attribute(self.__grid_name, self.__attribute_name)
