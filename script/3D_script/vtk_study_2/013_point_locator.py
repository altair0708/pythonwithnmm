from vtkmodules.vtkCommonDataModel import vtkPointLocator, vtkUnstructuredGrid, vtkMergePoints
from vtkmodules.vtkCommonCore import vtkIdList, vtkPoints, reference

############################
# Find closed point
points_0 = vtkPoints()
points_0.InsertNextPoint(0, 0, 0)
points_0.InsertNextPoint(1, 1, 1)
points_0.InsertNextPoint(2, 2, 2)

u_grid_0 = vtkUnstructuredGrid()
u_grid_0.SetPoints(points_0)

locator_0 = vtkPointLocator()
locator_0.SetDataSet(u_grid_0)

# # point_0 = (0, 0, 0)
# point_0 = (1, 0, 0)
# result_0 = vtkIdList()
# locator_0.FindPointsWithinRadius(0.00001, point_0, result_0)  # InInsertPoint() error!
# print(result_0.GetNumberOfIds())  # (0, 0, 0) = 1, (1, 0, 0) = 0

###############################
# Insert next point
points_1 = vtkPoints()
points_1.InsertNextPoint(0, 0, 0)
points_1.InsertNextPoint(1, 1, 1)
points_1.InsertNextPoint(2, 2, 2)

u_grid_1 = vtkUnstructuredGrid()
u_grid_1.SetPoints(points_1)
u_grid_1.ComputeBounds()

locator_1 = vtkPointLocator()
locator_1.InitPointInsertion(u_grid_1.GetPoints(), u_grid_1.GetBounds())

locator_1.InsertNextPoint((4, 4, 4))
locator_1.InsertNextPoint((5, 5, 5))
locator_1.InsertNextPoint((6, 6, 6))

# point_1 = (5, 5, 5)
# print(locator_1.IsInsertedPoint(point_1))  # 1. Actually, InitPointInsertion require we input all points by locator.InsertNextPoint().
#
# # point_1 = (0, 0, 0)
# result_1 = vtkIdList()
# locator_1.FindPointsWithinRadius(0.00001, point_1, result_1)
# print(result_1.GetNumberOfIds())  # 0, If without locator.SetDataSet(u_grid), It doesn't work.

###############################
# Insert unique point
points_2 = vtkPoints()

u_grid_2 = vtkUnstructuredGrid()
u_grid_2.SetPoints(points_2)
u_grid_2.ComputeBounds()

locator_2 = vtkMergePoints()
locator_2.InitPointInsertion(u_grid_2.GetPoints(), u_grid_2.GetBounds())  # vtkPoints should be empty.

c = reference(0)
locator_2.InsertUniquePoint((4, 4, 4), c)
locator_2.InsertUniquePoint((5, 5, 5), c)
locator_2.InsertUniquePoint((6, 6, 6), c)

point_2 = (5, 5, 5)
print(locator_2.IsInsertedPoint(point_2))  # id = 1. Actually, InitPointInsertion require we input all points by locator.
print(locator_2.GetPoints().GetNumberOfPoints())  # 3, duplicate point will not be insert.
print(u_grid_2.GetNumberOfPoints())  # 3, duplicate point will not be insert.
