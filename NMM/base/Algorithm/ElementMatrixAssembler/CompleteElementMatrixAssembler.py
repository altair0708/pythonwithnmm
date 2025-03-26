from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Property.Implement.PropertyMatrix import PropertyMatrix
from NMM.base.Property.Implement.PropertyVector import PropertyVector
from NMM.base.SimplexIntegralBase.tetrahedron_integral import once_integration, twice_integration
from NMM.base.CacheBase.EntranceCache import entrance_cache
import numpy as np


class CompleteAssembler(AbstractAlgorithm):
    def __init__(self, element: ElementBase):
        self.__element = element

    def update(self, *args, **kwargs):
        time_increment = entrance_cache.get_item('global_variable_PropertyMap')['time_increment']
        pass


def generate_delta_matrix(element: ElementBase):
    math_cover_coordinate = element.get_property('math_cover_coordinate').value
    delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(math_cover_coordinate, dtype=np.float64)]
    # delta_matrix = np.c_[np.ones((4, 1), dtype=np.float64), np.array(self.joint_list, dtype=np.float64)]
    delta_matrix = np.matrix(delta_matrix)
    delta_matrix = delta_matrix.I
    delta_matrix: np.matrix = delta_matrix.T
    # delta_matrix: np.matrix = delta_matrix
    assert delta_matrix.shape == (4, 4)
    # calculated by sympy
    # self.__delta_matrix = f_function(self.patch_list[0], self.patch_list[1], self.patch_list[2], self.patch_list[3])

    temp_matrix = PropertyMatrix(delta_matrix)
    temp_matrix.set_name('delta_matrix')
    element.add_property(temp_matrix)


def generate_B_shape_matrix(element: ElementBase):
    delta_matrix: np.matrix = element.get_property('delta_matrix').value
    # self.__B_shape_matrix = np.array([[delta_matrix[0, 1],                  0, delta_matrix[1, 1],                  0, delta_matrix[2, 1],                  0],
    #                                   [                 0, delta_matrix[0, 2],                  0, delta_matrix[1, 2],                  0, delta_matrix[2, 2]],
    #                                   [delta_matrix[0, 2], delta_matrix[0, 1], delta_matrix[1, 2], delta_matrix[1, 1], delta_matrix[2, 2], delta_matrix[2, 1]]])
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

    temp_matrix = PropertyMatrix(B_shape_matrix)
    temp_matrix.set_name('B_shape_matrix')
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


def generate_elastic_matrix(element: ElementBase):
    temp_E = float(element.get_property('material_parameter')['elastic_modulus'])
    temp_mu = float(element.get_property('mater_parameter')['poisson_ratio'])

    elastic_matrix = temp_E / ((1 + temp_mu) * (1 - 2 * temp_mu)) * \
                     np.matrix([[1 - temp_mu, temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, 1 - temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, temp_mu, 1 - temp_mu, 0, 0, 0],
                                [0, 0, 0, (1 - 2 * temp_mu) / 2, 0, 0],
                                [0, 0, 0, 0, (1 - 2 * temp_mu) / 2, 0],
                                [0, 0, 0, 0, 0, (1 - 2 * temp_mu) / 2]])

    temp_matrix = PropertyMatrix(elastic_matrix)
    temp_matrix.set_name('elastic_matrix')
    element.add_property(temp_matrix)


def generate_stiff_matrix(element: ElementBase):
    point_coordinate = element.get_property('point_coordinate').value
    B_shape_matrix: np.matrix = element.get_property('B_shape_matrix').value
    elastic_matrix: np.matrix = element.get_property('elastic_matrix').value

    temp_S, temp_xS, temp_yS, temp_zS = once_integration(np.array(point_coordinate, dtype=np.float64))
    temp_stiff_matrix = temp_S * B_shape_matrix.T
    temp_stiff_matrix = np.dot(temp_stiff_matrix, elastic_matrix)
    temp_stiff_matrix = np.dot(temp_stiff_matrix, B_shape_matrix)

    stiff_matrix = temp_stiff_matrix
    assert stiff_matrix.shape == (12, 12)

    temp_matrix = PropertyMatrix(stiff_matrix)
    temp_matrix.set_name('stiff_matrix')
    element.add_property(temp_matrix)


