from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex, vtkTetra
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from NMM.base.VTKBase import check_point_in_cell


def test_main():
    point = vtkVertex()
    point.GetPointIds().SetId(0, 0)

    points_0 = vtkPoints()
    points_0.InsertNextPoint(0, 0, 0)

    point_grid = vtkUnstructuredGrid()
    point_grid.InsertNextCell(point.GetCellType(), point.GetPointIds())
    point_grid.SetPoints(points_0)


    tetra = vtkTetra()
    tetra.GetPointIds().SetId(0, 0)
    tetra.GetPointIds().SetId(1, 1)
    tetra.GetPointIds().SetId(2, 2)
    tetra.GetPointIds().SetId(3, 3)

    points_1 = vtkPoints()
    points_1.InsertNextPoint(0, 0, 0)
    points_1.InsertNextPoint(1, 0, 0)
    points_1.InsertNextPoint(0, 1, 0)
    points_1.InsertNextPoint(0, 0, 1)

    cell_grid = vtkUnstructuredGrid()
    cell_grid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
    cell_grid.SetPoints(points_1)

    print(check_point_in_cell(point_grid, cell_grid))


