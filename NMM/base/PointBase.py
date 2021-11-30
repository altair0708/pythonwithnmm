#!/usr/bin/python
# -*- coding:utf-8 -*-
def id_generator():
    """This is an id generator, it can generate id number automatically, the start of it is 1."""
    id_number = 1
    while True:
        yield id_number
        id_number += 1


class PointBase(object):
    """
    This is the base class of different kinds of point.
    """
    counter = id_generator()

    def __init__(self, xvalue: float, yvalue: float):

        self.__xvalue = xvalue
        self.__yvalue = yvalue
        self.__id = next(PointBase.counter)

    def get_xvalue(self):
        return self.__xvalue

    def get_yvalue(self):
        return self.__yvalue

    def get_id(self):
        return self.__id

    @classmethod
    def reset_id_counter(cls):
        del PointBase.counter
        PointBase.counter = id_generator()


if __name__ == '__main__':
    pointA = PointBase(1, 1)
    pointB = PointBase(1, 2)
    print(pointB.get_id())

