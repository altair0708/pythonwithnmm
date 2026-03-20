import pytest
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.intersection_line_with_polydata import intersection_line_with_polydata


def test_main():

    vtk_model = VtkGrid('vtk_model', 'crack_propagation_intersection.vtu')
    edge = VtkGrid('edge', 'edge.vtu')

    result, points = intersection_line_with_polydata(vtk_model.value, edge.value)
    print(result)
    print(points)

