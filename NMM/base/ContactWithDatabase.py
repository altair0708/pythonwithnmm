import sqlite3
from shapely.geometry import LineString, Polygon, box, polygon


def get_one_loop(id_value: int, cursor: sqlite3.Cursor = None):
    """
    get one loop from database index by id
    :param id_value: loop id
    :param cursor: cursor of database
    :return: a polygon object of shapely
    """
    database_statement = 'SELECT xValue, yValue FROM ContactLoops AS CL ' \
                         'INNER JOIN JointPoints AS JP ON CL.jointID=JP.ID ' \
                         'WHERE loopID={id_value}'.format(id_value=id_value)

    loop = cursor.execute(database_statement)
    loop = loop.fetchall()
    loop_polygon = Polygon(loop)
    loop_line = LineString(loop)
    return loop_polygon, loop_line


def get_loop_bounds(loop_polygon: polygon.Polygon, offset: float = 0.1):
    """
    get the bounds rectangle from the given polygon
    :param loop_polygon: given polygon
    :param offset: the offset of rectangle
    :return: a polygon object of shapely
    """
    loop_bounds = loop_polygon.exterior.bounds
    loop_bounds = list(loop_bounds)
    loop_bounds[0] = loop_bounds[0] - offset
    loop_bounds[1] = loop_bounds[1] - offset
    loop_bounds[2] = loop_bounds[2] + offset
    loop_bounds[3] = loop_bounds[3] + offset
    loop_bounds = box(*loop_bounds)
    return loop_bounds


def get_loop_number(cursor: sqlite3.Cursor):
    """
    get the number of loop in database
    :param cursor: the cursor of database
    :return: int
    """
    return cursor.execute('SELECT max(loopID) FROM ContactLoops').fetchone()[0]


def is_two_polygon_overlap(polygon_1: polygon.Polygon, polygon_2: polygon.Polygon, offset: float = 0.1):
    bounds_1 = get_loop_bounds(loop_polygon=polygon_1, offset=offset)
    bounds_2 = box(*polygon_2.bounds)

    # TODO:function select: intersects, overlap, touch?
    is_overlap = bounds_1.intersects(bounds_2)
    return is_overlap


def get_window_size(cursor: sqlite3.Cursor = None):
    database_statement = 'SELECT min(xValue), min(yValue), max(xValue), max(yValue) FROM JointPoints'
    window_xy = cursor.execute(database_statement)
    window_xy = window_xy.fetchall()[0]
    window_bounds = box(*window_xy)
    return window_bounds


if __name__ == '__main__':
    database_name = '../../data/test.db'
    database_connect = sqlite3.connect(database_name)
    database_cursor = database_connect.cursor()
    a = get_loop_number(database_cursor)
    print(a)
    loop_polygon_temp, loop_line_temp = get_one_loop(1, cursor=database_cursor)
    loop_polygon_temp_2, loop_line_temp_2 = get_one_loop(2, cursor=database_cursor)
    is_two_polygon_overlap(loop_polygon_temp, loop_polygon_temp_2)
