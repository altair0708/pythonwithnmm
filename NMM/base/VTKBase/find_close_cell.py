from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkCellLocator
from vtkmodules.vtkCommonCore import vtkPoints, reference


def find_close_cell(point_grid: vtkUnstructuredGrid, vtk_model: vtkUnstructuredGrid):
    assert point_grid.GetNumberOfCells() == 1
    assert point_grid.GetNumberOfPoints() == 1

    point_coord = point_grid.GetPoint(0)
    sub_id = reference(0)
    cell_id = vtk_model.FindCell(point_coord, None, -1, 0, sub_id, [0, 0, 0], [0, 0, 0, 0])

    return cell_id


