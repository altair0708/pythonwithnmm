from ContactWithDatabase import get_one_loop, get_buffer_from_loop
from shapely.geometry import Point
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
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

    def __eq__(self, other):
        if self.__x == other.x and self.__y == other.y:
            return True
        else:
            return False

    def __str__(self):
        return 'BPoint({x_value}, {y_value})'.format(x_value=self.__x, y_value=self.__y)

    def __getattr__(self, item):
        return self.__point.__getattribute__(item)


class BEdge(object):
    def __init__(self, point1: tuple, point2: tuple):
        if point1 == point2:
            raise Exception('point1 == point2')
        self.__point1 = BPoint(*point1)
        self.__point2 = BPoint(*point2)
        self.__vector = self.__point2 - self.__point1

    def __str__(self):
        return 'start is {point1}, end is {point2}'.format(point1=self.__point1, point2=self.__point2)

    @property
    def point1(self):
        return self.__point1

    @property
    def point2(self):
        return self.__point2

    @property
    def vector(self):
        return self.__vector

    def draw(self):
        plt.plot((self.__point1.x, self.__point2.x), (self.__point1.y, self.__point2.y))


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

    @property
    def vertex(self):
        return self.__vertex

    @property
    def vector1(self):
        return self.__vector1

    @property
    def vector2(self):
        return self.__vector2

    def draw(self):
        plt.scatter((self.__last_point.x, self.__vertex.x, self.__next_point.x),
                    (self.__last_point.y, self.__vertex.y, self.__next_point.y), marker='p', s=100)


class Block(object):
    def __init__(self, id_value: int = None, cursor: sqlite3.Cursor = None):
        self.__point_list = []
        self.__edge_list = []
        self.__angle_list = []
        self.__polygon = None
        self.__line_string = None
        self.__loop_id = 0
        if id_value is not None:
            self.__loop_id = id_value
            self.__polygon, self.__line_string = get_one_loop(id_value=id_value, cursor=cursor)
            self.generate_list()
            self.__centroid = self.__polygon.centroid

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

    @property
    def point_list(self):
        return self.__point_list

    @property
    def edge_list(self):
        return self.__edge_list

    @property
    def angle_list(self):
        return self.__angle_list

    @property
    def polygon(self):
        return self.__polygon

    @polygon.setter
    def polygon(self, temp_polygon):
        self.__polygon = temp_polygon
        self.generate_list()

    @property
    def centroid(self):
        return self.__centroid


class EAB(object):
    def __init__(self, block_a: Block, block_b: Block):
        self.__block_a = block_a
        self.__block_b = block_b
        self.__eab_c10 = []
        self.__eab_c01 = []
        self.__eab = []
        self.__eab_polygon = None
        for each_angle in self.__block_a.angle_list:
            for each_edge in self.__block_b.edge_list:
                if self.is_contact_group(each_angle, each_edge):
                    self.__eab_c01.append(self.generate_eab_edge_ab(each_angle, each_edge, block_a.centroid))
                    self.__eab.append(self.generate_eab_edge_ab(each_angle, each_edge, block_a.centroid))
        for each_angle in self.__block_b.angle_list:
            for each_edge in self.__block_a.edge_list:
                if self.is_contact_group(each_angle, each_edge):
                    self.__eab_c10.append(self.generate_eab_edge_ba(each_angle, each_edge, block_a.centroid))
                    self.__eab.append(self.generate_eab_edge_ba(each_angle, each_edge, block_a.centroid))

    @property
    def eab(self):
        return self.__eab

    @staticmethod
    def is_contact_group(angle: BAngle, edge: BEdge):
        edge_norm_vector = get_normal_vector(edge.vector)
        angle_norm_vector = get_normal_vector(angle.vector2 - angle.vector1)
        dot1 = np.dot(np.array(angle.vector1.xy).T, np.array(edge_norm_vector.xy))
        dot2 = np.dot(np.array(angle.vector2.xy).T, np.array(edge_norm_vector.xy))
        dot3 = np.dot(np.array(edge_norm_vector.xy).T, np.array(angle_norm_vector.xy))
        if dot1 > 0 or dot2 > 0:
            return False
        else:
            return True

    @staticmethod
    def generate_eab_edge_ab(angle: BAngle, edge: BEdge, centroid: BPoint):
        point1 = edge.point1 - angle.vertex + centroid
        point2 = edge.point2 - angle.vertex + centroid
        return BEdge((point1.x, point1.y), (point2.x, point2.y))

    @staticmethod
    def generate_eab_edge_ba(angle: BAngle, edge: BEdge, centroid: BPoint):
        point1 = angle.vertex - edge.point1 + centroid
        point2 = angle.vertex - edge.point2 + centroid
        return BEdge((point1.x, point1.y), (point2.x, point2.y))


def get_direct_vector(vector: BPoint):
    x, y = vector.xy
    x = x[0]
    y = y[0]
    length = np.sqrt(x * x + y * y)
    x = x / length
    y = y / length
    return BPoint(x, y)


def get_normal_vector(vector: BPoint):
    np_vector = np.array(vector.xy)
    transform_matrix = np.array([[0, -1], [1, 0]])
    normal_vector = np.dot(transform_matrix, np_vector)
    result = BPoint(normal_vector[0], normal_vector[1])
    return result


if __name__ == "__main__":
    database_name = '../../data/test.db'
    database_connect = sqlite3.connect(database_name)
    database_cursor = database_connect.cursor()
    blockA = Block(id_value=2, cursor=database_cursor)
    blockB = Block(id_value=1, cursor=database_cursor)
    blockA.draw_boundary()
    blockB.draw_boundary()
    centroid_a = blockA.centroid.xy
    plt.plot(*centroid_a, marker='p')
    EAB1 = EAB(blockA, blockB)
    for i in EAB1.eab:
        i.draw()
    plt.show()

