import sqlite3
import numpy as np


def get_patch_number(cursor: sqlite3.Cursor) -> int:
    database_statement = 'SELECT MAX(ID) FROM PhysicalPatches'
    result = cursor.execute(database_statement)
    result = result.fetchall()[0][0]
    return result


def get_one_patch(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT ID, xValue, yValue, vdis, udis FROM PhysicalPatches ' \
                         'WHERE ID = {id_value}'.format(id_value=id_value)
    result = cursor.execute(database_statement)
    result = result.fetchall()[0]
    return result


def write_patch_displacement_into_database(displacement_array: np.ndarray, database_cursor: sqlite3.Cursor):
    database_statement = 'SELECT MAX(ID) FROM PhysicalPatches;'
    patch_number = database_cursor.execute(database_statement)
    patch_number = patch_number.fetchone()
    displacement_array = displacement_array.reshape((-1, 2))
    if displacement_array.shape[0] != patch_number[0]:
        print(patch_number)
        raise Exception('patch number error: {}'.format(displacement_array.shape))
    for id, point_displacement in enumerate(displacement_array):
        database_statement = 'UPDATE PhysicalPatches SET uDis = {uDis}, vDis = {vDis} ' \
                             'WHERE ID = {ID}'.format(uDis=point_displacement[0], vDis=point_displacement[1], ID=id+1)
        database_cursor.execute(database_statement)
    database_cursor.connection.commit()


