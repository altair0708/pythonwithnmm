from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell


def get_cell_point_id(vtk_model: vtkUnstructuredGrid, cell_id: int):
    vtk_cell: vtkCell = vtk_model.GetCell(cell_id)
    return [vtk_cell.GetPointId(i) for i in range(vtk_cell.GetNumberOfPoints())]

