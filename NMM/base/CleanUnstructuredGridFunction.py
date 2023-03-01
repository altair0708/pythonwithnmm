from vtkmodules.vtkCommonDataModel import vtkMergePoints, vtkUnstructuredGrid, vtkPolygon, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkCleanPolyData
from vtkmodules.vtkCommonCore import vtkPoints, reference, mutable
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter


def clean_unstructured_grid(ugrid):
    """Collapse a vtu produced from a discontinuous grid back down to the continuous space.

    Args:
    ugrid (vtkUnstructuredGrid): the input discontinuous grid

    Results
    out_grid (vtkUnstructuredGrid): A continuous grid"""

    out_grid = vtkUnstructuredGrid()

    point_number = ugrid.GetNumberOfPoints()

    point_source = vtkPointSource()
    point_source.SetNumberOfPoints(point_number)
    point_source.Update()
    point_s = point_source.GetOutput()

    merge_points = vtkMergePoints()
    merge_points.SetDataSet(point_s)
    # merge_points.SetDivisions(10, 10, 10)
    merge_points.InitPointInsertion(point_s.GetPoints(), point_s.GetBounds())

    a = mutable(0)
    for i in range(ugrid.GetNumberOfPoints()):
        merge_points.InsertUniquePoint(ugrid.GetPoints().GetPoint(i), a)
        # print('point:', i)
        # print(ugrid.GetPoints().GetPoint(i))
        # print('id:', a)
        # merge_points.IsInsertedPoint(ugrid.GetPoints().GetPoint(i))

    merge_points.BuildLocator()
    point_s = merge_points.GetPoints()
    # print('point number:', point_s.GetNumberOfPoints())
    # for i in range(point_s.GetNumberOfPoints()):
    #     print('coord:', point_s.GetPoint(i))

    pts = vtkPoints()
    pts.DeepCopy(merge_points.GetPoints())
    out_grid.SetPoints(pts)

    for i in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(i)
        cell_ids = cell.GetPointIds()

        for j in range(cell.GetNumberOfPoints()):

            original_point = cell.GetPoints().GetPoint(j)
            # print('original point: ', original_point)
            # print('is inserted point:', merge_points.IsInsertedPoint(original_point))
            point_id = merge_points.IsInsertedPoint(original_point)
            assert point_id != -1
            cell_ids.SetId(j, point_id)

        out_grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

    out_grid.GetCellData().DeepCopy(ugrid.GetCellData())

    return out_grid


def clean_poly_data(poly_data: vtkPolyData):
    cleaner = vtkCleanPolyData()
    cleaner.SetInputData(poly_data)
    cleaner.Update()
    result: vtkPolyData = cleaner.GetOutput()
    return result


if __name__ == '__main__':

    points = vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 0, 1)
    points.InsertNextPoint(0, 0, 1)

    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(0, 1, 0)
    points.InsertNextPoint(0, 1, 1)
    points.InsertNextPoint(0, 0, 1)

    polygon_1 = vtkPolygon()
    polygon_1.GetPointIds().SetNumberOfIds(4)
    polygon_1.GetPointIds().SetId(0, 0)
    polygon_1.GetPointIds().SetId(1, 1)
    polygon_1.GetPointIds().SetId(2, 2)
    polygon_1.GetPointIds().SetId(3, 3)

    polygon_2 = vtkPolygon()
    polygon_2.GetPointIds().SetNumberOfIds(4)
    polygon_2.GetPointIds().SetId(0, 4)
    polygon_2.GetPointIds().SetId(1, 5)
    polygon_2.GetPointIds().SetId(2, 6)
    polygon_2.GetPointIds().SetId(3, 7)

    u_grid = vtkUnstructuredGrid()
    u_grid.SetPoints(points)
    u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())
    u_grid.InsertNextCell(polygon_2.GetCellType(), polygon_2.GetPointIds())

    new_grid = clean_unstructured_grid(u_grid)

    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('re014_1.vtu')
    writer.SetInputData(u_grid)
    writer.Write()

    writer = vtkXMLUnstructuredGridWriter()
    writer.SetFileName('re014_2.vtu')
    writer.SetInputData(new_grid)
    writer.Write()