def generate_initial_strain_increment(element: ElementBase):
    math_cover_displacement_increment = element.get_property('math_cover_displacement_increment').value
    B_shape_matrix: np.matrix = element.get_property('B_shape_matrix').value

    temp_displacement = np.array(math_cover_displacement_increment, dtype=np.float64).reshape((12, 1))
    temp_displacement = np.dot(B_shape_matrix, temp_displacement)

    temp_vector = PropertyVector(temp_displacement)
    temp_vector.set_name('initial_strain_increment')
    element.add_property(temp_vector)


def generate_initial_strain_total(element: ElementBase):
    math_cover_displacement_total = element.get_property('math_cover_displacement_total').value
    B_shape_matrix: np.matrix = element.get_property('B_shape_matrix').value

    temp_displacement = np.array(math_cover_displacement_total, dtype=np.float64).reshape((12, 1))
    temp_displacement = np.dot(B_shape_matrix, temp_displacement)

    temp_vector = PropertyVector(temp_displacement)
    temp_vector.set_name('initial_strain_total')
    element.add_property(temp_vector)


def generate_initial_stress(element: ElementBase):
    # sigma(x) sigma(y) sigma(z) tau(xy) tau(yz) tau(xz)
    elastic_matrix = element.get_property('elastic_matrix').value
    initial_strain_total = element.get_property('initial_strain_total').value

    initial_stress = np.dot(elastic_matrix, initial_strain_total)
    initial_stress = np.array(initial_stress, dtype=np.float64)
    assert initial_stress.shape == (6, 1)

    temp_vector = PropertyVector(initial_stress)
    temp_vector.set_name('initial_stress')
    element.add_property(temp_vector)


def generate_initial_velocity(element: ElementBase):

    initial_velocity = np.zeros((12, 1), dtype=np.float64)
    # temp_velocity = np.array(self.joint_velocity_list, dtype=np.float64).reshape(12, 1)
    # self.__initial_velocity = self.__initial_velocity + temp_velocity

    assert initial_velocity.shape == (12, 1)

    temp_vector = PropertyVector(initial_velocity)
    temp_vector.set_name('initial_velocity')
    element.add_property(temp_vector)


def generate_initial_matrix(element: ElementBase):
    point_coordinate = element.get_property('point_coordinate').value
    B_shape_matrix: np.matrix = element.get_property('B_shape_matrix').value
    initial_stress = element.get_property('initial_stress').value

    initial_matrix = np.zeros((12, 1), dtype=np.float64)
    temp_S, temp_xS, temp_yS, temp_zS = once_integration(np.array(point_coordinate))
    temp_initial_matrix = temp_S * np.dot(B_shape_matrix.T, initial_stress)
    initial_matrix = initial_matrix - temp_initial_matrix
    assert initial_matrix.shape == (12, 1)

    temp_matrix = PropertyMatrix(initial_matrix)
    temp_matrix.set_name('initial_matrix')
    element.add_property(temp_matrix)


def generate_loading_matrix(element: ElementBase):
    loading_matrix = np.zeros((12, 1), dtype=np.float64)
    loading_point_coordinate = element.get_property('loading_point_list').value
    loading_point_force = element.get_property('loading_point_force').value
    delta_matrix = element.get_property('delta_matrix').value

    for each_loading_point_coordinate, each_loading_point_force in zip(loading_point_coordinate, loading_point_force):
        temp = generate_T_shape_matrix(1, each_loading_point_coordinate[0], each_loading_point_coordinate[1], each_loading_point_coordinate[2], delta_matrix=delta_matrix).T
        loading_matrix = loading_matrix + np.dot(temp, np.array(each_loading_point_force)).reshape(12, 1)

    assert loading_matrix.shape == (12, 1)

    temp_matrix = PropertyMatrix(loading_matrix)
    temp_matrix.set_name('loading_matrix')
    element.add_property(temp_matrix)


