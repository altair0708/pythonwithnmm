import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from scipy.interpolate import griddata
from typing import Tuple

from NMM.GlobalVariable import CONST


def calculate_integration(point_list: np.ndarray):
    if point_list.shape != (3, 2):
        raise Exception('please input a 3 rows 2 columns matrix')
    jacobi = np.c_[np.ones((3, 1)), point_list]
    jacobi = np.matrix(jacobi)
    jacobi = np.linalg.det(jacobi)
    S = 0.5 * jacobi
    xS = (1 / 6) * jacobi * (np.sum(point_list[:, 0]))
    yS = (1 / 6) * jacobi * (np.sum(point_list[:, 1]))
    return S, xS, yS


def calculate_twice_integration(point_list: np.ndarray):
    if point_list.shape != (3, 2):
        raise Exception('please input a 3 rows 2 columns matrix')
    x0 = point_list[0, 0]
    y0 = point_list[0, 1]
    x1 = point_list[1, 0]
    y1 = point_list[1, 1]
    x2 = point_list[2, 0]
    y2 = point_list[2, 1]
    jacobi = np.c_[np.ones((3, 1)), point_list]
    jacobi = np.matrix(jacobi)
    jacobi = np.linalg.det(jacobi)
    xxS = (1 / 12) * jacobi * (x0 * x0 + x0 * x1 + x0 * x2 + x1 * x1 + x1 * x2 + x2 * x2)
    yyS = (1 / 12) * jacobi * (y0 * y0 + y0 * y1 + y0 * y2 + y1 * y1 + y1 * y2 + y2 * y2)
    xyS = (1 / 24) * jacobi * (2 * x0 * y0 + x0 * y1 + x0 * y2 +
                               x1 * y0 + 2 * x1 * y1 + x1 * y2 +
                               x2 * y0 + x2 * y1 + 2 * x2 * y2)

    return xxS, yyS, xyS


def check_shape(array: np.ndarray, shape: Tuple[int, int]):
    if array.shape != shape:
        raise Exception('array shape error')


