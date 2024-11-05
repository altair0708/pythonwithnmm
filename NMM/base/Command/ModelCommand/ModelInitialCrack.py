from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Algorithm.InitialCrackGenerator import InitialCrackGenerator
from NMM.preprocess_3D.Part.DataStructure.DataStructure import DataStructure


class ModelInitialCrack(AbstractCommand):

    def __init__(self):
        self.__data_structure: DataStructure = entrance_cache.get_item('data_structure_Part')

    def execute(self):
        initial_crack_algorithm = InitialCrackGenerator(
            initial_crack_grid=self.__data_structure.get_property('initial_crack'),
            new_cover_grid=self.__data_structure.get_property('new_cover'),
            new_element_grid=self.__data_structure.get_property('new_element'),
            new_surface_grid=self.__data_structure.get_property('new_surface'),
            mathematics_point_grid=self.__data_structure.get_property('mathematics_point'),
            manifold_element_grid=self.__data_structure.get_property('manifold_element'),
            element_surface_grid=self.__data_structure.get_property('element_surface'),
            crack_surface_grid=self.__data_structure.get_property('crack_surface'),
            crack_edge_grid=self.__data_structure.get_property('crack_edge'))
        initial_crack_algorithm.update()
