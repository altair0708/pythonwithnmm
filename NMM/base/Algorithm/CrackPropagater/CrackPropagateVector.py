from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.CrackPropagater.CalculateHalfAnglePlane import AngleHalf
from NMM.base.Algorithm.ElementCracker.Criterion.MohrCoulomb import MohrCoulomb
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress
from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensilePlaneStress import MaximumTensilePlaneStress
from NMM.base.Algorithm.ElementCracker.Criterion.MohrCoulombPlaneStress import MohrCoulombPlaneStress
from NMM.base.VTKBase.find_close_cell import find_close_cell
from NMM.base.VTKBase.intersection_line_with_polydata import intersection_line_with_polydata
from NMM.base.VTKBase.generate_line import generate_line
from NMM.base.VTKBase.modify_point_coordinate import modify_point_coordinate
from NMM.base.VTKBase.check_line_on_shell import classify_point_vs_closed_surface
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.CacheBase.EntranceCache import entrance_cache
import numpy as np


class CrackPropagateVector(AbstractAlgorithm):
    def __init__(self, id_value: int, crack_tip: VtkGrid, geometric_tetrahedron: VtkGrid):
        self.__id_value = id_value
        self.__crack_tip = crack_tip
        self.__geometric_tetrahedron = geometric_tetrahedron
        self.__geometric_shell: VtkGrid = entrance_cache.get_item('geometric_shell_VtkGrid')

        # result
        self.__direction_vector = None

    @property
    def direction_vector(self):
        return self.__direction_vector

    def update(self, *args, **kwargs):
        crack_point_id = self.__id_value
        crack_tip = self.__crack_tip
        geometric_tetrahedron = self.__geometric_tetrahedron
        geometric_shell = self.__geometric_shell.value

        crack_point_coordinate = crack_tip.get_point_coordinate(crack_point_id)
        element_id = find_close_cell(vtk_model=geometric_tetrahedron.value, point_coord=crack_point_coordinate)

        algorithm = AngleHalf(crack_point_id, crack_tip)
        algorithm.update()

        # criterion = MaximumTensilePlaneStress()
        criterion = MohrCoulombPlaneStress()
        criterion.set_point_coordinate(crack_point_coordinate)
        criterion.set_element_id(element_id)
        criterion.set_plane_normal(algorithm.e1, algorithm.e2, algorithm.e3)
        criterion.update()

        if criterion.crack_flag is True:
            normal_0 = criterion.normal

            propagate_direction = crack_tip.get_point_attribute('propagate_direction', crack_point_id)
            propagate_direction = np.array(propagate_direction).reshape(-1)

            intersection_vector = normal_0
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
            intersection_vector = np.array([0, 0, 0])

        # Maybe crack point go outside the shell
        next_point_coordinate = tuple([crack_point_coordinate[i] + intersection_vector[i] for i in range(3)])
        if classify_point_vs_closed_surface(next_point_coordinate, geometric_shell) == 'outside':
            line_grid = generate_line(crack_point_coordinate, next_point_coordinate)
            result, intersection = intersection_line_with_polydata(geometric_shell, line_grid)
            assert result is True
            intersection_vector = np.array([intersection[i] - crack_point_coordinate[i] for i in range(3)])

        self.__direction_vector = intersection_vector


