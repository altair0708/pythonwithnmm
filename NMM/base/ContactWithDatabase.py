import sqlite3
from shapely.geometry import Polygon, box
from NMM.base.DataBase import query_by_column


def get_one_loop(id_value: int, cursor: sqlite3.Cursor = None):
    database_statement = 'SELECT xValue, yValue FROM ContactLoops AS CL ' \
                         'INNER JOIN JointPoints AS JP ON CL.jointID=JP.ID ' \
                         'WHERE loopID={id_value}'.format(id_value=id_value)

    loop = cursor.execute(database_statement)
    loop = loop.fetchall()
    return loop


def get_loop_bounds(loop_list: list):
    loop_polygon = Polygon(loop_list)
    return loop_polygon


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    database_name = '../../data/test.db'
    database_connect = sqlite3.connect(database_name)
    database_cursor = database_connect.cursor()
    for temp_i in range(1, 5):
        loop_temp = get_one_loop(temp_i, database_cursor)
        loop_polygon_temp = get_loop_bounds(loop_temp)
        x, y = loop_polygon_temp.exterior.xy
        a = loop_polygon_temp.bounds
        print(type(a))
        bounds_temp = box(*a)
        x1, y1 = bounds_temp.exterior.xy
    plt.show()
