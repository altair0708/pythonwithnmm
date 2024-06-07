from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelGenerateGeometricGrid(AbstractCommand):
    def __init__(self, geometric_name: str, data_structure: DataStructure):
        self.__geometric_name = geometric_name
        self.__data_structure = data_structure

    def execute(self):
        self.__data_structure.generate_geometric_grid(self.__geometric_name)



