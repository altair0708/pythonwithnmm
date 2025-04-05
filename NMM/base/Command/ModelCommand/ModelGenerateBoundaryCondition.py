from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.CacheBase import entrance_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class ModelGenerateBoundaryCondition(AbstractCommand):
    def __init__(self):
        self.__special_point = entrance_cache.get_item('special_point_VtkGrid')
        self.__boundary_condition: VtkGrid = entrance_cache.get_item('boundary_condition_VtkGrid')

    def execute(self):
        for each_point in self.__special_point:
            self.__boundary_condition.add_item(each_point)
