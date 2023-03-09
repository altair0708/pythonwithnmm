import os
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points = vtkPoints()
points.InsertNextPoint((-0.25, 0, 0.75))
points.InsertNextPoint((-0.25, 0.75, 0))
points.InsertNextPoint((-0.125, 0.25, 0.375))

points.InsertNextPoint((0, -0.25, 0.75))
points.InsertNextPoint((0.75, -0.25, 0))
points.InsertNextPoint((0.25, -0.125, 0.375))

points.InsertNextPoint((0.625, 0.25, -0.125))
points.InsertNextPoint((0.75, 0, -0.25))
points.InsertNextPoint((0.625, 0.125, -0.125))

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(3)
polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(1, 1)
polygon_0.GetPointIds().SetId(2, 2)

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(3)
polygon_1.GetPointIds().SetId(0, 3)
polygon_1.GetPointIds().SetId(1, 4)
polygon_1.GetPointIds().SetId(2, 5)

polygon_2 = vtkPolygon()
polygon_2.GetPointIds().SetNumberOfIds(3)
polygon_2.GetPointIds().SetId(0, 6)
polygon_2.GetPointIds().SetId(1, 7)
polygon_2.GetPointIds().SetId(2, 8)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())
u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())
u_grid.InsertNextCell(polygon_2.GetCellType(), polygon_2.GetPointIds())

output_path = '.'

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName(output_path + '/initial_crack.vtu')
writer.Write()


