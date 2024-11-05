import sqlite3
from NMM.fem.ElementBase import Element


def get_one_joint(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT ID, xValue, yValue, xdis, ydis FROM JointPoints ' \
                         'WHERE ID = {id_value}'.format(id_value=id_value)
    result = cursor.execute(database_statement)
    result = result.fetchall()[0]
    return result


def write_joint_displacement_into_database(element: Element, cursor: sqlite3.Cursor):
    element_joint_number = len(element.joint_id)
    assert len(element.joint_displacement_increment) == element_joint_number
    for each_index in range(element_joint_number):
        joint_id = element.joint_id[each_index]
        joint_displacement_increment = element.joint_displacement_increment[each_index]
        database_statement = 'UPDATE JointPoints SET xDis = xDis + {xDis}, yDis = yDis + {yDis} WHERE ID = {ID}'\
            .format(xDis=joint_displacement_increment[0], yDis=joint_displacement_increment[1], ID=joint_id)
        cursor.execute(database_statement)
        cursor.connection.commit()
