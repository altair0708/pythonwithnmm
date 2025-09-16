from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.CrackPropagater.CalculateHalfAnglePlane import AngleHalf
from NMM.base.Algorithm.ElementCracker.Criterion.MohrCoulomb import MohrCoulomb
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress
from NMM.base.VTKBase.find_close_cell import find_close_cell
import numpy as np


class CrackPropagateVectorOnShell(AbstractAlgorithm):
    def __init__(self, id_value: int, crack_tip: VtkGrid, manifold_element: VtkGrid):
        self.__id_value = id_value
        self.__crack_tip = crack_tip
        self.__manifold_element = manifold_element

        # result
        self.__direction_vector = None

    @property
    def direction_vector(self):
        return self.__direction_vector

    def update(self, *args, **kwargs):
        crack_point_id = self.__id_value
        crack_tip = self.__crack_tip
        manifold_element = self.__manifold_element

        crack_point_coordinate = crack_tip.get_point_coordinate(crack_point_id)
        element_id = find_close_cell(vtk_model=manifold_element.value, point_coord=crack_point_coordinate)

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
                intersection_vector = intersection_vector / (magnitude * 5)

        else:
            intersection_vector = np.array([0, 0, 0])

        self.__direction_vector = intersection_vector



