from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, vtkPolygon, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkFiltersCore import vtkRemoveUnusedPoints
from vtkmodules.vtkFiltersGeneral import vtkCleanUnstructuredGrid
from NMM.base.VTKBase.write_file import write_file
from typing import List


def get_a_vtk_cell_grid(vtk_model: vtkUnstructuredGrid, id_value: int, turn_polyhedron=False):

    if id_value >= vtk_model.GetNumberOfCells():
        raise IndexError

    # cell type
    cell_type = vtk_model.GetCellType(id_value)

    # id list
    cell_id_list = vtkIdList()
    if 42 == cell_type:
        # polyhedron
        vtk_model.GetFaceStream(id_value, cell_id_list)
    else:
        # other vtk_cell
        cell_id_list.DeepCopy(vtk_model.GetCell(id_value).GetPointIds())

    # cell points
    cell_points = vtkPoints()
    cell_points.DeepCopy(vtk_model.GetPoints())

    new_grid = vtkUnstructuredGrid()
    new_grid.InsertNextCell(cell_type, cell_id_list)
    new_grid.SetPoints(cell_points)

    # turn vtk_cell to vtk_polyhedron
    if turn_polyhedron is True and VTK_POLYHEDRON != cell_type:
        vtk_cell: vtkCell = new_grid.GetCell(0)

        face_list = [vtk_cell.GetNumberOfFaces()]

        for each_face_id in range(vtk_cell.GetNumberOfFaces()):
            face_list = face_list + [vtk_cell.GetFace(each_face_id).GetNumberOfPoints()]
            face_list = face_list + id_list_2_list(vtk_cell.GetFace(each_face_id).GetPointIds())

        new_grid = vtkUnstructuredGrid()
        new_grid.InsertNextCell(VTK_POLYHEDRON, list_2_id_list(face_list))
        new_grid.SetPoints(cell_points)

    # clean unused points
    cleaner = vtkCleanUnstructuredGrid()
    # cleaner = vtkRemoveUnusedPoints()
    cleaner.RemovePointsWithoutCellsOn()
    cleaner.SetInputData(new_grid)
    cleaner.Update()
    new_grid = cleaner.GetOutput()

    return new_grid


def id_list_2_list(id_list: vtkIdList):
    result = []
    for each_id in range(id_list.GetNumberOfIds()):
        result.append(id_list.GetId(each_id))
    return result


def list_2_id_list(id_list: List[int]):
    result = vtkIdList()
    for each_id in id_list:
        result.InsertNextId(each_id)
    return result

