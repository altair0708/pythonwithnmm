from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelInitialNewElement(AbstractCommand):
    def __init__(self):
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')

    def execute(self):
        for each_cell_id in range(self.__new_element.get_cell_number()):
            self.__new_element.set_attribute('material_id', each_cell_id, 0)
            self.__new_element.set_attribute('initial_strain_total', each_cell_id, (0, 0, 0, 0, 0, 0))
        global_variable_cache.add_item('new_element_number', self.__new_element.get_cell_number())

        for each_point_id in range(self.__new_element.get_point_number()):
            point_coordinate = self.__new_element.get_point_coordinate(each_point_id)
            self.__new_element.set_attribute('point_coordinate', each_point_id, point_coordinate)
            self.__new_element.set_attribute('point_displacement_total', each_point_id, (0, 0, 0))
            self.__new_element.set_attribute('point_displacement_increment', each_point_id, (0, 0, 0))
            self.__new_element.set_attribute('point_velocity', each_point_id, (0, 0, 0))
