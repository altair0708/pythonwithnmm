from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkTetra, vtkPlane
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet

tetra_1 = vtkTetra()
tetra_1.GetPointIds().SetId(0, 0)
tetra_1.GetPointIds().SetId(1, 1)
tetra_1.GetPointIds().SetId(2, 2)
tetra_1.GetPointIds().SetId(3, 3)

points = vtkPoints()
points.InsertNextPoint((0, 0, 0))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((0, 1, 0))
points.InsertNextPoint((0, 0, 1))

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(tetra_1.GetCellType(), tetra_1.GetPointIds())
u_grid.SetPoints(points)

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName('re004_1.vtu')
writer.Write()
del writer

plane = vtkPlane()
plane.SetOrigin(0.5, 0, 0)
plane.SetNormal(1, 0.8, 0)

clipper = vtkClipDataSet()
clipper.SetInputData(u_grid)
clipper.SetClipFunction(plane)
clipper.Update()
result: vtkUnstructuredGrid = clipper.GetOutput()

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(result)
writer.SetFileName('re004_2.vtu')
writer.Write()


