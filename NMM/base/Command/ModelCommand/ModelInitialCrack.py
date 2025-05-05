from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
# from NMM.base.Algorithm.InitialCrackGenerator import InitialCrackGenerator
from NMM.base.Algorithm.ElementCracker.InitialCracker import InitialCrackGenerator
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelInitialCrack(AbstractCommand):

    def __init__(self):
        self.__data_structure: DataStructure = entrance_cache.get_item('data_structure_Part')

    def execute(self):
        initial_crack_algorithm = InitialCrackGenerator(
            initial_crack_grid=self.__data_structure.get_property('initial_crack'),
            manifold_element_grid=self.__data_structure.get_property('manifold_element'))
        initial_crack_algorithm.update()
