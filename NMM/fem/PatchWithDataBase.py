import sqlite3
import matplotlib.pyplot as plt


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
