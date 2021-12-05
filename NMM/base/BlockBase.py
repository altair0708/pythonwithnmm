from ContactWithDatabase import get_one_loop, get_buffer_from_loop
from shapely.geometry import Point
import sqlite3
import matplotlib.pyplot as plt
"""
This file is about shape with Block(loop), it used to calculate EAB
eg : BlockPoint(BPoint), BlockEdge(BEdge), BlockAngle(BAngle), Block
"""


class BPoint(object):
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__point = Point(x, y)

    def __sub__(self, other):
        return BPoint(self.__x - other.x, self.__y - other.y)

    def __add__(self, other):
        return BPoint(self.__x + other.x, self.__y + other.y)

    def __str__(self):
        return 'BPoint({x_value}, {y_value})'.format(x_value=self.__x, y_value=self.__y)

    def __getattr__(self, item):
        return self.__point.__getattribute__(item)


class BEdge(object):
    def __init__(self, point1: tuple, point2: tuple):
        self.__point1 = BPoint(*point1)
        self.__point2 = BPoint(*point2)

    def __str__(self):
        return 'start is {point1}, end is {point2}'.format(point1=self.__point1, point2=self.__point2)

    def draw(self):
        plt.plot((self.__point1.x, self.__point2.x), (self.__point1.y, self.__point2.y), linewidth=10)
        plt.show()


class BAngle(object):
    def __init__(self, point1: tuple, point2: tuple, point3: tuple):
        self.__vertex = BPoint(*point1)
        self.__last_point = BPoint(*point2)
        self.__next_point = BPoint(*point3)
        self.__vector1 = self.__last_point - self.__vertex
        self.__vector2 = self.__next_point - self.__vertex
        # todo:how to get the angle degree?
        self.__angle = None

    def __str__(self):
        return 'vertex is {}, last point is {}, next point is {}'\
            .format(self.__vertex, self.__last_point, self.__next_point)

    def draw(self):
        plt.scatter((self.__last_point.x, self.__vertex.x, self.__next_point.x),
                    (self.__last_point.y, self.__vertex.y, self.__next_point.y), marker='p', s=100)
        plt.show()


class Block(object):
    def __init__(self, id_value: int, cursor: sqlite3.Cursor):
        self.__loop_id = id_value
        self.__polygon, self.__line_string = get_one_loop(id_value=id_value, cursor=cursor)
        self.__point_list = []
        self.__edge_list = []
        self.__angle_list = []
        self.generate_list()

    def generate_list(self):
        temp_list = list(self.__polygon.exterior.coords)
        temp_list_0 = temp_list.copy()  # offset = 0
        temp_list_1 = temp_list.copy()  # move left, offset = 1
        temp_list_2 = temp_list.copy()  # move right, offset = 1
        temp_list_0.pop()
        temp_list_1.pop(0)
        temp_list_2.pop()
        temp = temp_list_2.pop()
        temp_list_2.insert(0, temp)
        for each_number in range(len(temp_list_0)):
            self.__point_list.append(BPoint(*temp_list_0[each_number]))
            self.__edge_list.append(BEdge(temp_list_0[each_number], temp_list_1[each_number]))
            self.__angle_list.append(BAngle(temp_list_0[each_number], temp_list_1[each_number], temp_list_2[each_number]))

    def draw_boundary(self):
        x, y = self.__polygon.exterior.xy
        plt.plot(x, y)
        plt.show()

    @property
    def point_list(self):
        return self.__point_list

    @property
    def edge_list(self):
        return self.__edge_list

    @property
    def angle_list(self):
        return self.__angle_list


class EAB(object):
    def __init__(self, block_a: Block, block_b: Block):
        self.__block_a = block_a
        self.__block_b = block_b
        self.__eab_c10 = []
        self.__eab_c01 = []
        self.__eab_polygon = None

    @staticmethod
    def is_contact_group(angle: BAngle, edge: BEdge):
        pass

    @staticmethod
    def get_eab(angle: BAngle, edge: BEdge):
        pass


if __name__ == "__main__":
    database_name = '../../data/test.db'
    database_connect = sqlite3.connect(database_name)
    database_cursor = database_connect.cursor()
    blockA = Block(4, cursor=database_cursor)
    blockA.draw_boundary()
    print(blockA.point_list[0] + blockA.point_list[0])
    print(blockA.point_list[0])
