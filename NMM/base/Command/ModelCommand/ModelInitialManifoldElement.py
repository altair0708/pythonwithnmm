from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelInitialManifoldElement(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')

    def execute(self):
        global_variable_cache.add_item('element_number', self.__manifold_element.get_cell_number())
        for each_cell_id in range(self.__manifold_element.get_cell_number()):
            self.__manifold_element.set_attribute('material_id', each_cell_id, 0)
            self.__manifold_element.set_attribute('initial_strain_total', each_cell_id, (0, 0, 0, 0, 0, 0))

        for each_point_id in range(self.__manifold_element.get_point_number()):

            point_coordinate = self.__manifold_element.get_point_coordinate(each_point_id)
            self.__manifold_element.set_attribute('point_coordinate', each_point_id, point_coordinate)

            self.__manifold_element.set_attribute('point_displacement_total', each_point_id, (0, 0, 0))
            self.__manifold_element.set_attribute('point_displacement_increment', each_point_id, (0, 0, 0))
            self.__manifold_element.set_attribute('point_velocity', each_point_id, (0, 0, 0))
