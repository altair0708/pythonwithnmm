from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.get_point_cell import get_point_cell
from NMM.base.VTKBase.get_angle_bisector import get_angle_bisector


class AngleHalf(AbstractAlgorithm):
    def __init__(self, id_value: int, crack_tip: VtkGrid):
        self.__id_value = id_value
        self.__crack_tip = crack_tip

        # result
        self.__origin = None
        self.__bisector = None
        self.__normal = None

    @property
    def origin(self):
        return self.__origin

    @property
    def normal(self):
        return self.__normal

    def update(self, *args, **kwargs):
        id_value = self.__id_value
        crack_tip = self.__crack_tip.value
        edge_grid = get_point_cell(crack_tip, id_value)
        try:
            origin, bisector, normal = get_angle_bisector(edge_grid)
            # print(f'origin:{origin}')
            # print(f'normal:{normal}')
            self.__origin = origin
            self.__normal = normal
        except Exception as e:
            print("❌ 错误:", e)

