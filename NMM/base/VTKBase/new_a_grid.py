from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def new_a_grid():
    new_grid = vtkUnstructuredGrid()
    points = vtkPoints()
    new_grid.SetPoints(points)
    return new_grid
