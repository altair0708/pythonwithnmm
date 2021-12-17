import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from PointBase import EPoint
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


class Element(object):
    def __init__(self, id_value: int):
        # assembly
        self.id = id_value
        self.material_id = 0
        self.joint_list = []
        self.patch_list = []
        self.joint_array = None
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

        # template variable
        self.__B_shape_matrix = None
        self.__delta_matrix = None
        self.__triangle_list = None

        # constant variable
        self.__loading_point = EPoint('loading')
        self.__fixed_point = EPoint('fixed')
        self.__body_force = None
        self.__time_step = None
        self.__constant_spring = None
        self.__unit_mass = None

        # refresh every time step
        self.__initial_stress = None
        self.__initial_velocity = None

        # calculate matrix
        self.__stiff_matrix = None
        self.__initial_matrix = None
        self.__loading_matrix = None
        self.__body_matrix = None
        self.__mass_matrix = None
        self.__mass_force = None
        self.__fixed_matrix = None

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
            temp_E = self.material_dict['elastic_modulus']
            temp_mu = self.material_dict['possion_ratio']
            elastic_matrix = temp_E / (1 - temp_mu ** 2) * np.matrix([[1, temp_mu, 0],
                                                                      [temp_mu, 1, 0],
                                                                      [0, 0, (1 - temp_mu) / 2]])
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_stiff_matrix = temp_S * self.B_shape_matrix.T
                temp_stiff_matrix = np.dot(temp_stiff_matrix, elastic_matrix)
                temp_stiff_matrix = np.dot(temp_stiff_matrix, self.B_shape_matrix)
                self.__stiff_matrix = self.__stiff_matrix + temp_stiff_matrix
        return self.__stiff_matrix

    @property
    def initial_matrix(self):
        if self.__initial_matrix is None:
            self.__initial_matrix = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_initial_matrix = temp_S * np.dot(self.B_shape_matrix.T, self.initial_stress.T)
                self.__initial_matrix = self.__initial_matrix - temp_initial_matrix
        return self.__initial_matrix

    @property
    def loading_matrix(self):
        if self.__loading_matrix is None:
            self.__loading_matrix = np.zeros((6, 1))
            if self.__loading_point is not None:
                temp = self.T_shape_matrix(coord=self.loading_point.coord, delta_matrix=self.delta_matrix).T
                self.__loading_matrix = np.dot(temp, self.loading_point.force)
        return self.__loading_matrix

    @property
    def body_matrix(self):
        if self.__body_matrix is None:
            self.__body_matrix = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp = self.T_shape_matrix(coord=np.array([[temp_xS, temp_yS]]), delta_matrix=self.delta_matrix)
                temp_body_matrix = np.dot(temp.T, self.body_force)
                self.__body_matrix = self.body_matrix + temp_body_matrix
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
                self.__mass_force = self.__mass_force + temp_mass_force

        return self.__mass_matrix, self.__mass_force

    @property
    def fixed_matrix(self):
        if self.__fixed_matrix is None:
            self.__fixed_matrix = np.zeros((6, 6))
            temp_T_matrix = self.T_shape_matrix(coord=self.__fixed_point.coord, delta_matrix=self.delta_matrix)
            self.__fixed_matrix = np.dot(temp_T_matrix.T, temp_T_matrix)
            self.__fixed_matrix = self.constant_spring * self.__fixed_matrix
        if self.__fixed_matrix.shape != (6, 6):
            raise Exception('fixed matrix shape error')
        return self.__fixed_matrix

    # temp_matrix
    @property
    def delta_matrix(self):
        if self.__delta_matrix is None:
            delta_matrix = np.c_[np.ones((3, 1)), np.array(self.patch_list)]
            delta_matrix = np.matrix(delta_matrix)
            delta_matrix = delta_matrix.I
            self.__delta_matrix = delta_matrix.T
        return self.__delta_matrix

    @property
    def B_shape_matrix(self):
        if self.__B_shape_matrix is None:
            delta_matrix = self.delta_matrix
            self.__B_shape_matrix = np.array([[delta_matrix[0, 1],                  0, delta_matrix[1, 1],                  0, delta_matrix[2, 1],                 0],
                                              [                 0, delta_matrix[0, 2],                  0, delta_matrix[1, 2],                  0, delta_matrix[2, 2]],
                                              [delta_matrix[0, 2], delta_matrix[0, 1], delta_matrix[1, 2], delta_matrix[1, 1], delta_matrix[2, 2], delta_matrix[2, 1]]])
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
    def triangle_list(self):
        if self.__triangle_list is None:
            triangle_delaunay = Delaunay(self.joint_array)
            self.__triangle_list = self.joint_array[triangle_delaunay.simplices]
        return self.__triangle_list

    # TODO: get initial stress from database,
    #  database generate at the end of first step,
    #  then refresh at each end of step
    @property
    def initial_stress(self):
        if self.__initial_stress is None:
            self.__initial_stress = np.array(self.material_dict['initial_force'])
        return self.__initial_stress

    # TODO: Get loading point from database
    @property
    def loading_point(self):
        return self.__loading_point

    @loading_point.setter
    def loading_point(self, point: EPoint):
        self.__loading_point = point

    # TODO: Get fixed point from database
    @property
    def fixed_point(self):
        return self.__fixed_point

    @fixed_point.setter
    def fixed_point(self, point: EPoint):
        self.__fixed_point = point

    @property
    def body_force(self):
        if self.__body_force is None:
            self.__body_force = self.material_dict['body_force']
            self.__body_force = np.array([self.__body_force])
            self.__body_force = self.__body_force.T
            if self.__body_force.shape != (2, 1):
                raise Exception('body force shape error')
        return self.__body_force

    # TODO: Initial velocity
    @property
    def initial_velocity(self):
        if self.__initial_velocity is None:
            self.__initial_velocity = np.zeros((6, 1))
            if self.__initial_velocity.shape != (6, 1):
                raise Exception('initial velocity shape error')
        return self.__initial_velocity

    @property
    def unit_mass(self):
        if self.__unit_mass is None:
            self.__unit_mass = self.material_dict['unit_mass']
        return self.__unit_mass

    # TODO: Get time step form global variable
    @property
    def time_step(self):
        if self.__time_step is None:
            self.__time_step = CONST.TIME_INCREMENT
        return self.__time_step

    # TODO: Get constant spring stiff form global variable
    @property
    def constant_spring(self):
        if self.__constant_spring is None:
            self.__constant_spring = CONST.CONSTANT_SPRING_STIFF
        return self.__constant_spring
