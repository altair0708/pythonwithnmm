from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.SpecialPointRefresher.SpecialPointRefresher import SpecialPointRefresher
from NMM.base.CacheBase import entrance_cache


class ModelRefreshBoundaryCondition(AbstractCommand):
    def __init__(self):
        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')
        self.__boundary_condition = entrance_cache.get_item('boundary_condition_VtkGrid')

    def execute(self):
        mathematics_point = self.__mathematics_point
        boundary_condition = self.__boundary_condition

        special_point_refresher = SpecialPointRefresher(mathematics_point, boundary_condition)
        special_point_refresher.update()
