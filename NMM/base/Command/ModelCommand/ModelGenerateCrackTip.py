from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.GenerateGrid.GenerateCrackTip import GenerateCrackTip


class ModelGenerateCrackTip(AbstractCommand):
    def __init__(self, data_structure: DataStructure):
        self.__data_structure = data_structure

    def execute(self):
        initial_crack = self.__data_structure.get_property('initial_crack')
        crack_tip = self.__data_structure.get_property('crack_tip')
        crack_propagation = self.__data_structure.get_property('crack_propagation')

        algorithm = GenerateCrackTip(initial_crack, crack_tip, crack_propagation)
        algorithm.update()

