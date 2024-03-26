import pytest
from NMM.base.LeastSqPlane import min_distance_plane

def test_min_distance_plane():
    point_list = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)]
    min_distance_plane(point_list)
