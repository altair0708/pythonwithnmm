import os
import sys
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
sys.path.append(os.path.abspath('../NMM/preprocess_3D'))

points = vtkPoints()

points.InsertNextPoint((0, 2, 9.9))
points.InsertNextPoint((0, 3, 9.9))
points.InsertNextPoint((4, 3, 9.9))
points.InsertNextPoint((4, 2, 9.9))

points.InsertNextPoint((0, 17, 10.1))
points.InsertNextPoint((0, 18, 10.1))
points.InsertNextPoint((4, 18, 10.1))
points.InsertNextPoint((4, 17, 10.1))

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(4)
polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(1, 1)
polygon_0.GetPointIds().SetId(2, 2)
polygon_0.GetPointIds().SetId(3, 3)

polygon_1 = vtkPolygon()
polygon_1.GetPointIds().SetNumberOfIds(4)
polygon_1.GetPointIds().SetId(0, 4)
polygon_1.GetPointIds().SetId(1, 5)
polygon_1.GetPointIds().SetId(2, 6)
polygon_1.GetPointIds().SetId(3, 7)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())
u_grid.InsertNextCell(polygon_1.GetCellType(), polygon_1.GetPointIds())

output_path = './mesh/'
output_path = os.path.abspath(output_path)

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName(output_path + '/initial_crack.vtu')
writer.Write()


