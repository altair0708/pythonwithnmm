from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelWriteFile(AbstractCommand):
    def __init__(self, grid_name: str, data_structure: DataStructure):
        self.__data_structure = data_structure
        self.__grid_name = grid_name

    def execute(self):
        self.__data_structure.write_file(self.__grid_name)
