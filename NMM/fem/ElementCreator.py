import numpy as np
import json
from ElementWithDataBase import *
from ElementBase import Element
from PointBase import EPoint, PointType


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


class ElementCreator(object):
    def __init__(self, cursor: sqlite3.Cursor):
        self.__database_cursor = cursor
        self.__element_number = get_element_number(self.__database_cursor)
        self.__element_list = []

    def create_an_element(self, id_value: int) -> Element:
        element = Element(id_value)
        element.material_id = get_one_element_material(id_value=id_value, cursor=self.__database_cursor)
        with open('../data/material_coefficient.json') as material_coefficient:
            element.material_dict = json.load(material_coefficient)
        return element

    def assembly_joint_point(self, element):
        joint_list = get_one_element_joint(id_value=element.id, cursor=self.__database_cursor)
        for each_joint in joint_list:
            element.joint_list.append(each_joint)
        element.joint_array = np.array(element.joint_list)

    def assembly_patch(self, element):
        patch_list = get_one_element_patch(id_value=element.id, cursor=self.__database_cursor)
        for each_patch in patch_list:
            element.patch_id.append(each_patch[0])
            element.patch_list.append(each_patch[1:3])

    def assembly_special_point(self, element):
        special_point_list = get_one_special_point(id_value=element.id, cursor=self.__database_cursor)
        if len(special_point_list) != 0:
            for each_point in special_point_list:
                temp_point = EPoint(PointType(each_point[4]))
                temp_point.element_id = element.id
                temp_point.coord = np.array([each_point[1:3]])
                if temp_point.point_type == PointType.fixed_point:
                    element.fixed_point_list.append(temp_point)
                elif temp_point.point_type == PointType.loading_point:
                    element.loading_point_list.append(temp_point)
                elif temp_point.point_type == PointType.measured_point:
                    element.measured_point_list.append(temp_point)
                else:
                    raise Exception('point type error:{point_type}'.format(point_type=temp_point.point_type))

    def run(self):
        print('element number is {}'.format(self.__element_number))
        for each_id in range(1, self.__element_number + 1):
            temp_element = self.create_an_element(each_id)
            self.assembly_patch(temp_element)
            self.assembly_special_point(temp_element)
            self.assembly_joint_point(temp_element)
            self.__element_list.append(temp_element)
        return self.__element_list
