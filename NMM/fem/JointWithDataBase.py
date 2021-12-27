import sqlite3
import matplotlib.pyplot as plt
import numpy as np

from NMM.fem.ElementBase import Element
from shapely.geometry import Point, Polygon


def get_one_joint(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT ID, xValue, yValue, vdis, udis FROM JointPoints ' \
                         'WHERE ID = {id_value}'.format(id_value=id_value)
    result = cursor.execute(database_statement)
    result = result.fetchall()[0]
    return result


def write_joint_displacement_into_database(element: Element, cursor: sqlite3.Cursor):
    element_joint_number = len(element.joint_id)
    element_id = element.id
    assert len(element.joint_displacement_increment) == element_joint_number
    for each_index in range(element_joint_number):
        joint_id = element.joint_id[each_index]
        joint_displacement_increment = element.joint_displacement_increment[each_index]
        # TODO: get element joint
        database_statement = 'UPDATE JointPoints SET uDis = uDis + {uDis}, vDis = vDis + {vDis} WHERE ID = {ID}'\
            .format(uDis=joint_displacement_increment[0], vDis=joint_displacement_increment[1], ID=joint_id)
        try:
            cursor.execute(database_statement)
        except sqlite3.OperationalError:
            element.draw_edge()
            element.draw_patch()
            plt.show()
        cursor.connection.commit()
