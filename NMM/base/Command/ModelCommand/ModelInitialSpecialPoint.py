from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache
from NMM.base.Algorithm.SpecialPointAdder import SpecialPointAdder
from NMM.base.Algorithm.CopyCellData import CopyCellData


class ModelInitialSpecialPoint(AbstractCommand):
    def __init__(self):
        self.__manifold_element = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__special_point = entrance_cache.get_item('special_point_VtkGrid')
        self.__boundary_condition = entrance_cache.get_item('boundary_condition_VtkGrid')

    def execute(self):
        special_point_adder = SpecialPointAdder(self.__manifold_element, self.__special_point)
        special_point_adder.update()

        copy_cell_data = CopyCellData(self.__special_point, self.__boundary_condition)
        copy_cell_data.update()


