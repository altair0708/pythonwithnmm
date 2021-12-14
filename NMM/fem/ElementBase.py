import sqlite3
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from ElementWithDataBase import *
from shapely.geometry import Polygon


class EPoint(object):
    def __init__(self):
        self.__element_id = 0
        self.__coord = np.zeros((1, 2))
        self.__force = np.zeros((2, 1))

    @property
    def element_id(self):
        return self.__element_id

    @property
    def coord(self):
        return self.__coord

    @property
    def force(self):
        return self.__force


class Element(object):
    def __init__(self, id_value: int):
        # assembly
        self.id = id_value
        self.material_id = 0
        self.joint_list = []
        self.patch_list = []
        self.__loading_point = EPoint()
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
        self.joint_array = np.zeros((3, 2))
        self.__B_shape_matrix = None
        self.__T_shape_matrix = None
        self.__xs = 0
        self.__ys = 0
        self.__jacobi = np.zeros((2, 2))
        self.__delta_matrix = None
        self.__triangle_list = None
        self.__initial_stress = None

        # calculate matrix
        self.__stiff_matrix = None
        self.__initial_matrix = None
        self.__loading_matrix = None

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
                temp_polygon = Polygon(each_triangle)
                plt.triplot(*temp_polygon.exterior.xy)
                temp_stiff_matrix = temp_polygon.area * self.B_shape_matrix.T
                temp_stiff_matrix = np.dot(temp_stiff_matrix, elastic_matrix)
                temp_stiff_matrix = np.dot(temp_stiff_matrix, self.B_shape_matrix)
                self.__stiff_matrix = self.__stiff_matrix + temp_stiff_matrix
        return self.__stiff_matrix

    @property
    def initial_matrix(self):
        if self.__initial_matrix is None:
            self.__initial_matrix = np.zeros((6, 1))
            for each_triangle in self.triangle_list:
                temp_polygon = Polygon(each_triangle)
                temp_initial_matrix = temp_polygon.area * np.dot(self.B_shape_matrix.T, self.initial_stress.T)
                self.__initial_matrix = self.__initial_matrix - temp_initial_matrix
        return self.__initial_matrix

    @property
    def loading_matrix(self):
        if self.__loading_matrix is None:
            self.__loading_matrix = np.zeros((6, 1))
            if self.__loading_point is not None:
                temp = self.T_shape_matrix(coord=self.loading_point.coord, delta_matrix=self.delta_matrix).T
                self.__loading_matrix = np.dot(temp, self.loading_point.force)
                print(temp)
        return self.__loading_matrix

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

    @property
    def loading_point(self):
        return self.__loading_point

    @loading_point.setter
    def loading_point(self, point: EPoint):
        self.__loading_point = point


class EPatch(object):
    pass


def create_an_element(id_value: int, cursor: sqlite3.Cursor) -> Element:
    element = Element(id_value)
    element.material_id = get_one_element_material(id_value=id_value, cursor=cursor)

    joint_list = get_one_element_joint(id_value=id_value, cursor=cursor)
    for each_joint in joint_list:
        element.joint_list.append(each_joint)
    element.joint_array = np.array(element.joint_list)

    patch_list = get_one_element_patch(id_value=id_value, cursor=cursor)
    for each_patch in patch_list:
        element.patch_list.append(each_patch)

    with open('../data/material_coefficient.json') as material_coefficient:
        element.material_dict = json.load(material_coefficient)

    return element

