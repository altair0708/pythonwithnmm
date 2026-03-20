from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelInitialCrackSurface(AbstractCommand):
    def __init__(self):
        self.__crack_surface: VtkGrid = entrance_cache.get_item('crack_surface_VtkGrid')

    def execute(self):
        for each_cell_id in range(self.__crack_surface.get_cell_number()):
            self.__crack_surface.set_attribute('material_id', each_cell_id, 0)

            center = self.__crack_surface.get_surface_center_2d(each_cell_id)
            self.__crack_surface.set_attribute('center_coordinate_0', each_cell_id, center)
            self.__crack_surface.set_attribute('center_coordinate_1', each_cell_id, center)
