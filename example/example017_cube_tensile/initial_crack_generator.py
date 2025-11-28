import os
import sys
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
sys.path.append(os.path.abspath('../NMM/preprocess_3D'))

points = vtkPoints()

points.InsertNextPoint((1, 2, 0.7))
points.InsertNextPoint((2, 1, 1.3))
points.InsertNextPoint((2, -1, 1.3))
points.InsertNextPoint((1, -2, 0.7))
points.InsertNextPoint((-1, -2, -0.5))
points.InsertNextPoint((-2, -1, -1.1))
points.InsertNextPoint((-2, 1, -1.1))
points.InsertNextPoint((-1, 2, -0.5))

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(8)
polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(1, 1)
polygon_0.GetPointIds().SetId(2, 2)
polygon_0.GetPointIds().SetId(3, 3)
polygon_0.GetPointIds().SetId(4, 4)
polygon_0.GetPointIds().SetId(5, 5)
polygon_0.GetPointIds().SetId(6, 6)
polygon_0.GetPointIds().SetId(7, 7)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())

output_path = './mesh/'
output_path = os.path.abspath(output_path)

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName(output_path + '/initial_crack.vtu')
writer.Write()


