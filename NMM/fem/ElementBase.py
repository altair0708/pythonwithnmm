import sqlite3
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from ElementWithDataBase import *


class Element(object):
    def __init__(self, id_value: int):
        self.id = id_value
        self.material_id = 0
        self.joint_list = []
        self.patch_list = []
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
        self.joint_array = np.ones((3, 2))
        self.__B_shape_matrix = None
        self.__T_shape_matrix = None
        self.__xs = 0
        self.__ys = 0
        self.__jacobi = np.ones((2, 2))

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

    def shape_function(self):
        pass

    @property
    def stiff_matrix(self):
        temp_E = self.material_dict['elastic_modulus']
        temp_mu = self.material_dict['possion_ratio']
        elastic_matrix = temp_E / (1 - temp_mu ** 2) * np.matrix([[1, temp_mu, 0],
                                                                  [temp_mu, 1, 0],
                                                                  [0, 0, (1 - temp_mu) / 2]])

    @property
    def B_shape_matrix(self):
        if not self.__B_shape_matrix:
            delta_matrix = np.c_[np.ones((3, 1)), np.array(self.patch_list)]
            delta_matrix = np.matrix(delta_matrix)
            delta_matrix = delta_matrix.I
            delta_matrix = delta_matrix.T
            self.__B_shape_matrix = np.array([[delta_matrix[1, 2],                  0, delta_matrix[2, 2],                  0, delta_matrix[3, 2],                 0],
                                              [                 0, delta_matrix[1, 3],                  0, delta_matrix[2, 3],                  0, delta_matrix[3, 3]],
                                              [delta_matrix[1, 3], delta_matrix[1, 2], delta_matrix[2, 3], delta_matrix[2, 2], delta_matrix[3, 3], delta_matrix[3, 2]]])
            return self.__B_shape_matrix
        else:
            return self.__B_shape_matrix

    @property
    def T_shape_matrix(self):
        if not self.__T_shape_matrix:
            self.__xs = (self.joint_array[0, 0] + self.joint_array[0, 0] + self.joint_array[0, 1] + self.joint_array[0, 2]) / 4
            self.__ys = (self.joint_array[1, 0] + self.joint_array[1, 0] + self.joint_array[1, 1] + self.joint_array[1, 2]) / 4
            self.__jacobi = np.array([[self.joint_array[0, 2] - self.joint_array[0, 1], self.joint_array[1, 2] - self.joint_array[1, 1]],
                                      [self.joint_array[0, 0] * 2 - self.joint_array[0, 2] - self.joint_array[0, 1], self.joint_array[1, 0] * 2 - self.joint_array[1, 2] - self.joint_array[1, 1]]])
            self.__jacobi = 0.25 * self.__jacobi
            return self.__T_shape_matrix
        else:
            return self.__T_shape_matrix


class EPoint(object):
    pass


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

