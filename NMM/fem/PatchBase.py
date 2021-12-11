import sqlite3
import matplotlib.pyplot as plt


def get_patch_number(cursor: sqlite3.Cursor) -> int:
    database_statement = 'SELECT MAX(ID) FROM PhysicalPatches'
    result = cursor.execute(database_statement)
    result = result.fetchall()[0][0]
    return result


def get_one_patch(id_value: int, cursor: sqlite3.Cursor):
    database_statement = 'SELECT ID, xValue, yValue FROM PhysicalPatches ' \
                         'WHERE ID = {id_value}'.format(id_value=id_value)
    result = cursor.execute(database_statement)
    result = result.fetchall()[0]
    return result


if __name__ == '__main__':
    database_name = '../../data/test.db'
    database_connect = sqlite3.connect(database_name)
    database_cursor = database_connect.cursor()

    patch_number = get_patch_number(database_cursor)

    for each_id in range(1, patch_number + 1):
        id, x, y = get_one_patch(each_id, database_cursor)
        plt.scatter(x, y)

    plt.show()

    database_connect.close()