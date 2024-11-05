from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


def check_point_in_cell(point_grid: vtkUnstructuredGrid, vtk_model: vtkUnstructuredGrid):
    assert point_grid.GetNumberOfCells() == 1
    assert vtk_model.GetNumberOfCells() == 1

    point = [0, 0, 0]
    point_grid.GetPoint(0, point)

    locator = vtk_model.GetPointLocator()
    if locator is None:
        vtk_model.BuildLocator()
        locator = vtk_model.GetPointLocator()

    result = vtkIdList()
    locator.FindPointsWithinRadius(0.0001, point, result)
    if result.GetNumberOfIds() == 0:
        return False
    elif result.GetNumberOfIds() > 0:
        return True
    else:
        raise Exception('Point number error!!!')
