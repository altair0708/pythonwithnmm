from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.get_point_cell import get_point_cell
from NMM.base.VTKBase.get_angle_bisector import get_angle_bisector
from NMM.base.VTKBase.get_point_cell_id import get_point_cell_id
from NMM.base.Algorithm.Debuger import Debuger
from copy import deepcopy
import numpy as np


class AngleHalf(AbstractAlgorithm):
    def __init__(self, id_value: int, crack_tip: VtkGrid):
        self.__id_value = id_value
        self.__crack_tip = crack_tip

        # result
        self.__origin = None
        self.__bisector = None
        self.__normal = None

        self.__e1 = None
        self.__e2 = None
        self.__e3 = None

    @property
    def origin(self):
        return self.__origin

    @property
    def normal(self):
        return self.__normal

    @property
    def e1(self):
        return self.__e1

    @property
    def e2(self):
        return self.__e2

    @property
    def e3(self):
        return self.__e3

    def update(self, *args, **kwargs):
        id_value = self.__id_value
        crack_tip = self.__crack_tip
        # edge_grid = get_point_cell(crack_tip, id_value)
        cell_id_list = crack_tip.get_point_cell_id(id_value)
        coordinate_0 = np.array(crack_tip.get_point_coordinate(id_value), dtype=np.float64)

        temp_list = deepcopy(cell_id_list)

        cell_id_list = filter(lambda x: crack_tip.is_empty_cell(x) is False, cell_id_list)
        cell_id_list = list(cell_id_list)

        if len(cell_id_list) !=2:
            debug = Debuger()
            debug.update(crack_tip.value, 'crack_tip.vtu')
            print(id_value)
            print(cell_id_list)
            print(temp_list)

        assert len(cell_id_list) == 2, f'{cell_id_list}'

        temp_id = crack_tip.get_cell_point_id(cell_id_list[0])
        temp_id.remove(id_value)
        coordinate_1 = np.array(crack_tip.get_point_coordinate(temp_id[0]), dtype=np.float64)

        temp_id = crack_tip.get_cell_point_id(cell_id_list[1])
        temp_id.remove(id_value)
        coordinate_2 = np.array(crack_tip.get_point_coordinate(temp_id[0]), dtype=np.float64)

        vector_1 = coordinate_1 - coordinate_0
        vector_1 = vector_1 / np.linalg.norm(vector_1)
        assert np.linalg.norm(vector_1) > 0.00001

        vector_2 = coordinate_0 - coordinate_2
        vector_2 = vector_2 / np.linalg.norm(vector_2)
        assert np.linalg.norm(vector_2) > 0.00001

        normal = vector_1 + vector_2
        # print('####AngleHalfAlgorithm####')
        normal = normal / np.linalg.norm(normal)
        self.__normal = normal

        n = np.asarray(normal, dtype=np.float64)
        nunit = n / np.linalg.norm(n)
        # 选取一个与 n 不共线的向量 a
        if abs(nunit[0]) < 0.9:
            a = np.array([1.0, 0.0, 0.0])
        else:
            a = np.array([0.0, 1.0, 0.0])
        e1 = a - (a @ nunit) * nunit
        e1 /= np.linalg.norm(e1)
        e2 = np.cross(nunit, e1)
        e2 /= np.linalg.norm(e2)

        self.__e1 = e1
        self.__e2 = e2
        self.__e3 = normal

