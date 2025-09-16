from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.GenerateGrid.GenerateGeometricShell import GenerateGeometricShell
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelGenerateGeometricShell(AbstractCommand):
    def __init__(self, data_structure: DataStructure):
        self.__data_structure = data_structure

    def execute(self):
        geometric_tetrahedron = self.__data_structure.get_property('geometric_tetrahedron')
        geometric_shell = self.__data_structure.get_property('geometric_shell')
        algorithm = GenerateGeometricShell(geometric_tetrahedron, geometric_shell)
        algorithm.update()
        # print('GenerateGeometricShell')
