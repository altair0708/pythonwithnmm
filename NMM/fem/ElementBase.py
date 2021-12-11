import sqlite3
import json
import numpy as np
import matplotlib.pyplot as plt
from ElementWithDataBase import *


class Element(object):
    def __init__(self, id_value: int):
        self.id = id_value
        self.material_id = 0
        self.joint_list = []
        self.patch_list = []
        self.material_dict = {}
        self.joint_array = None

    def draw_edge(self):
        temp_list = self.joint_list.copy()
        temp_list.append(self.joint_list[0])
        temp_array = np.array(temp_list)
        plt.plot(temp_array[:, 0], temp_array[:, 1])

    def draw_patch(self):
        temp_list = self.patch_list.copy()
        temp_list.append(self.patch_list[0])
        temp_array = np.array(temp_list)
        plt.plot(temp_array[:, 0], temp_array[:, 1])


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

