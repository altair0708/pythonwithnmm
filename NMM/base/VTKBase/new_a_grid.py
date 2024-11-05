from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, vtkLogger
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkMergePoints, vtkPointLocator


def new_a_grid(allow_duplicate=True):
    new_grid = vtkUnstructuredGrid()
    new_grid.EditableOn()
    points = vtkPoints()

    # Bounds of model
    points.InsertNextPoint((-100, -100, -100))
    points.InsertNextPoint((100, 100, 100))
    new_grid.ComputeBounds()

    new_grid.SetPoints(points)

    # whether inserted point duplicated
    if allow_duplicate is True:
        point_locator = vtkPointLocator()
        point_locator.SetDataSet(new_grid)
        point_locator.AutomaticOn()
        # point_locator.SetNumberOfPointsPerBucket(2)
        # point_locator.BuildLocator()
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
