from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.CoverRefresher import CoverRefresher
from NMM.base.CacheBase import entrance_cache


# TODO: refresh cover
class ModelRefreshCover(AbstractCommand):
    def __init__(self):
        self.__matrix_solver = entrance_cache.get_item('matrix_solver_Part')
        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        refresher = CoverRefresher(self.__matrix_solver, self.__mathematics_point, self.__new_cover)
        refresher.update()
