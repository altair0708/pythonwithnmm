from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkGenericCell, vtkCellLocator
from vtkmodules.vtkCommonCore import vtkPoints, reference


def find_close_cell(point_grid: vtkUnstructuredGrid = None, vtk_model: vtkUnstructuredGrid = None, point_coord=None):

    if point_grid is not None:
        assert point_grid.GetNumberOfCells() == 1
        assert point_grid.GetNumberOfPoints() == 1
        point_coord = point_grid.GetPoint(0)

    # locator = vtkCellLocator()
    # locator.SetDataSet(vtk_model)
    # locator.BuildLocator()
    # cell_id = locator.FindCell(point_coord)

    sub_id = reference(0)
    cell_id = vtk_model.FindCell(point_coord, None, -1, 0, sub_id, [0, 0, 0], [0, 0, 0, 0])

    return cell_id


