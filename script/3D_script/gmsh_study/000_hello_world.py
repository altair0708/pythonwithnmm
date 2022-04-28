import pygmsh
import meshio
from vtkmodules.vtkCommonDataModel import vtkTetra, vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOXML import vtkXMLDataSetWriter

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)

tetra = vtkTetra()
[tetra.GetPointIds().SetId(i, i) for i in range(4)]

polyData = vtkUnstructuredGrid()
polyData.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
polyData.SetPoints(points)

writer = vtkXMLDataSetWriter()
writer.SetFileName('test.vtu')
writer.SetInputData(polyData)
writer.Write()

mesh = meshio.read('test.vtu')
print(mesh)

