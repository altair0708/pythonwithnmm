from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelGenerateCover(AbstractCommand):

    def __init__(self, cover_name: str, data_structure: DataStructure):
        self.__cover_name = cover_name
        self.__data_structure = data_structure

    def execute(self):
        self.__data_structure.generate_cover(self.__cover_name)

