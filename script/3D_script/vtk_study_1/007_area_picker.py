from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.ElementIntersectionFunction import check_intersect
from NMM.base.CopyFunction import copy_vtk_cell

points = vtkPoints()
points.InsertNextPoint((0, 0, 0))
points.InsertNextPoint((0, 1, 0))
points.InsertNextPoint((1, 1, 0))
points.InsertNextPoint((1, 0, 0))

points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((0, 1, 1))
points.InsertNextPoint((1, 1, 1))
points.InsertNextPoint((1, 0, 1))

points.InsertNextPoint((0, 0, 2))
points.InsertNextPoint((0, 1, 2))
points.InsertNextPoint((1, 1, 2))
points.InsertNextPoint((1, 0, 2))

points.InsertNextPoint((0.5, 0.5, 0.5))
points.InsertNextPoint((0.5, 1.5, 0.5))
points.InsertNextPoint((0.5, 1.5, 2.5))
points.InsertNextPoint((0.5, 0.5, 2.5))

points.InsertNextPoint((4, 0, 2))
points.InsertNextPoint((4, 0, -2))
points.InsertNextPoint((0, 0, -2))
points.InsertNextPoint((0, 0, 2))

box_0 = vtkHexahedron()
box_0.GetPointIds().SetId(0, 0)
box_0.GetPointIds().SetId(1, 1)
box_0.GetPointIds().SetId(2, 2)
box_0.GetPointIds().SetId(3, 3)
box_0.GetPointIds().SetId(4, 4)
box_0.GetPointIds().SetId(5, 5)
box_0.GetPointIds().SetId(6, 6)
box_0.GetPointIds().SetId(7, 7)

box_1 = vtkHexahedron()
box_1.GetPointIds().SetId(0, 4)
box_1.GetPointIds().SetId(1, 5)
box_1.GetPointIds().SetId(2, 6)
box_1.GetPointIds().SetId(3, 7)
box_1.GetPointIds().SetId(4, 8)
box_1.GetPointIds().SetId(5, 9)
box_1.GetPointIds().SetId(6, 10)
box_1.GetPointIds().SetId(7, 11)

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(4)
polygon_0.GetPointIds().SetId(0, 12)
polygon_0.GetPointIds().SetId(1, 13)
polygon_0.GetPointIds().SetId(2, 14)
polygon_0.GetPointIds().SetId(3, 15)

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(4)
polygon_1.GetPointIds().SetId(0, 16)
polygon_1.GetPointIds().SetId(1, 17)
polygon_1.GetPointIds().SetId(2, 18)
polygon_1.GetPointIds().SetId(3, 19)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(box_0.GetCellType(), box_0.GetPointIds())
u_grid.InsertNextCell(box_1.GetCellType(), box_1.GetPointIds())
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())
u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())

cell_0: vtkCell = u_grid.GetCell(0)
new_cell_0 = copy_vtk_cell(vtk_cell=cell_0, vtk_points=u_grid.GetPoints())
cell_1: vtkCell = u_grid.GetCell(1)
new_cell_1 = copy_vtk_cell(vtk_cell=cell_1, vtk_points=u_grid.GetPoints())
cell_2: vtkPolygon = u_grid.GetCell(2)
new_cell_2: vtkPolygon = copy_vtk_cell(vtk_cell=cell_2, vtk_points=u_grid.GetPoints())

print(new_cell_0.IntersectWithCell(new_cell_2))
print(new_cell_1.IntersectWithCell(new_cell_2))
n = [0, 0, 0]
vtkPolygon.ComputeNormal(new_cell_2.GetPoints(), n)
print(n)


writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName('re007_0.vtu')
writer.Write()


