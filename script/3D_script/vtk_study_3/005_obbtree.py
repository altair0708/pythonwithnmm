from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPolyData, vtkPolygon, vtkCellArray, vtkTriangle
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkFiltersGeneral import vtkOBBTree


point_0 = (0.00366004, -0.353578, 6.9359)
point_1 = (0.141635, -0.379163, 6.79339)

points = vtkPoints()
# points.SetDataTypeToDouble()
points.InsertNextPoint((0, 0.235402, 7.70897))
points.InsertNextPoint((0, -0.987611, 7.14508))
points.InsertNextPoint((0, 0.477569, 6.36915))

polygon = vtkTriangle()
polygon.GetPointIds().SetId(0, 0)
polygon.GetPointIds().SetId(1, 1)
polygon.GetPointIds().SetId(2, 2)

cells = vtkCellArray()
cells.InsertNextCell(polygon)

poly_data = vtkPolyData()
poly_data.SetPolys(cells)
poly_data.SetPoints(points)

obb_tree = vtkOBBTree()
obb_tree.SetDataSet(poly_data)
# print(obb_tree.GetToleranceMaxValue())
# print(obb_tree.GetTolerance())
# obb_tree.SetTolerance(1)
# print(obb_tree.GetTolerance())
# print(obb_tree.GetToleranceMinValue())
obb_tree.BuildLocator()

intersection = vtkPoints()

obb_tree.IntersectWithLine(point_0, point_1, intersection, None)
point_number = intersection.GetNumberOfPoints()

print(f'point number: {point_number}')
if point_number > 0:
    print(f'coordinate: {intersection.GetPoint(0)}')

