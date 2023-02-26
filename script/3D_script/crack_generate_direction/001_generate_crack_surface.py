import os
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

points = vtkPoints()
# points.InsertNextPoint((4.5, 4.5, 4.4))
# points.InsertNextPoint((5.5, 4.5, 5.4))
# points.InsertNextPoint((5.5, 5.5, 5.4))
# points.InsertNextPoint((4.5, 5.5, 4.4))

# points.InsertNextPoint((0, 0, 1))
# points.InsertNextPoint((0, 0, -1))
# points.InsertNextPoint((4, 0, -1))
# points.InsertNextPoint((4, 0, 1))
points.InsertNextPoint((-0.5, 0, 0))
points.InsertNextPoint((-0.01, 0, 0.49))
points.InsertNextPoint((-0.01, 1, 0.49))
points.InsertNextPoint((-0.5, 1, 0))

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(4)
polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(1, 1)
polygon_0.GetPointIds().SetId(2, 2)
polygon_0.GetPointIds().SetId(3, 3)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())

output_path = './mesh'

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName(output_path + '/initial_crack.vtu')
writer.Write()


