import sqlite3
import numpy as np
import json
from ElementWithDataBase import *
from ElementBase import Element


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
