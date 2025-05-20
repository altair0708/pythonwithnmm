import os
import sys
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkCommonDataModel import vtkCell, vtkHexahedron, vtkUnstructuredGrid, vtkPolygon, vtkCell3D
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
sys.path.append(os.path.abspath('../NMM/preprocess_3D'))

points = vtkPoints()
# points.InsertNextPoint((0, 0, 10))
# points.InsertNextPoint((8, 0, 10))
# points.InsertNextPoint((8, 4, 10))
# points.InsertNextPoint((0, 4, 10))

# 90 degree
points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((0, 0, -1))
points.InsertNextPoint((6, 0, -1))
points.InsertNextPoint((6, 0, 1))

# 63.5 degree
# points.InsertNextPoint((0, -0.5, 1))
# points.InsertNextPoint((0, 0.5, -1))
# points.InsertNextPoint((4, 0.5, -1))
# points.InsertNextPoint((4, -0.5, 1))

# 60 degree
# points.InsertNextPoint((0, -0.5, 1))
# points.InsertNextPoint((0, 0.577, -1))
# points.InsertNextPoint((4, 0.577, -1))
# points.InsertNextPoint((4, -0.5, 1))

# 45 degree
# points.InsertNextPoint((0, -1, 1))
# points.InsertNextPoint((0, 1, -1))
# points.InsertNextPoint((4, 1, -1))
# points.InsertNextPoint((4, -1, 1))

# L block
# points.InsertNextPoint((24.9, 0, 24.9))
# points.InsertNextPoint((26, 0, 24.9))
# points.InsertNextPoint((26, 4, 24.9))
# points.InsertNextPoint((24.9, 4, 24.9))

# pull
# points.InsertNextPoint((0, 0, 14))
# points.InsertNextPoint((0.5, 0, 14))
# points.InsertNextPoint((0.5, 4, 14))
# points.InsertNextPoint((0, 4, 14))

polygon_0 = vtkPolygon()
polygon_0.GetPointIds().SetNumberOfIds(4)
polygon_0.GetPointIds().SetId(0, 0)
polygon_0.GetPointIds().SetId(1, 1)
polygon_0.GetPointIds().SetId(2, 2)
polygon_0.GetPointIds().SetId(3, 3)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(polygon_0.GetCellType(), polygon_0.GetPointIds())

output_path = './mesh/'
output_path = os.path.abspath(output_path)

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName(output_path + '/initial_crack.vtu')
writer.Write()


