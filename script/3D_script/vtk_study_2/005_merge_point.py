from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex, vtkMergePoints, vtkPointLocator, vtkIncrementalPointLocator
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference

points = vtkPoints()
# points.InsertNextPoint(0, 0, 0)
# points.InsertNextPoint(1, 1, 1)
# points.InsertNextPoint(2, 2, 2)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)

# merger = vtkMergePoints()
merger = vtkPointLocator()
# merger.SetDataSet(u_grid)
merger.InitPointInsertion(u_grid.GetPoints(), u_grid.GetBounds())
merger.Update()
u_grid.SetPointLocator(merger)

a = reference(999)
b = reference(999)
c = reference(999)
# merger.InsertUniquePoint((0, 0, 0), a)
# merger.InsertUniquePoint((2, 0, 0), b)
# merger.InsertUniquePoint((3, 0, 0), c)
print(merger.InsertNextPoint((0, 0, 0)))
print(merger.InsertNextPoint((0, 0, 0)))
print(merger.InsertNextPoint((1, 0, 0)))
print(merger.InsertNextPoint((1, 0, 0)))
print(merger.InsertNextPoint((2, 0, 0)))
print(merger.InsertNextPoint((2, 0, 0)))
# print(a)
# print(b)
# print(c)

# print(merger.GetPoints().GetPoint(2))

# c = reference((9, 9, 9))
# print(u_grid.GetPoint(1))

# new_grid = vtkUnstructuredGrid()
# points = vtkPoints()
# new_grid.SetPoints(points)
# print(u_grid.GetNumberOfPoints())

# u_grid.EditableOn()
# u_grid.BuildPointLocator()
# print(u_grid.GetPointLocator())
temp_merger: vtkMergePoints = u_grid.GetPointLocator()
d = reference(999)
# temp_merger.InsertUniquePoint((1, 1, 1), d)
# temp_merger.InsertUniquePoint((1, 1, 1), d)
# temp_merger.InsertUniquePoint((1, 1, 1), d)
# temp_merger.InsertUniquePoint((1, 2, 1), d)
print(temp_merger.GetClassName())
print(u_grid.GetNumberOfPoints())

# merger.Update()
# print(merger.GetDataSet().GetNumberOfPoints())
