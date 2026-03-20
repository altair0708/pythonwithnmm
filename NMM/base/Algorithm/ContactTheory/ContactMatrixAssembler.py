from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Property.Implement.PropertyMatrix import PropertyMatrix
from NMM.base.Property.Implement.PropertyVector import PropertyVector
from NMM.base.SimplexIntegralBase.tetrahedron_integral import once_integration, twice_integration
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.LogBase.matrix_save import new_matrix_save
from typing import List
import numpy as np


class ContactAssembler(AbstractAlgorithm):
    def __init__(self, crack_surface: ElementBase, step: int):
        self.__crack_surface = crack_surface
        self.__time_step = step

    def update(self, *args, **kwargs):
        generate_delta_matrix(self.__crack_surface)
        generate_contact_matrix(self.__crack_surface)


def generate_delta_matrix(element: ElementBase):
    math_cover_coordinate: List = element.get_property('math_cover_coordinate_0').value
    delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(math_cover_coordinate, dtype=np.float64)]
    delta_matrix = np.matrix(delta_matrix)
    delta_matrix = delta_matrix.I
    delta_matrix: np.matrix = delta_matrix.T
    assert delta_matrix.shape == (4, 4)

    temp_matrix = PropertyMatrix(delta_matrix)
    temp_matrix.set_name('delta_matrix')
    element.add_property(temp_matrix)


def generate_T_shape_matrix(S: float, xS: float, yS: float, zS: float, delta_matrix: np.ndarray):
    def weight_matrix(s, xs, ys, zs):
        return np.dot(delta_matrix, np.array([[s], [xs], [ys], [zs]], dtype=np.float64))
    assert weight_matrix(1, 1, 1, 1).shape == (4, 1)
    We1 = np.array(weight_matrix(S, xS, yS, zS))[0][0]
    We2 = np.array(weight_matrix(S, xS, yS, zS))[1][0]
    We3 = np.array(weight_matrix(S, xS, yS, zS))[2][0]
    We4 = np.array(weight_matrix(S, xS, yS, zS))[3][0]
    T_shape_matrix = np.c_[We1 * np.identity(3), We2 * np.identity(3), We3 * np.identity(3), We4 * np.identity(3)]
    assert T_shape_matrix.shape == (3, 12)
    return T_shape_matrix


def generate_contact_matrix(element: ElementBase):
    temp_penalty = float(element.get_property('material_parameter')['penalty_parameter'])

    point_list = element.get_property('point_coordinate').value
    normal_vector = plane_normal(point_list)

    point_number = len(point_list)
    centre = tuple((sum(x) / point_number) for x in zip(*point_list))

    surface_area = element.get_property('surface_area').value

    cover_displacement_0 = np.array(element.get_property('math_cover_displacement_increment_0').value).reshape(12, 1)
    cover_displacement_1 = np.array(element.get_property('math_cover_displacement_increment_1').value).reshape(12, 1)

    center_coordinate_0 = element.get_property('center_coordinate_0').value
    center_coordinate_1 = element.get_property('center_coordinate_1').value

    CC_matrix = np.zeros((12, 12), dtype=np.float64)
    F_matrix = np.zeros((12, 1), dtype=np.float64)

    delta_matrix = element.get_property('delta_matrix').value
    temp = generate_T_shape_matrix(1, centre[0], centre[1], centre[2], delta_matrix=delta_matrix)
    temp_0 = generate_T_shape_matrix(1, center_coordinate_0[0], center_coordinate_0[1], center_coordinate_0[2], delta_matrix=delta_matrix)
    temp_1 = generate_T_shape_matrix(1, center_coordinate_1[0], center_coordinate_1[1], center_coordinate_1[2], delta_matrix=delta_matrix)
    project_matrix = np.outer(normal_vector, normal_vector)

    CC_00_matrix = CC_matrix + 0.5 * surface_area * temp_penalty * (temp_0.T @ project_matrix @ temp_0)
    CC_11_matrix = CC_matrix + 0.5 * surface_area * temp_penalty * (temp_1.T @ project_matrix @ temp_1)
    CC_01_matrix = CC_matrix + 0.5 * surface_area * temp_penalty * (temp_0.T @ project_matrix @ temp_1)
    CC_10_matrix = CC_matrix + 0.5 * surface_area * temp_penalty * (temp_1.T @ project_matrix @ temp_0)

    F_0_matrix = F_matrix + surface_area * temp_penalty * (temp_0.T @ project_matrix @ (temp_0 @ cover_displacement_0 - temp_1 @ cover_displacement_1))
    F_1_matrix = F_matrix + surface_area * temp_penalty * (temp_1.T @ project_matrix @ (temp_1 @ cover_displacement_1 - temp_0 @ cover_displacement_0))
    # F_0_matrix = F_matrix
    # F_1_matrix = F_matrix

    # CC_matrix = CC_matrix + 0.5 * surface_area * temp_penalty * (temp.T @ project_matrix @ temp)
    # F_matrix = F_matrix + surface_area * temp_penalty * (temp.T @ project_matrix @ (temp @ cover_displacement_0 - temp @ cover_displacement_1))

    assert CC_00_matrix.shape == (12, 12)
    temp_matrix = PropertyMatrix(CC_00_matrix)
    temp_matrix.set_name('CC_00_matrix')
    element.add_property(temp_matrix)

    assert CC_11_matrix.shape == (12, 12)
    temp_matrix = PropertyMatrix(CC_11_matrix)
    temp_matrix.set_name('CC_11_matrix')
    element.add_property(temp_matrix)

    assert CC_01_matrix.shape == (12, 12)
    temp_matrix = PropertyMatrix(CC_01_matrix)
    temp_matrix.set_name('CC_01_matrix')
    element.add_property(temp_matrix)

    assert CC_10_matrix.shape == (12, 12)
    temp_matrix = PropertyMatrix(CC_10_matrix)
    temp_matrix.set_name('CC_10_matrix')
    element.add_property(temp_matrix)

    assert F_0_matrix.shape == (12, 1), f'{F_0_matrix.shape}'
    temp_matrix = PropertyMatrix(F_0_matrix)
    temp_matrix.set_name('F_0_matrix')
    element.add_property(temp_matrix)

    assert F_1_matrix.shape == (12, 1), f'{F_1_matrix.shape}'
    temp_matrix = PropertyMatrix(F_1_matrix)
    temp_matrix.set_name('F_1_matrix')
    element.add_property(temp_matrix)

    assert CC_matrix.shape == (12, 12)
    temp_matrix = PropertyMatrix(CC_matrix)
    temp_matrix.set_name('CC_matrix')
    element.add_property(temp_matrix)

    assert F_matrix.shape == (12, 1), f'{F_matrix.shape}'
    temp_matrix = PropertyMatrix(F_matrix)
    temp_matrix.set_name('F_matrix')
    element.add_property(temp_matrix)

def plane_normal(points):
    """
    输入: points (N,3)
    输出: 单位法向量 normal
    """
    points = np.array(points)

    if len(points) < 3:
        raise ValueError("至少需要三个点")

    centroid = points.mean(axis=0)
    centered = points - centroid

    _, _, vh = np.linalg.svd(centered)

    normal = vh[-1]
    normal = normal / np.linalg.norm(normal)

    return normal
