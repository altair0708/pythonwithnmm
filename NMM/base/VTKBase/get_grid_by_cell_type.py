from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCell, VTK_VERTEX, VTK_LINE, VTK_TRIANGLE, VTK_TETRA
from NMM.base.VTKBase import new_a_grid


def get_grid_by_cell_type(vtk_grid: vtkUnstructuredGrid, geometric_name: str):

    if 'geometric_vertex' == geometric_name:
        cell_type = VTK_VERTEX
    elif 'geometric_line' == geometric_name:
        cell_type = VTK_LINE
    elif 'geometric_surface' == geometric_name:
        cell_type = VTK_TRIANGLE
    elif 'geometric_tetrahedron' == geometric_name:
        cell_type = VTK_TETRA
    else:
        raise Exception('Cell type error!!!')

    new_grid: vtkUnstructuredGrid = new_a_grid()
    cell_number = vtk_grid.GetNumberOfCells()
    for cellId in range(cell_number):
        if vtk_grid.GetCellType(cellId) == cell_type:
            tempCell: vtkCell = vtk_grid.GetCell(cellId)
            new_grid.InsertNextCell(tempCell.GetCellType(), tempCell.GetPointIds())
    new_grid.SetPoints(vtk_grid.GetPoints())

    return new_grid
