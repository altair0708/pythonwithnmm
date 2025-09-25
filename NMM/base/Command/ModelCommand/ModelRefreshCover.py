from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.CoverRefresher.CoverRefresherNew import CoverRefresher
from NMM.base.Algorithm.ElementRefresher.ElementRefresherNew import ElementRefresher
from NMM.base.CacheBase import entrance_cache


class ModelRefreshCover(AbstractCommand):
    def __init__(self):
        self.__matrix_solver = entrance_cache.get_item('matrix_solver_Part')
        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        displacement_vector = self.__matrix_solver.get_property('displacement_vector').value
        mathematics_point = self.__mathematics_point
        new_cover = self.__new_cover

        cover_refresher = CoverRefresher(displacement_vector, mathematics_point, new_cover)
        cover_refresher.update()
