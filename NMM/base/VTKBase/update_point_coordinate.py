from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
import numpy as np


def update_point_coordinate(vtk_model: vtkUnstructuredGrid, point_id: int, coordinate):
    assert len(coordinate) == 3
    points = vtkPoints()
    points.ShallowCopy(vtk_model.GetPoints())
    points.SetPoint(point_id, coordinate)
