from vtkmodules.vtkCommonDataModel import vtkMergePoints, vtkUnstructuredGrid, vtkPolyData, vtkPolyVertex
from vtkmodules.vtkCommonCore import mutable, vtkPoints

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(0, 0, 1)
points.InsertNextPoint(0, 0, 2)

poly_data = vtkUnstructuredGrid()
poly_data.SetPoints(points)


a = vtkMergePoints()
a.SetDataSet(poly_data)
a.InitPointInsertion(poly_data.GetPoints(), poly_data.GetBounds())
a.BuildLocator()

x = mutable(0)
a.InsertUniquePoint((0, 0, 0), x)
print(x)
a.InsertUniquePoint((0, 0, 0), x)
print(x)
a.InsertUniquePoint((0, 0, 1), x)
print(x)
a.InsertUniquePoint((0, 0, 4), x)
print(x)
a.InsertUniquePoint((0, 0, 5), x)
print(x)

