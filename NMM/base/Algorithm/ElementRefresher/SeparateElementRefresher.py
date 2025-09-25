from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.PropertyList import PropertyList
from NMM.base.Property.Implement.Relationship import Relationship
from NMM.base.Algorithm.ElementRefresher import displacement_interpolation
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.VTKBase.write_file import write_file
from typing import List
import numpy as np


class SeparateElementRefresher(AbstractAlgorithm):
    def __init__(self, element_id: int, cover: VtkGrid, element: VtkGrid, relationship_list: List[Relationship]):
        self.__element_id = element_id
        self.__cover = cover
        self.__element = element
        self.__relationship_list = relationship_list

    def update(self, *args, **kwargs):
        cover_id = [each_relationship['newcover'] for each_relationship in self.__relationship_list]
        assert len(cover_id) == 4
        point_id = self.__element.get_cell_point_id(self.__element_id)

        cover_displacement = PropertyList(
            [self.__cover.get_cell_attribute('math_cover_displacement_increment', i) for i in cover_id])
        cover_coordinate = PropertyList([self.__cover.get_point_coordinate(i) for i in cover_id])

        strain_total = self.__element.get_cell_attribute('initial_strain_total', self.__element_id)
        strain_increment = generate_strain_increment(cover_coordinate, cover_displacement)
        strain_total = np.array(strain_total, dtype=np.float64) + np.array(strain_increment, dtype=np.float64)
        self.__element.set_cell_attribute('initial_strain_total', self.__element_id, strain_total)

        for each_id in point_id:
            point_coordinate = self.__element.get_point_coordinate(each_id)

            displacement_increment = displacement_interpolation(point_coordinate, cover_displacement, cover_coordinate)
            self.__element.set_point_attribute('point_displacement_increment', each_id, displacement_increment)

            displacement_total = self.__element.get_point_attribute('point_displacement_total', each_id)
            displacement_total = np.array(displacement_total, dtype=np.float64) + np.array(displacement_increment, dtype=np.float64)
            self.__element.set_point_attribute('point_displacement_total', each_id, displacement_total)

            temp_point_coordinate = self.__element.get_point_attribute('point_coordinate', each_id)
            temp_point_coordinate = np.array(temp_point_coordinate, dtype=np.float64) + np.array(displacement_increment, dtype=np.float64)
            self.__element.set_point_attribute('point_coordinate', each_id, temp_point_coordinate)

            time_increment = global_variable_cache.get_item('time_increment')
            initial_velocity = self.__element.get_point_attribute('point_velocity', each_id)
            current_velocity = np.array(displacement_increment, dtype=np.float64) * 2 / time_increment - np.array(initial_velocity, dtype=np.float64)
            self.__element.set_point_attribute('point_velocity', each_id, current_velocity)


def generate_B_shape_matrix(math_cover_coordinate: PropertyList):
    delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(math_cover_coordinate.value, dtype=np.float64)]
    delta_matrix = np.matrix(delta_matrix)
    delta_matrix = delta_matrix.I
    delta_matrix: np.matrix = delta_matrix.T

    B_shape_matrix = np.empty((6, 0), dtype=np.float64)
    for i in range(4):
        temp_B = np.array([[delta_matrix[i, 1],                  0,                  0],
                           [                 0, delta_matrix[i, 2],                  0],
                           [                 0,                  0, delta_matrix[i, 3]],
                           [delta_matrix[i, 2], delta_matrix[i, 1],                  0],
                           [                 0, delta_matrix[i, 3], delta_matrix[i, 2]],
                           [delta_matrix[i, 3],                  0, delta_matrix[i, 1]]])
        B_shape_matrix = np.c_[B_shape_matrix, temp_B]
    assert B_shape_matrix.shape == (6, 12)
    return B_shape_matrix


def generate_strain_increment(cover_coordinate: PropertyList, cover_displacement: PropertyList):
    B_shape_matrix: np.matrix = generate_B_shape_matrix(cover_coordinate)

    temp_displacement = np.array(cover_displacement.value, dtype=np.float64).reshape((12, 1))
    temp_displacement = np.dot(B_shape_matrix, temp_displacement).reshape((6, ))

    return temp_displacement
