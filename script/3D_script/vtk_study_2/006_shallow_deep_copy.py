from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(2, 2, 2)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)

new_grid = vtkUnstructuredGrid()
new_grid.ShallowCopy(u_grid)
# new_grid = u_grid
points.InsertNextPoint(3, 3, 3)

# print(new_grid.GetNumberOfPoints())
# print(u_grid.GetNumberOfPoints())
print(new_grid is u_grid)
