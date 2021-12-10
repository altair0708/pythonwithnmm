import pytest
from random import uniform
from NMM.contact.BlockBase import *


def test_point_minus():
    point_a = BPoint(1, 1)
    point_b = BPoint(5, 4)
    point_c = point_b - point_a
    assert point_c == BPoint(4, 3)


def test_get_direct_vector():
    point_a = BPoint(5, 0)
    point_b = get_direct_vector(point_a)
    point_c = BPoint(3, 4)
    point_d = get_direct_vector(point_c)
    assert point_b == BPoint(1, 0)
    assert point_d == BPoint(0.6, 0.8)


def test_get_normal_vector():
    point_a = BPoint(5, 0)
    point_b = get_normal_vector(point_a)
    assert point_b == BPoint(0, 5)


def test_is_same_direct():
    for step in range(100):
        vector_a = BPoint(1, 2) - BPoint(1, 1) + BPoint(uniform(-0.001, 0.001), uniform(-0.001, 0.001))
        vector_b = BPoint(0.5, 0.5) - BPoint(0.5, 1) + BPoint(uniform(-0.001, 0.001), uniform(-0.001, 0.001))
        result = is_same_direct(vector_a, vector_b)
        assert result is False
    vector_a = BPoint(1.001, 0)
    vector_b = BPoint(-0.999, 0)
    result = is_same_direct(vector_a, vector_b)
    assert result is False


def test_edge_direct():
    vector_a = BPoint(1, 0)
    edge_a = BEdge((0, 0), (1, 0))
    result = is_same_direct(vector_a, edge_a.vector)
    assert result is True
    edge1 = BEdge((0, 0), (1, 0))
    angle1 = BAngle((0, 0), (-1, 1), (1, 1))
    result1 = is_same_direct(angle1.vector1, edge1.vector)
    result2 = is_same_direct(angle1.vector2, edge1.vector)
    assert result1 is False
    assert result2 is True


def test_vectors_multiple():
    vector_a = BPoint(1, 0)
    vector_b = BPoint(1, 0)
    result = vector_a * vector_b
    assert result == 1
    vector_a = BPoint(2, 2)
    vector_b = BPoint(1, 1)
    result = vector_a * vector_b
    assert result == 4


def test_get_angle_degree():
    temp = fra()
    for step in range(100):
        angle1 = BAngle((next(temp), next(temp)), (next(temp) - 1, next(temp)), (next(temp) + 1, next(temp)))
        result = get_angle_degree(angle1)
        assert result > 179
    angle1 = BAngle((0, 0), (-1, 1), (1, 1))
    result = get_angle_degree(angle1)
    assert result == 90


# TODO:
# def test_is_contact_group_180_false():
#     """
#     angle = 180
#     """
#     temp = fra()
#     for step in range(100):
#         edge = BEdge((next(temp), next(temp)), (next(temp) + 1, next(temp)))
#         angle = BAngle((next(temp), next(temp)), (next(temp) - 1, next(temp)), (next(temp) + 1, next(temp)))
#         result = EAB.is_contact_group(angle, edge)
#         assert result is False
#
#
# def test_is_contact_group_180_true():
#     """
#     angle = 180
#     """
#     temp = fra()
#     for step in range(100):
#         edge = BEdge((next(temp), next(temp)), (next(temp) - 1, next(temp)))
#         angle = BAngle((next(temp), next(temp)), (next(temp) - 1, next(temp)), (next(temp) + 1, next(temp)))
#         result = EAB.is_contact_group(angle, edge)
#         try:
#             assert result is True
#         except AssertionError:
#             print('______________')
#             print(edge)
#             print(angle)
#             assert result is True


def test_cross_value():
    angle_a = BAngle((0, 0), (-1, 1), (1, 1))
    print(angle_a.vector1.x)
    print(angle_a.vector1.y)
    print(angle_a.cross_value)
    assert angle_a.cross_value < 0


def fra():
    while True:
        temp = uniform(-0.001, 0.001)
        yield temp


if __name__ == '__main__':
    pytest.main()
