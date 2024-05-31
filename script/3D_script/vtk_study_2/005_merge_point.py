from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex, vtkMergePoints
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference

points = vtkPoints()
# points.InsertNextPoint(0, 0, 0)
# points.InsertNextPoint(1, 1, 1)
# points.InsertNextPoint(2, 2, 2)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)

merger = vtkMergePoints()
merger.SetDataSet(u_grid)
merger.InitPointInsertion(u_grid.GetPoints(), u_grid.GetBounds())
merger.Update()

# u_grid.SetPointLocator(merger)

a = reference(999)
merger.InsertUniquePoint((0, 0, 0), a)
print(a)
print(merger.GetPoints().GetPoint(a))

b = reference(999)
merger.InsertUniquePoint((3, 3, 3), b)
print(b)
print(merger.GetPoints().GetPoint(b))
print(merger.GetPoints().GetPoint(1))
# print(merger.GetPoints().GetPoint(2))

# c = reference((9, 9, 9))
c = [0, 0, 0]
u_grid.GetPoint(0, c)
print(c)

new_grid = vtkUnstructuredGrid()
points = vtkPoints()
new_grid.SetPoints(points)

# merger.Update()
# print(merger.GetDataSet().GetNumberOfPoints())
