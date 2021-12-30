import numpy as np
import sqlite3
from typing import List
from NMM.fem.ElementBase import Element
from NMM.fem.PatchWithDataBase import write_patch_displacement_into_database, get_one_patch
from NMM.fem.JointWithDataBase import get_one_joint, write_joint_displacement_into_database
from NMM.fem.ElementWithDataBase import write_special_point_displacement_into_database


class ElementRefresher:
    @staticmethod
    def refresh_patch_displacement(patch_displacement: np.ndarray, element_list: List[Element], cursor: sqlite3.Cursor):
        write_patch_displacement_into_database(patch_displacement, cursor)
        for each_element in element_list:
            ElementRefresher.assembly_patch_displacement(each_element, cursor)

    @staticmethod
    def assembly_patch_displacement(element: Element, database_cursor: sqlite3.Cursor):
        for each_id in element.patch_id:
            id_value, x, y, u, v = get_one_patch(each_id, database_cursor)
            element.patch_displacement.append([u, v])

    @staticmethod
    def refresh_joint_displacement(element_list: List[Element], cursor: sqlite3.Cursor):
        for each_element in element_list:
            write_joint_displacement_into_database(each_element, cursor)
        ElementRefresher.refresh_special_point_displacement(element_list, cursor)

    @staticmethod
    def refresh_special_point_displacement(element_list: List[Element], cursor: sqlite3.Cursor):
        for each_element in element_list:
            write_special_point_displacement_into_database(each_element, cursor)
