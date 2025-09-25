from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.CrackPropagater.CalculateHalfAnglePlane import AngleHalf
from NMM.base.Algorithm.ElementCracker.Criterion.MohrCoulomb import MohrCoulomb
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress
from NMM.base.VTKBase.find_close_cell import find_close_cell
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
import numpy as np


class CrackPropagateSIF(AbstractAlgorithm):
    def __init__(self, id_value: int, crack_tip: VtkGrid, geometric_tetrahedron: VtkGrid):
        self.__id_value = id_value
        self.__crack_tip = crack_tip
        self.__geometric_tetrahedron = geometric_tetrahedron

        # result
        self.__direction_vector = None

    @property
    def direction_vector(self):
        return self.__direction_vector

    def update(self, *args, **kwargs):
        crack_point_id = self.__id_value
        crack_tip = self.__crack_tip
        geometric_tetrahedron = self.__geometric_tetrahedron

        crack_point_coordinate = crack_tip.get_point_coordinate(crack_point_id)
        element_id = find_close_cell(vtk_model=geometric_tetrahedron.value, point_coord=crack_point_coordinate)

        criterion = MaximumTensileStress()
        criterion.set_element_id(element_id)
        criterion.update()
        if criterion.crack_flag is True:
            normal_0 = criterion.normal

            algorithm = AngleHalf(crack_point_id, crack_tip)
            algorithm.update()
            normal_1 = algorithm.normal

            propagate_direction = crack_tip.get_point_attribute('propagate_direction', crack_point_id)
            propagate_direction = np.array(propagate_direction).reshape(-1)

            intersection_vector = np.cross(normal_0, normal_1)
            intersection_vector = np.array(intersection_vector).reshape(-1)

            if np.dot(intersection_vector, propagate_direction) < 0:
                intersection_vector = - intersection_vector

            magnitude = np.linalg.norm(intersection_vector)
            if magnitude != 0:
                try:
                    step = global_variable_cache.get_item('crack_length')
                except AssertionError:
                    step = 0.2
                intersection_vector = intersection_vector * step / magnitude

        else:
            # print('##################')
            # print(crack_point_coordinate)
            # print(element_id)
            intersection_vector = np.array([0, 0, 0])

        self.__direction_vector = intersection_vector



