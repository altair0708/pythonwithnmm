import numpy as np
from enum import Enum


class PointType(Enum):
    loading_point = 'Loading'
    fixed_point = 'Fixed'
    measured_point = 'Measured'


class EPoint(object):
    def __init__(self, point_type):
        self.__element_id = 0
        self.__coord = np.zeros((1, 2))
        self.__force = np.zeros((2, 1))
        self.__type = point_type

    @property
    def element_id(self):
        return self.__element_id

    @element_id.setter
    def element_id(self, id_value: int):
        self.__element_id = id_value

    @property
    def coord(self):
        return self.__coord

    @coord.setter
    def coord(self, coordinate: np.ndarray):
        self.__coord = coordinate

    @property
    def force(self):
        return self.__force

    @property
    def point_type(self):
        return self.__type


if __name__ == '__main__':
    print(type(PointType.fixed_point))
    print(PointType.fixed_point.value)