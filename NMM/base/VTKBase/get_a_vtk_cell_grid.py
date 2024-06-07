from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList


def get_a_vtk_cell_grid(vtk_model: vtkUnstructuredGrid, id_value: int):
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

    return new_grid
