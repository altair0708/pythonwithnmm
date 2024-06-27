from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelGenerateGrid(AbstractCommand):
    def __init__(self, entity_name: str, data_structure: DataStructure):
        self.__entity_name = entity_name
        self.__data_structure = data_structure

    def execute(self):
        # self.__data_structure.generate_geometric_grid(self.__geometric_name)
        self.__data_structure.generate_grid(self.__entity_name)
