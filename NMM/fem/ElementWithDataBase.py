import sqlite3
from typing import List
from NMM.fem.PointBase import EPoint
from NMM.fem.ElementBase import Element


def get_element_number(cursor: sqlite3.Cursor) -> int:
    database_statement = 'SELECT MAX(elementID) FROM ElementJoints'

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result[0][0]


def get_element_joint_number(id_value: int, cursor: sqlite3.Cursor) -> int:
    database_statement = 'SELECT MAX(jointOrder) FROM ElementJoints ' \
                         'WHERE elementID = {id_value}'.format(id_value=id_value)

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result[0][0]


def get_one_element_joint(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT jointID, xValue, yValue FROM ElementJoints AS EJ ' \
                         'INNER JOIN JointPoints AS JP ON EJ.jointID = JP.ID ' \
                         'WHERE elementID = {id_value}'.format(id_value=id_value)

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result


def get_one_element_patch(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT patchID, xValue, yValue FROM ElementPatches AS EP ' \
                         'INNER JOIN PhysicalPatches AS PP ON EP.patchID = PP.ID ' \
                         'WHERE elementID = {id_value}'.format(id_value=id_value)

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result


def get_one_element_material(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT materialID FROM ElementJoints ' \
                         'WHERE jointOrder = 1 AND jointID = {id_value}'.format(id_value=id_value)

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result


def get_one_special_point(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT * FROM SpecialPoints ' \
                         'WHERE elementID = {id_value}'.format(id_value=id_value)
    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result


def write_special_point_displacement_into_database(element: Element, cursor: sqlite3.Cursor):

    def write_one_type(temp_point_list: List[EPoint], temp_cursor:sqlite3.Cursor):
        for each_point in temp_point_list:
            database_statement = 'UPDATE SpecialPoints SET uDis = uDis + {uDis}, vDis = vDis + {vDis} WHERE ID = {ID}'\
                .format(uDis=each_point.displacement_increment[0][0], vDis=each_point.displacement_increment[0][1], ID=each_point.id)
            temp_cursor.execute(database_statement)
            temp_cursor.connection.commit()
    write_one_type(element.fixed_point_list, cursor)
    write_one_type(element.loading_point_list, cursor)
    write_one_type(element.measured_point_list, cursor)


