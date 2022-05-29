import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from typing import Tuple, List
from NMM.GlobalVariable import CONST
from NMM.fem.PointBase import EPoint, PointType


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
            'unit_mass': 0.0,
            'body_force': (0, 0),
            'elastic_modulus': 200000000000,
            'possion_ratio': 0.28,
            'initial_force': (0, 0, 0),
            'yield_coefficient': {
                'friction_angle': 0,
                'cohesion': 0,
                'tensile_strength': 0
            },
            'initial_velocity': (0, 0, 0)
        }

        self.joint_list = []
        self.joint_id = []
        self.patch_list = []
        self.patch_id = []
        self.__loading_point_list: List[EPoint] = []
        self.__fixed_point_list: List[EPoint] = []
        self.__measured_point_list: List[EPoint] = []

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
        self.__initial_stress = None
        self.__initial_strain_increment = None
        self.__initial_strain_total = np.zeros((3, 1))
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
        self.__fixed_force = None

        # total stiff matrix
        self.__total_matrix = None
        self.__total_force = None

        # something generated to deal with calculate error
        self.__minified_joint_list = []

    def clean_all(self):
        # refresh at the end of time step
        self.patch_displacement = []
        self.__joint_displacement_increment = []
        self.__minified_joint_list = []
        self.__initial_stress = None
        self.__initial_strain_increment = None
        self.__initial_velocity = None
        for each_point in self.fixed_point_list:
            each_point.clean()
        for each_point in self.measured_point_list:
            each_point.clean()
        for each_point in self.loading_point_list:
            each_point.clean()

        # refresh at the start of time step
        self.__stiff_matrix = None
        self.__initial_matrix = None
        self.__loading_matrix = None
        self.__body_matrix = None
        self.__mass_matrix = None
        self.__mass_force = None
        self.__fixed_matrix = None
        self.__fixed_force = None

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
            self.__stiff_matrix = np.zeros((6, 6), dtype=np.float64)
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
            self.__initial_matrix = np.zeros((6, 1), dtype=np.float64)
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_initial_matrix = temp_S * np.dot(self.B_shape_matrix.T, self.initial_stress)
                self.__initial_matrix = self.__initial_matrix - temp_initial_matrix
            check_shape(self.__initial_matrix, (6, 1))
        return self.__initial_matrix

    @property
    def loading_matrix(self):
        if self.__loading_matrix is None:
            self.__loading_matrix = np.zeros((6, 1), dtype=np.float64)
            for loading_point in self.loading_point_list:
                temp = self.T_shape_matrix(1, loading_point.coord[0][0], loading_point[0][1], delta_matrix=self.delta_matrix).T
                self.__loading_matrix = self.__loading_matrix + np.dot(temp, loading_point.force).reshape(6, 1)
            check_shape(self.__loading_matrix, (6, 1))
        return self.__loading_matrix

    @property
    def body_matrix(self):
        if self.__body_matrix is None:
            self.__body_matrix = np.zeros((6, 1), dtype=np.float64)
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp = self.T_shape_matrix(temp_S, temp_xS, temp_yS, delta_matrix=self.delta_matrix)
                temp_body_matrix = np.dot(temp.T, self.body_force)
                self.__body_matrix = self.body_matrix + temp_body_matrix.reshape(6, 1)
            check_shape(self.__body_matrix, (6, 1))
        return self.__body_matrix

    @property
    def mass_matrix(self):
        if self.__mass_matrix is None:
            self.__mass_matrix = np.zeros((6, 6), dtype=np.float64)
            self.__mass_force = np.zeros((6, 1), dtype=np.float64)
            for each_triangle in self.triangle_list:
                temp_S, temp_xS, temp_yS = calculate_integration(each_triangle)
                temp_xxS, temp_yyS, temp_xyS = calculate_twice_integration(each_triangle)
                ff = np.array(self.delta_matrix)
                temp_matrix = np.zeros((6, 6), dtype=np.float64)
                for r in range(3):
                    for s in range(3):
                        temp = ff[r][0] * ff[s][0] * temp_S + (ff[r][0] * ff[s][1] + ff[r][1] * ff[s][0]) * temp_xS +\
                               (ff[r][0] * ff[s][2] + ff[r][2] * ff[s][0]) * temp_yS + ff[r][1] * ff[s][1] * temp_xxS + \
                               (ff[r][1] * ff[s][2] + ff[r][2] * ff[s][1]) * temp_xyS + ff[r][2] * ff[s][2] * temp_yyS
                        temp_matrix[2 * r][2 * s] = temp
                        temp_matrix[2 * r + 1][2 * s + 1] = temp
                check_shape(temp_matrix, (6, 6))
                temp_mass_matrix = temp_matrix
                temp_mass_force = np.dot(temp_matrix, self.initial_velocity)
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
            self.__fixed_matrix = np.zeros((6, 6), dtype=np.float64)
            self.__fixed_force = np.zeros((6, 1), dtype=np.float64)
            for fixed_point in self.fixed_point_list:
                temp = self.T_shape_matrix(1, fixed_point.coord[0][0], fixed_point.coord[0][1], delta_matrix=self.delta_matrix)
                '''fixed test'''
                # temp_zero = np.array([[0, 0, 0, 0, 0, 0]])
                # temp[[0], :] = temp_zero
                '''fixed test'''
                temp_matrix = np.dot(temp.T, temp)
                temp_matrix = self.constant_spring * temp_matrix
                temp_force = np.dot(temp.T, fixed_point.displacement_total.reshape((2, 1)))
                temp_force = self.constant_spring * temp_force
                self.__fixed_matrix = self.__fixed_matrix + temp_matrix
                self.__fixed_force = self.__fixed_force - temp_force
        check_shape(self.__fixed_matrix, (6, 6))
        check_shape(self.__fixed_force, (6, 1))
        return self.__fixed_matrix, self.__fixed_force

    @property
    def total_matrix(self):
        if self.__total_matrix is None:
            self.__total_matrix = self.stiff_matrix + self.fixed_matrix[0] + self.mass_matrix[0]
        return self.__total_matrix

    @property
    def total_force(self):
        if self.__total_force is None:
            self.__total_force = self.initial_matrix + self.loading_matrix + self.body_matrix + self.fixed_matrix[1] + self.mass_matrix[1]
            # self.__total_force = self.fixed_matrix[1] + self.loading_matrix + self.body_matrix + self.mass_matrix[1]
        return self.__total_force

    # temp_matrix
    @property
    def delta_matrix(self):
        if self.__delta_matrix is None:
            delta_matrix = np.c_[np.ones((3, 1), dtype=np.float64), np.array(self.patch_list, dtype=np.float64)]
            delta_matrix = np.matrix(delta_matrix)
            delta_matrix = delta_matrix.I
            self.__delta_matrix = delta_matrix.T
            check_shape(self.__delta_matrix, (3, 3))
        return self.__delta_matrix

    @property
    def B_shape_matrix(self):
        if self.__B_shape_matrix is None:
            delta_matrix = self.delta_matrix
            self.__B_shape_matrix = np.array([[delta_matrix[0, 1],                  0, delta_matrix[1, 1],                  0, delta_matrix[2, 1],                  0],
                                              [                 0, delta_matrix[0, 2],                  0, delta_matrix[1, 2],                  0, delta_matrix[2, 2]],
                                              [delta_matrix[0, 2], delta_matrix[0, 1], delta_matrix[1, 2], delta_matrix[1, 1], delta_matrix[2, 2], delta_matrix[2, 1]]])
            check_shape(self.__B_shape_matrix, (3, 6))
        return self.__B_shape_matrix

    @staticmethod
    def T_shape_matrix(S: float, xS: float, yS: float, delta_matrix: np.ndarray):
        def weight_matrix(s, xs, ys):
            return np.dot(delta_matrix, np.array([[s], [xs], [ys]], dtype=np.float64))
        check_shape(weight_matrix(1, 1, 1), (3, 1))
        We1 = np.array(weight_matrix(S, xS, yS))[0][0]
        We2 = np.array(weight_matrix(S, xS, yS))[1][0]
        We3 = np.array(weight_matrix(S, xS, yS))[2][0]
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
                                                                      [0, 0, (1 - temp_mu) / 2]], dtype=np.float64)
            self.__elastic_matrix = elastic_matrix
        return self.__elastic_matrix

    @property
    def triangle_list(self):
        if self.__triangle_array is None:
            triangle_delaunay = Delaunay(np.array(self.joint_list, dtype=np.float64))
            self.__triangle_array = np.array(self.joint_list, dtype=np.float64)[triangle_delaunay.simplices]
        return self.__triangle_array

    @property
    def initial_strain_total(self):
        if self.__initial_strain_increment is None:
            temp_displacement = np.array(self.patch_displacement, dtype=np.float64).reshape((6, 1))
            temp_displacement = np.dot(self.B_shape_matrix, temp_displacement)
            self.__initial_strain_increment = temp_displacement
            self.__initial_strain_total = self.__initial_strain_total + self.__initial_strain_increment
        return self.__initial_strain_total

    @property
    def initial_stress(self):
        if self.__initial_stress is None:
            self.__initial_stress = np.dot(self.elastic_matrix, self.initial_strain_total)
            self.__initial_stress = np.array(self.__initial_stress, dtype=np.float64)
            check_shape(self.__initial_stress, (3, 1))
        return self.__initial_stress

    # TODO: Initial velocity
    @property
    def initial_velocity(self):
        if self.__initial_velocity is None:
            self.__initial_velocity = np.zeros((6, 1), dtype=np.float64)
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
            self.__body_force = np.array([self.__body_force], dtype=np.float64)
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
            self.__constant_spring = CONST.CONSTANT_SPRING_STIFF * 100
        return self.__constant_spring

    # displacement interpolation
    @property
    def joint_displacement_increment(self):
        if len(self.__joint_displacement_increment) == 0:
            temp_patch_displacement = np.array(self.patch_displacement, dtype=np.float64).reshape((6, 1))
            for each_joint in self.joint_list:
                temp_coord = np.array(each_joint).reshape((1, 2))
                temp_displacement_increment = Element.displacement_interpolation(temp_coord, temp_patch_displacement, self.delta_matrix)
                self.__joint_displacement_increment.append(temp_displacement_increment[0])

            # temp_patch_displacement = np.array(self.patch_displacement, dtype=np.float64)
            # temp_patch_coordinate = np.array(self.patch_list, dtype=np.float64)
            # temp_joint_coordinate = np.array(self.joint_list, dtype=np.float64)
            # self.__joint_displacement_increment = griddata(temp_patch_coordinate, temp_patch_displacement, temp_joint_coordinate)
            # if np.isnan(self.__joint_displacement_increment).any():
            #     temp_joint_coordinate = np.array(self.minified_joint_list, dtype=np.float64)
            #     self.__joint_displacement_increment = griddata(temp_patch_coordinate, temp_patch_displacement, temp_joint_coordinate)

            # special point interpolation
            for each_point in self.fixed_point_list:
                self.special_points_interpolation(each_point, temp_patch_displacement, self.delta_matrix)
            for each_point in self.loading_point_list:
                self.special_points_interpolation(each_point, temp_patch_displacement, self.delta_matrix)
            for each_point in self.measured_point_list:
                self.special_points_interpolation(each_point, temp_patch_displacement, self.delta_matrix)

        self.__joint_displacement_increment = list(self.__joint_displacement_increment)
        if len(self.__joint_displacement_increment) != len(self.joint_list):
            raise Exception('joint displacement number error!')
        return self.__joint_displacement_increment

    # @property
    # def minified_joint_list(self):
    #     if len(self.__minified_joint_list) == 0:
    #         self.__minified_joint_list = self.minify_polygon(self.joint_list)
    #     return self.__minified_joint_list
    #
    # @staticmethod
    # def minify_polygon(point_list: list, factor: float = 0.999):
    #     temp_polygon = Polygon(point_list)
    #     temp_polygon = scale(temp_polygon, factor, factor, origin='centroid')
    #     temp_x, temp_y = temp_polygon.exterior.xy
    #     temp_x = np.array(temp_x, dtype=np.float64).reshape((-1, 1))
    #     temp_y = np.array(temp_y, dtype=np.float64).reshape((-1, 1))
    #     temp_point_list = np.c_[temp_x, temp_y]
    #     temp_point_list = list(temp_point_list)
    #     temp_point_list.pop()
    #     return temp_point_list

    # special points interpolation
    @staticmethod
    def special_points_interpolation(point: EPoint, patch_displacement: np.ndarray, delta_matrix: np.ndarray):

        temp_coord = point.coord
        temp_point_displacement = Element.displacement_interpolation(temp_coord, patch_displacement, delta_matrix)
        point.displacement_increment = temp_point_displacement

    # @staticmethod
    # def special_points_interpolation(point: EPoint, patch_displacement: list, patch_list: list):
    #     temp_patch_displacement = np.array(patch_displacement, dtype=np.float64)
    #     temp_patch_coordinate = np.array(patch_list, dtype=np.float64)
    #     temp_point_coordinate = point.coord[0]
    #     self.__joint_displacement_increment = griddata(temp_point_coordinate, temp_patch_displacement, temp_joint_coordinate)
    #     point.displacement_increment = temp_point_displacement

    @staticmethod
    def displacement_interpolation(point_coord: np.ndarray, patch_displacement: np.ndarray, delta_matrix: np.ndarray):
        check_shape(point_coord, (1, 2))
        check_shape(patch_displacement, (6, 1))
        check_shape(delta_matrix, (3, 3))
        temp_T = Element.T_shape_matrix(1, point_coord[0][0], point_coord[0][1], delta_matrix)
        temp_displacement = np.dot(temp_T, patch_displacement).reshape((1, 2))
        return temp_displacement
