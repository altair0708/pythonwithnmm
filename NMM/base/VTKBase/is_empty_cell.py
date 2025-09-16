from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkEmptyCell


def is_empty_cell(vtk_model: vtkUnstructuredGrid):
    assert vtk_model.GetNumberOfCells() == 1
    cell = vtk_model.GetCell(0)
    return isinstance(cell, vtkEmptyCell)
