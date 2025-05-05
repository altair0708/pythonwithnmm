from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase import calculate_polygon_angle


class CalculateDihedralAngle(AbstractAlgorithm):
    def __init__(self, adjacent_crack_id):
        self.__adjacent_crack_id = adjacent_crack_id
        self.__crack_surface = None
        self.__angle = -1

    @property
    def crack_surface(self):
        return self.__crack_surface

    @crack_surface.setter
    def crack_surface(self, value):
        self.__crack_surface = value

    @property
    def angle(self):
        return self.__angle

    def update(self, *args, **kwargs):
        if self.__crack_surface is None:
            raise Exception('Don\'t initial crack_surface!!!')

        from NMM.base.CacheBase import entrance_cache

        crack_surface = self.__crack_surface
        crack_surface_grid = entrance_cache.get_item('crack_surface_VtkGrid')
        adjacent_crack_surface = crack_surface_grid[self.__adjacent_crack_id]

        self.__angle = calculate_polygon_angle(crack_surface, adjacent_crack_surface)

