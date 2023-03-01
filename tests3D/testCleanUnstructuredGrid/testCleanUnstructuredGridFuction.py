from NMM.base.CleanUnstructuredGridFunction import clean_unstructured_grid
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolygon, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridReader


def test_clean_unstructured_grid():
    points_1 = vtkPoints()
    points_1.InsertNextPoint(0, 0, 0)
    points_1.InsertNextPoint(1, 0, 0)
    points_1.InsertNextPoint(1, 0, 1)
    points_1.InsertNextPoint(0, 0, 1)

    points_2 = vtkPoints()
    points_2.InsertNextPoint(0, 0, 0)
    points_2.InsertNextPoint(0, 1, 0)
    points_2.InsertNextPoint(0, 1, 1)
    points_2.InsertNextPoint(0, 0, 1)

    polygon_1 = vtkPolygon()
    polygon_1.GetPointIds().SetNumberOfIds(4)
    polygon_1.GetPointIds().SetId(0, 0)
    polygon_1.GetPointIds().SetId(1, 1)
    polygon_1.GetPointIds().SetId(2, 2)
    polygon_1.GetPointIds().SetId(3, 3)
    u_grid = vtkUnstructuredGrid()
    u_grid.SetPoints(points_1)
    u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())

    polygon_2 = vtkPolygon()
    polygon_2.GetPointIds().SetNumberOfIds(4)
    polygon_2.GetPointIds().SetId(0, 0)
    polygon_2.GetPointIds().SetId(1, 1)
    polygon_2.GetPointIds().SetId(2, 2)
    polygon_2.GetPointIds().SetId(3, 3)

    new_grid = clean_unstructured_grid(u_grid)
    assert new_grid.GetNumberOfPoints() == 6

    reader = vtkXMLUnstructuredGridReader()
    reader.SetFileName('error_0.vtu')
    reader.Update()
    grid_0 = reader.GetOutput()

    grid_1 = clean_unstructured_grid(grid_0)
    assert grid_1.GetNumberOfPoints() == 5


def test_two_point():

    a = vtkVertex()
    a.GetPointIds().SetId(0, 0)

    b = vtkVertex()
    b.GetPointIds().SetId(0, 1)

    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(0, 0, 0)

    test_grid = vtkUnstructuredGrid()
    test_grid.InsertNextCell(a.GetCellType(), a.GetPointIds())
    test_grid.InsertNextCell(b.GetCellType(), b.GetPointIds())
    test_grid.SetPoints(points)

    assert test_grid.GetNumberOfPoints() == 2
    new_grid = clean_unstructured_grid(test_grid)
    assert new_grid.GetNumberOfPoints() == 1





