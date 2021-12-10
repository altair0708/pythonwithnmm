import sqlite3
from itertools import product
from shapely.geometry import LineString, Polygon, box, linestring, polygon, multipolygon, Point


def get_one_loop(id_value: int, cursor: sqlite3.Cursor = None) -> (polygon.Polygon, linestring.LineString):
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


def get_buffer_from_loop(loop_list_c, step_offset: float = 0.1, is_separated: bool = False):
    """
    find all the overlap area from the list consist of each group which contain every two loops
    :param loop_list_c: combination of loop list
    :param step_offset: the max allow displacement of each time step
    :param is_separated: if separate the multipolygon into simple polygon, default is False
    :return: the list of overlap id and area
    """
    overlap_loop_id = []
    for each_group in loop_list_c:
        overlap_area = each_group[0][1].intersection(each_group[1][1])
        if not overlap_area.is_empty:
            overlap_area = overlap_area.buffer(step_offset)
            if is_separated and isinstance(overlap_area, multipolygon.MultiPolygon):
                for each_polygon in overlap_area:
                    overlap_loop_id.append((each_group[0][0], each_group[1][0], each_polygon))
                continue
            overlap_loop_id.append((each_group[0][0], each_group[1][0], overlap_area))

    return overlap_loop_id


def get_loop_point_in_area(loop_id: int, area, cursor: sqlite3.Cursor):
    point_list = []
    database_statement = 'SELECT * FROM ContactLoops AS CL INNER JOIN JointPoints AS JP ' \
                         'ON CL.jointID = JP.ID WHERE loopID = {loop_id}'.format(loop_id=loop_id)
    temp_result = cursor.execute(database_statement).fetchall()
    for each_point in temp_result:
        temp_point = Point((each_point[6], each_point[7]))
        if temp_point.intersects(area):
            point_list.append(temp_point)
    return point_list


def get_possible_contact_from_loop(loop_id_1: int, loop_id_2: int, overlap_area, cursor: sqlite3.Cursor):
    point_list_1 = get_loop_point_in_area(loop_id_1, overlap_area, cursor)
    point_list_2 = get_loop_point_in_area(loop_id_2, overlap_area, cursor)
    combination_point_list = product(point_list_1, point_list_2)
    combination_point_list = list(combination_point_list)
    return combination_point_list


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
