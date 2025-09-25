from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


def get_point_cell_id(vtk_model: vtkUnstructuredGrid, point_id: int):
    cell_id = vtkIdList()
    vtk_model.GetPointCells(point_id, cell_id)
    id_list = []
    for each in range(cell_id.GetNumberOfIds()):
        id_list.append(cell_id.GetId(each))
    return id_list
