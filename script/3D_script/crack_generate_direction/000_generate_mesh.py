from vtkmodules.vtkCommonDataModel import vtkTetra, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
import os

points = vtkPoints()
points.InsertNextPoint((0, 0, 0))
points.InsertNextPoint((0, 1, 0))
points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((-1, 0, 0))

element_1 = vtkTetra()
element_1.GetPointIds().SetId(0, 0)
element_1.GetPointIds().SetId(1, 1)
element_1.GetPointIds().SetId(2, 2)
element_1.GetPointIds().SetId(3, 3)

element_2 = vtkTetra()
element_2.GetPointIds().SetId(0, 0)
element_2.GetPointIds().SetId(1, 1)
element_2.GetPointIds().SetId(2, 2)
element_2.GetPointIds().SetId(3, 4)

u_grid = vtkUnstructuredGrid()
u_grid.SetPoints(points)
u_grid.InsertNextCell(element_1.GetCellType(), element_1.GetPointIds())
u_grid.InsertNextCell(element_2.GetCellType(), element_2.GetPointIds())

try:
    os.mkdir('mesh')
except FileExistsError:
    pass

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('./mesh/gmsh_file.vtu')
writer.SetInputData(u_grid)
writer.Write()



