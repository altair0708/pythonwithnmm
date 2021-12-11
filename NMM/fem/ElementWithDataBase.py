import sqlite3


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
    database_statement = 'SELECT xValue, yValue FROM ElementJoints AS EJ ' \
                         'INNER JOIN JointPoints AS JP ON EJ.jointID = JP.ID ' \
                         'WHERE elementID = {id_value}'.format(id_value=id_value)

    result = cursor.execute(database_statement)
    result = result.fetchall()
    return result


def get_one_element_patch(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT xValue, yValue FROM ElementPatches AS EP ' \
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
