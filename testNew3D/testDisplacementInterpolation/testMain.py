from NMM.base.Algorithm.ElementRefresher.InterpolationFunction import displacement_interpolation
from NMM.base.Property.Implement import PropertyList


def test_interpolation():
    point_coord = [1, 0, 0]

    cover_coord = PropertyList([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)])
    cover_dis = PropertyList([(0, 0, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2)])

    point_dis = displacement_interpolation(point_coord, cover_dis, cover_coord)
    print(point_dis)
