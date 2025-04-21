from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelInitialNewCover(AbstractCommand):
    def __init__(self):
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        global_variable_cache.add_item('new_cover_number', self.__new_cover.get_cell_number())
        for each_point_id in range(self.__new_cover.get_point_number()):
            point_coordinate = self.__new_cover.get_point_coordinate(each_point_id)
            self.__new_cover.set_attribute('math_cover_coordinate', each_point_id, point_coordinate)
            self.__new_cover.set_attribute('math_cover_displacement_total', each_point_id, (0, 0, 0))
            self.__new_cover.set_attribute('math_cover_displacement_increment', each_point_id, (0, 0, 0))

