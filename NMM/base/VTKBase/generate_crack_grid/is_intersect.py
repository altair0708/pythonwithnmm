from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell


def is_intersect(cell_grid_0: vtkUnstructuredGrid, cell_grid_1: vtkUnstructuredGrid):

    assert cell_grid_0.GetNumberOfCells() == 1
    assert cell_grid_1.GetNumberOfCells() == 1

    cell_0: vtkCell = cell_grid_0.GetCell(0)
    cell_1: vtkCell = cell_grid_1.GetCell(0)

    return cell_0.IntersectWithCell(cell_1)
