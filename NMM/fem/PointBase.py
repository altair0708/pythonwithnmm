import numpy as np
from enum import Enum


class PointType(Enum):
    loading_point = 'loading'
    fixed_point = 'fixed'
    measured_point = 'measured'


class EPoint(object):
    def __init__(self, point_type):
        self.__element_id = 0
        self.__coord = np.zeros((1, 2))
        self.__force = np.zeros((2, 1))
        self.__type = point_type

    @property
    def element_id(self):
        return self.__element_id

    @property
    def coord(self):
        return self.__coord

    @property
    def force(self):
        return self.__force


