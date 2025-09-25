from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkEmptyCell, VTK_EMPTY_CELL


def is_empty_cell(vtk_model: vtkUnstructuredGrid):
    assert vtk_model.GetNumberOfCells() == 1
    cell = vtk_model.GetCell(0)
    return isinstance(cell, vtkEmptyCell)


def is_empty_cell_id(vtk_model: vtkUnstructuredGrid, cell_id):
    cell = vtk_model.GetCell(cell_id)
    if cell.GetCellType() == VTK_EMPTY_CELL:
        return True
    else:
        return False

