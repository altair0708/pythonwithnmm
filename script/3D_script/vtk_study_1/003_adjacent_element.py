from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points = vtkPoints()
points.InsertNextPoint((0, 0, 0))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((1, 1, 0))
points.InsertNextPoint((0, 1, 0))

points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((1, 0, 1))
points.InsertNextPoint((1, 1, 1))
points.InsertNextPoint((0, 1, 1))

points.InsertNextPoint((0, 0, 0))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((1, 1, 0))
points.InsertNextPoint((0, 1, 0))

points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((1, 0, 1))
points.InsertNextPoint((1, 1, 1))
points.InsertNextPoint((0, 1, 1))

point_list = vtkIdList()
point_list.InsertNextId(4)

point_list.InsertNextId(3)
point_list.InsertNextId(4)
point_list.InsertNextId(0)
point_list.InsertNextId(1)

point_list.InsertNextId(3)
point_list.InsertNextId(4)
point_list.InsertNextId(1)
point_list.InsertNextId(3)

point_list.InsertNextId(3)
point_list.InsertNextId(4)
point_list.InsertNextId(3)
point_list.InsertNextId(0)

point_list.InsertNextId(3)
point_list.InsertNextId(0)
point_list.InsertNextId(1)
point_list.InsertNextId(3)

point_list_1 = vtkIdList()
point_list_1.InsertNextId(4)

point_list_1.InsertNextId(3)
point_list_1.InsertNextId(6)
point_list_1.InsertNextId(4)
point_list_1.InsertNextId(1)
# point_list_1.InsertNextId(14)
# point_list_1.InsertNextId(12)
# point_list_1.InsertNextId(9)

point_list_1.InsertNextId(3)
point_list_1.InsertNextId(6)
point_list_1.InsertNextId(1)
point_list_1.InsertNextId(3)
# point_list_1.InsertNextId(14)
# point_list_1.InsertNextId(9)
# point_list_1.InsertNextId(11)

point_list_1.InsertNextId(3)
point_list_1.InsertNextId(6)
point_list_1.InsertNextId(3)
point_list_1.InsertNextId(4)
# point_list_1.InsertNextId(14)
# point_list_1.InsertNextId(11)
# point_list_1.InsertNextId(12)

point_list_1.InsertNextId(3)
point_list_1.InsertNextId(1)
point_list_1.InsertNextId(3)
point_list_1.InsertNextId(4)
# point_list_1.InsertNextId(9)
# point_list_1.InsertNextId(11)
# point_list_1.InsertNextId(12)

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(VTK_POLYHEDRON, point_list)
u_grid.InsertNextCell(VTK_POLYHEDRON, point_list_1)
u_grid.SetPoints(points)

cell_id_list = vtkIdList()
point_id_list = vtkIdList()
point_id_list.InsertNextId(3)
point_id_list.InsertNextId(4)
point_id_list.InsertNextId(1)

u_grid.GetCellNeighbors(2, point_id_list, cell_id_list)
print(point_id_list)
print(cell_id_list)

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re003_1.vtu')
writer.SetInputData(u_grid)
writer.Write()