def generate_body_matrix(element: ElementBase):
    point_coordinate = element.get_property('point_coordinate').value
    delta_matrix: np.matrix = element.get_property('delta_matrix').value
    body_force = np.array(element.get_property('material_parameter')['body_force'])

    temp_S, temp_xS, temp_yS, temp_zS = once_integration(np.array(point_coordinate, dtype=np.float64))
    temp = generate_T_shape_matrix(temp_S, temp_xS, temp_yS, temp_zS, delta_matrix=delta_matrix)

    temp_body_matrix = np.dot(temp.T, body_force)
    body_matrix = temp_body_matrix.reshape(12, 1)
    assert body_matrix.shape == (12, 1)

    temp_matrix = PropertyMatrix(body_matrix)
    temp_matrix.set_name('body_matrix')
    element.add_property(temp_matrix)


def generate_mass_matrix(element: ElementBase, time_increment: float):

    mass_matrix = np.zeros((12, 12), dtype=np.float64)
    mass_force = np.zeros((12, 1), dtype=np.float64)
    point_coordinate = element.get_property('point_coordinate').value
    delta_matrix: np.matrix = element.get_property('delta_matrix').value
    unit_mass = element.get_property('material_parameter')['unit_mass']
    initial_velocity = np.array(element.get_property('initial_velocity').value)

    temp_S, temp_xS, temp_yS, temp_zS = once_integration(np.array(point_coordinate, dtype=np.float64))
    temp_xxS, temp_yyS, temp_zzS, temp_xyS, temp_xzS, temp_yzS = twice_integration(np.array(point_coordinate, dtype=np.float64))

    ff = np.array(delta_matrix)
    temp_matrix = np.zeros((12, 12), dtype=np.float64)

    for r in range(4):
        for s in range(4):
            temp = ff[r][0] * ff[s][0] * temp_S + \
                   (ff[r][0] * ff[s][1] + ff[r][1] * ff[s][0]) * temp_xS + \
                   (ff[r][0] * ff[s][2] + ff[r][2] * ff[s][0]) * temp_yS + \
                   (ff[r][0] * ff[s][3] + ff[r][3] * ff[s][0]) * temp_zS + \
                   ff[r][1] * ff[s][1] * temp_xxS + \
                   ff[r][2] * ff[s][2] * temp_yyS + \
                   ff[r][3] * ff[s][3] * temp_zzS + \
                   (ff[r][1] * ff[s][2] + ff[r][2] * ff[s][1]) * temp_xyS + \
                   (ff[r][1] * ff[s][3] + ff[r][3] * ff[s][1]) * temp_xzS + \
                   (ff[r][2] * ff[s][3] + ff[r][3] * ff[s][2]) * temp_yzS
            temp_matrix[3 * r][3 * s] = temp
            temp_matrix[3 * r + 1][3 * s + 1] = temp
            temp_matrix[3 * r + 2][3 * s + 2] = temp
    assert temp_matrix.shape == (12, 12)

    temp_mass_matrix = temp_matrix
    temp_mass_matrix = temp_mass_matrix * (2 * unit_mass / time_increment ** 2)
    mass_matrix = mass_matrix + temp_mass_matrix
    assert mass_matrix.shape == (12, 12)

    temp_mass_force = np.dot(temp_matrix, initial_velocity)
    temp_mass_force = temp_mass_force * (2 * unit_mass / time_increment)
    mass_force = mass_force + temp_mass_force.reshape(12, 1)
    assert mass_force.shape == (12, 1)

    temp_matrix = PropertyMatrix(mass_matrix)
    temp_matrix.set_name('mass_matrix')
    element.add_property(temp_matrix)

    temp_matrix = PropertyMatrix(mass_force)
    temp_matrix.set_name('mass_force')
    element.add_property(temp_matrix)

