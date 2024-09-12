from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPointLocator
from vtkmodules.vtkCommonCore import reference


def insert_a_point(vtk_model: vtkUnstructuredGrid, point):
    point_locator: vtkPointLocator = vtk_model.GetPointLocator()
    if 'vtkPointLocator' == point_locator.GetClassName():
        point_id = point_locator.InsertNextPoint(point)
    elif 'vtkMergePoints' == point_locator.GetClassName():
        point_id = reference(0)
        point_locator.InsertUniquePoint(point, point_id)
    else:
        raise Exception('Grid is unmodifiable!!!')
    return point_id
