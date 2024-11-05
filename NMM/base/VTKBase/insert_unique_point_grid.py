from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPointLocator
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
import sys


def insert_unique_point_grid(vtk_model: vtkUnstructuredGrid, point=(0, 0, 0)):

    merger = vtkPointLocator()
    merger.SetDataSet(vtk_model)
    merger.InitPointInsertion(vtk_model.GetPoints(), vtk_model.GetBounds())
    merger.BuildLocator()

    point_id_list = vtkIdList()
    merger.FindPointsWithinRadius(0.001, point, point_id_list)
    try:
        # assert point_id_list.GetNumberOfIds() < 2
        assert point_id_list.GetNumberOfIds() < 10
    except AssertionError:
        sys.exit()

    if point_id_list.GetNumberOfIds() == 0:
        point_id = vtk_model.GetNumberOfPoints()
        vtk_model.GetPoints().InsertNextPoint(point)
    else:
        point_id = point_id_list.GetId(0)

    return point_id
