from NMM.base.ModifyVtkCell import insert_a_cell_0
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolygon, vtkUnstructuredGrid
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points_1 = vtkPoints()
points_1.InsertNextPoint(0, 0, 0)
points_1.InsertNextPoint(1, 0, 0)
points_1.InsertNextPoint(1, 0, 1)
points_1.InsertNextPoint(0, 0, 1)

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(4)
polygon_1.GetPointIds().SetId(0, 0)
polygon_1.GetPointIds().SetId(1, 1)
polygon_1.GetPointIds().SetId(2, 2)
polygon_1.GetPointIds().SetId(3, 3)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points_1)
u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())
cell_1 = u_grid.GetCell(0)

points_2 = vtkPoints()
points_2.InsertNextPoint(0, 0, 0)
points_2.InsertNextPoint(0, 1, 0)
points_2.InsertNextPoint(0, 1, 1)
points_2.InsertNextPoint(0, 0, 1)

polygon_2 = vtkPolygon()
polygon_2.GetPointIds().SetNumberOfIds(4)
polygon_2.GetPointIds().SetId(0, 0)
polygon_2.GetPointIds().SetId(1, 1)
polygon_2.GetPointIds().SetId(2, 2)
polygon_2.GetPointIds().SetId(3, 3)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points_2)
u_grid.InsertNextCell(polygon_2.GetCellType(), polygon_2.GetPointIds())
cell_2 = u_grid.GetCell(0)

u_grid = vtkUnstructuredGrid()
# points = vtkPoints()
# u_grid.SetPoints(points)

insert_a_cell_0(u_grid, cell_1)
insert_a_cell_0(u_grid, cell_2)

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('00.vtu')
writer.SetInputData(u_grid)
writer.Write()
