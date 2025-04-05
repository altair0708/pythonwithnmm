import numpy as np
from NMM.base.Property.Implement import PropertyList
from typing import List


def displacement_interpolation(point_coordinate: List, math_point_displacement: PropertyList, math_point_coordinate: PropertyList):

    temp_delta_matrix = delta_matrix(math_point_coordinate)
    
    point_coordinate = np.array(point_coordinate, dtype=np.float64).reshape((1, 3))

    math_point_displacement = math_point_displacement.value
    math_point_displacement = np.array(math_point_displacement, dtype=np.float64).reshape(12, 1)

    assert temp_delta_matrix.shape == (4, 4)
    temp_T = T_shape_matrix(1, point_coordinate[0][0], point_coordinate[0][1], point_coordinate[0][2], temp_delta_matrix)
    temp_displacement = np.dot(temp_T, math_point_displacement).reshape((3,))
    return temp_displacement


def delta_matrix(math_point_coordinate: PropertyList):
    math_point_coordinate = math_point_coordinate.value
    temp_delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(math_point_coordinate, dtype=np.float64)]
    temp_delta_matrix = np.matrix(temp_delta_matrix)
    temp_delta_matrix = temp_delta_matrix.I
    temp_delta_matrix = temp_delta_matrix.T
    assert temp_delta_matrix.shape == (4, 4)
    return temp_delta_matrix


def T_shape_matrix(S: float, xS: float, yS: float, zS: float, temp_delta_matrix: np.ndarray):
    def weight_matrix(s, xs, ys, zs):
        return np.dot(temp_delta_matrix, np.array([[s], [xs], [ys], [zs]], dtype=np.float64))
    assert weight_matrix(1, 1, 1, 1).shape == (4, 1)
    We1 = np.array(weight_matrix(S, xS, yS, zS))[0][0]
    We2 = np.array(weight_matrix(S, xS, yS, zS))[1][0]
    We3 = np.array(weight_matrix(S, xS, yS, zS))[2][0]
    We4 = np.array(weight_matrix(S, xS, yS, zS))[3][0]
    T_shape_matrix = np.c_[We1 * np.identity(3), We2 * np.identity(3), We3 * np.identity(3), We4 * np.identity(3)]
    assert T_shape_matrix.shape == (3, 12)
    return T_shape_matrix
