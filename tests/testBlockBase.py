import pytest
from NMM.base.BlockBase import *


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


def test_is_contact_group():
    edge1 = BEdge((0, 0), (1, 0))
    angle1 = BAngle((0, 0), (-1, 1), (1, 1))
    result1 = EAB.is_contact_group(angle1, edge1)
    edge2 = BEdge((0, 0), (1, 0))
    angle2 = BAngle((0, 0), (-1, 0), (1, 0))
    result2 = EAB.is_contact_group(angle2, edge2)
    assert result1 is False
    assert result2 is False


if __name__ == '__main__':
    pytest.main()