class Element(object):
    def __init__(self, id_value: int):
        # generate at the start of calculate
        self.id = id_value
        self.material_id = 0
        self.material_dict = {
            'id': 1,
            'unit_mass': 0.05,
            'body_force': (0, -1),
            'elastic_modulus': 5000,
            'possion_ratio': 0.3,
            'initial_force': (0, 0, 0),
            'yield_coefficient': {
                'friction_angle': 0,
                'cohesion': 0,
                'tensile_strength': 0
            },
            'initial_velocity': (0, 0, 0)
        }

        # TODO: something can be modified
        self.joint_list = []
        self.joint_id = []
        self.patch_list = []
        self.patch_id = []
        self.__loading_point_list = []
        self.__fixed_point_list = []
        self.__measured_point_list = []

        # constant variable
        self.__body_force = None
        self.__time_step = None
        self.__constant_spring = None
        self.__unit_mass = None

        # template variable
        self.__B_shape_matrix = None
        self.__delta_matrix = None
        self.__triangle_array = None
        self.__elastic_matrix = None

        # draw a counter
        # refresh at the end of time step
        self.patch_displacement = []
        self.__joint_displacement_increment = []
        self.joint_displacement_total = []
        self.__initial_stress = None
        self.__initial_strain = None
        self.__initial_velocity = None

        # calculate matrix
        # refresh at the start of time step
        self.__stiff_matrix = None
        self.__initial_matrix = None
        self.__loading_matrix = None
        self.__body_matrix = None
        self.__mass_matrix = None
        self.__mass_force = None
        self.__fixed_matrix = None

        # total stiff matrix
        self.__total_matrix = None
        self.__total_force = None

    def draw_edge(self):
        temp_list = self.joint_list.copy()
        temp_list.append(self.joint_list[0])
        temp_array = np.array(temp_list)
        plt.plot(temp_array[:, 0], temp_array[:, 1])
        # triangle = Delaunay(self.joint_array)
        # plt.triplot(self.joint_array[:, 0], self.joint_array[:, 1], triangle.simplices)

    def draw_patch(self):
        temp_list = self.patch_list.copy()
        temp_list.append(self.patch_list[0])
        temp_array = np.array(temp_list)
        plt.plot(temp_array[:, 0], temp_array[:, 1], linestyle="dashed")

    # calculate matrix
    @property
    def stiff_matrix(self):
        if self.__stiff_matrix is None:
            self.__stiff_matrix = np.zeros((6, 6))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_stiff_matrix = temp_S * self.B_shape_matrix.T
                temp_stiff_matrix = np.dot(temp_stiff_matrix, self.elastic_matrix)
                temp_stiff_matrix = np.dot(temp_stiff_matrix, self.B_shape_matrix)
                self.__stiff_matrix = self.__stiff_matrix + temp_stiff_matrix
            check_shape(self.__stiff_matrix, (6, 6))
        return self.__stiff_matrix

    @property
    def initial_matrix(self):
        if self.__initial_matrix is None:
            self.__initial_matrix = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_initial_matrix = temp_S * np.dot(self.B_shape_matrix.T, self.initial_stress)
                self.__initial_matrix = self.__initial_matrix - temp_initial_matrix.reshape(6, 1)
            check_shape(self.__initial_matrix, (6, 1))
        return self.__initial_matrix

    @property
    def loading_matrix(self):
        if self.__loading_matrix is None:
            self.__loading_matrix = np.zeros((6, 1))
            for loading_point in self.loading_point_list:
                temp = self.T_shape_matrix(coord=loading_point.coord, delta_matrix=self.delta_matrix).T
                self.__loading_matrix = self.__loading_matrix + np.dot(temp, loading_point.force).reshape(6, 1)
            check_shape(self.__loading_matrix, (6, 1))
        return self.__loading_matrix

    @property
    def body_matrix(self):
        if self.__body_matrix is None:
            self.__body_matrix = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp = self.T_shape_matrix(coord=np.array([[temp_xS, temp_yS]]), delta_matrix=self.delta_matrix)
                temp_body_matrix = np.dot(temp.T, self.body_force)
                self.__body_matrix = self.body_matrix + temp_body_matrix.reshape(6, 1)
            check_shape(self.__body_matrix, (6, 1))
        return self.__body_matrix

    # TODO: Simplex integral VS Numerical integral
    @property
    def mass_matrix(self):
        if self.__mass_matrix is None:
            self.__mass_matrix = np.zeros((6, 6))
            self.__mass_force = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_T = self.T_shape_matrix(coord=np.array([[temp_xS, temp_yS]]), delta_matrix=self.delta_matrix)
                temp_mass_matrix = np.dot(temp_T.T, temp_T)
                temp_mass_force = np.dot(temp_mass_matrix, self.initial_velocity)
                temp_mass_matrix = temp_mass_matrix * (2 * self.unit_mass / self.time_step ** 2)
                temp_mass_force = temp_mass_force * (2 * self.unit_mass / self.time_step)
                self.__mass_matrix = self.__mass_matrix + temp_mass_matrix
                self.__mass_force = self.__mass_force + temp_mass_force.reshape(6, 1)
            check_shape(self.__mass_matrix, (6, 6))
            check_shape(self.__mass_force, (6, 1))
        return self.__mass_matrix, self.__mass_force

    @property
    def fixed_matrix(self):
        if self.__fixed_matrix is None:
            self.__fixed_matrix = np.zeros((6, 6))
            for fixed_point in self.fixed_point_list:
                temp = self.T_shape_matrix(coord=fixed_point.coord, delta_matrix=self.delta_matrix)
                temp = np.dot(temp.T, temp)
                temp = self.constant_spring * temp
                self.__fixed_matrix = self.__fixed_matrix + temp
        if self.__fixed_matrix.shape != (6, 6):
            raise Exception('fixed matrix shape error')
        return self.__fixed_matrix

    @property
    def total_matrix(self):
        if self.__total_matrix is None:
            self.__total_matrix = self.stiff_matrix + self.mass_matrix[0] + self.fixed_matrix
        return self.__total_matrix

    @property
    def total_force(self):
        if self.__total_force is None:
            self.__total_force = self.initial_matrix + self.loading_matrix + self.body_matrix + self.mass_matrix[1]
        return self.__total_force

    # temp_matrix
    @property
    def delta_matrix(self):
        if self.__delta_matrix is None:
            delta_matrix = np.c_[np.ones((3, 1)), np.array(self.patch_list)]
            delta_matrix = np.matrix(delta_matrix)
            delta_matrix = delta_matrix.I
            self.__delta_matrix = delta_matrix.T
            check_shape(self.__delta_matrix, (3, 3))
        return self.__delta_matrix

    @property
    def B_shape_matrix(self):
        if self.__B_shape_matrix is None:
            delta_matrix = self.delta_matrix
            self.__B_shape_matrix = np.array([[delta_matrix[0, 1],                  0, delta_matrix[1, 1],                  0, delta_matrix[2, 1],                 0],
                                              [                 0, delta_matrix[0, 2],                  0, delta_matrix[1, 2],                  0, delta_matrix[2, 2]],
                                              [delta_matrix[0, 2], delta_matrix[0, 1], delta_matrix[1, 2], delta_matrix[1, 1], delta_matrix[2, 2], delta_matrix[2, 1]]])
            check_shape(self.__B_shape_matrix, (3, 6))
        return self.__B_shape_matrix

    @staticmethod
    def T_shape_matrix(coord: np.ndarray, delta_matrix: np.ndarray):
        We1 = delta_matrix[0, 0] + delta_matrix[0, 1] * coord[0][0] + delta_matrix[0, 2] * coord[0][1]
        We2 = delta_matrix[1, 0] + delta_matrix[1, 1] * coord[0][0] + delta_matrix[1, 2] * coord[0][1]
        We3 = delta_matrix[2, 0] + delta_matrix[2, 1] * coord[0][0] + delta_matrix[2, 2] * coord[0][1]
        T_shape_matrix = np.c_[We1 * np.identity(2), We2 * np.identity(2), We3 * np.identity(2)]
        if T_shape_matrix.shape != (2, 6):
            raise Exception('T matrix shape error')
        return T_shape_matrix

    @property
    def elastic_matrix(self):
        if self.__elastic_matrix is None:
            temp_E = self.material_dict['elastic_modulus']
            temp_mu = self.material_dict['possion_ratio']
            elastic_matrix = temp_E / (1 - temp_mu ** 2) * np.matrix([[1, temp_mu, 0],
                                                                      [temp_mu, 1, 0],
                                                                      [0, 0, (1 - temp_mu) / 2]])
            self.__elastic_matrix = elastic_matrix
        return self.__elastic_matrix

    @property
    def triangle_list(self):
        if self.__triangle_array is None:
            triangle_delaunay = Delaunay(np.array(self.joint_list))
            self.__triangle_array = np.array(self.joint_list)[triangle_delaunay.simplices]
        return self.__triangle_array

    # TODO: get initial stress from database,
    #  database generate at the end of first step,
    #  then refresh at each end of step
    @property
    def initial_strain(self):
        if self.__initial_strain is None:
            temp_displacement = np.array(self.patch_displacement).reshape((6, 1))
            temp_displacement = np.dot(self.B_shape_matrix, temp_displacement)
            self.__initial_strain = temp_displacement
        return self.__initial_strain

    @property
    def initial_stress(self):
        if self.__initial_stress is None:
            self.__initial_stress = np.dot(self.elastic_matrix, self.initial_strain)
        return self.__initial_stress

    # TODO: Initial velocity
    @property
    def initial_velocity(self):
        if self.__initial_velocity is None:
            self.__initial_velocity = np.zeros((6, 1))
            if self.__initial_velocity.shape != (6, 1):
                raise Exception('initial velocity shape error')
        return self.__initial_velocity

    @property
    def loading_point_list(self):
        return self.__loading_point_list

    @property
    def fixed_point_list(self):
        return self.__fixed_point_list

    @property
    def measured_point_list(self):
        return self.__measured_point_list

    @property
    def body_force(self):
        if self.__body_force is None:
            self.__body_force = self.material_dict['body_force']
            self.__body_force = np.array([self.__body_force])
            self.__body_force = self.__body_force.T
            if self.__body_force.shape != (2, 1):
                raise Exception('body force shape error')
        return self.__body_force

    @property
    def unit_mass(self):
        if self.__unit_mass is None:
            self.__unit_mass = self.material_dict['unit_mass']
        return self.__unit_mass

    @property
    def time_step(self):
        if self.__time_step is None:
            self.__time_step = CONST.TIME_INCREMENT
        return self.__time_step

    @property
    def constant_spring(self):
        if self.__constant_spring is None:
            self.__constant_spring = CONST.CONSTANT_SPRING_STIFF
        return self.__constant_spring

    @property
    def joint_displacement_increment(self):
        if len(self.__joint_displacement_increment) == 0:
            temp_patch_displacement = np.array(self.patch_displacement)
            temp_patch_coordinate = np.array(self.patch_list)
            temp_joint_coordinate = np.array(self.joint_list)
            self.__joint_displacement_increment = griddata(temp_patch_coordinate, temp_patch_displacement, temp_joint_coordinate)
        self.__joint_displacement_increment = list(self.__joint_displacement_increment)
        if len(self.__joint_displacement_increment) != len(self.joint_list):
            raise Exception('joint displacement number error!')
        return self.__joint_displacement_increment

    def clean_all(self):
        # refresh at the end of time step
        self.patch_displacement.clear()
        self.__joint_displacement_increment.clear()
        self.joint_displacement_total.clear()
        self.__initial_stress = None
        self.__initial_strain = None
        self.__initial_velocity = None

        # refresh at the start of time step
        self.__stiff_matrix = None
        self.__initial_matrix = None
        self.__loading_matrix = None
        self.__body_matrix = None
        self.__mass_matrix = None
        self.__mass_force = None
        self.__fixed_matrix = None

        # total stiff matrix
        self.__total_matrix = None
        self.__total_force = None
