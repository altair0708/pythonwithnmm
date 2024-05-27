from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid,
                                           vtkPolyhedron)
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, mutable, vtkMath
from NMM.base.ModifyVtkCell import insert_a_cell


# this method will not lead to duplicated point
def insert_a_grid(vtk_model: vtkUnstructuredGrid, new_grid: vtkUnstructuredGrid):

    assert new_grid.GetNumberOfCells() == 1

    new_point_list = vtkPoints()
    new_point_list.DeepCopy(new_grid.GetPoints())

    new_point_id = vtkIdList()
    new_grid.GetCellPoints(0, new_point_id)

    new_id_list = vtkIdList()
    new_grid.GetFaceStream(0, new_id_list)
    temp_list = []
    for x in range(new_id_list.GetNumberOfIds()):
        temp_list.append(new_id_list.GetId(x))

    new_cell = vtkPolyhedron()
    new_cell.GetPoints().DeepCopy(new_point_list)
    new_cell.GetPointIds().DeepCopy(new_point_id)
    new_cell.SetFaces(temp_list)
    new_cell.Initialize()

    # this function is error: vtkPolyhedron.GetFaces().
    # print(new_cell.GetFaces())

    insert_a_cell(vtk_model, new_cell)
