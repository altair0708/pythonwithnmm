import pytest
import copy
from NMM.base.PointBase import PointBase


class TestPointBase(object):
    def test_id_counter(self):
        point1 = PointBase(1, 1)
        point2 = PointBase(1, 2)
        assert point2.get_id() == 2

    def test_reset_id_counter(self):
        PointBase.reset_id_counter()
        point3 = PointBase(1, 1)
        assert point3.get_id() == 1

    def test_copy_point(self):
        point3 = PointBase(1, 1)
        point4 = point3
        point5 = copy.copy(point3)
        assert point4 is point3
        assert point5 is not point3


if __name__ == '__main__':
    pytest.main()
