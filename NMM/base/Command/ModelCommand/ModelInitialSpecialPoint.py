from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import entrance_cache
from NMM.base.Algorithm.SpecialPointAdder import SpecialPointAdder
from NMM.base.Algorithm.CopyCellData import CopyCellData


class ModelInitialSpecialPoint(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__special_point: VtkGrid = entrance_cache.get_item('special_point_VtkGrid')
        self.__boundary_condition: VtkGrid = entrance_cache.get_item('boundary_condition_VtkGrid')

    def execute(self):
        special_point_adder = SpecialPointAdder(self.__manifold_element, self.__special_point)
        special_point_adder.update()

        copy_cell_data = CopyCellData(self.__special_point, self.__boundary_condition)
        copy_cell_data.update()

        for each_cell_id in range(self.__boundary_condition.get_cell_number()):
            self.__boundary_condition.set_attribute('special_point_displacement_total', each_cell_id, (0, 0, 0))
            self.__boundary_condition.set_attribute('special_point_displacement_increment', each_cell_id, (0, 0, 0))

            point_coordinate = self.__boundary_condition.get_point_coordinate(each_cell_id)
            self.__boundary_condition.set_attribute('special_point_coordinate', each_cell_id, point_coordinate)



