from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkMergePoints, vtkPointLocator


def new_a_grid(allow_duplicate=True):
    new_grid = vtkUnstructuredGrid()
    points = vtkPoints()
    # points.InsertNextPoint((0, 0, 0))
    new_grid.SetPoints(points)

    # whether inserted point duplicated
    if allow_duplicate is True:
        point_locator = vtkPointLocator()
    else:
        point_locator = vtkMergePoints()

    # pointLocator->SetDataSet(pointSource->GetOutput());
    # point_locator.SetDataSet(new_grid)

    point_locator.InitPointInsertion(new_grid.GetPoints(), new_grid.GetBounds())
    # point_locator.InitPointInsertion(new_grid.GetPoints(), [-100, -100, -100, 100, 100, 100])
    # point_locator.InsertNextPoint((0, 0, 0))
    # point_locator.InsertNextPoint((1, 1, 1))
    # point_locator.BuildLocator()
    # point_locator.Update()
    new_grid.SetPointLocator(point_locator)

    return new_grid
