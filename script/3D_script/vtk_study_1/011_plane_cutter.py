from tests3D.object.tetra_polyhedron import generate_tetra_polyhedron
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkPlane, vtkTetra, vtkPolyData, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkFiltersCore import vtkCutter, vtkPlaneCutter
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter, vtkXMLUnstructuredGridWriter

points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(0, 0, 1)

tetra = vtkTetra()
tetra.GetPointIds().SetId(0, 0)
tetra.GetPointIds().SetId(1, 1)
tetra.GetPointIds().SetId(2, 2)
tetra.GetPointIds().SetId(3, 3)

tetra1, id_list, points_1 = generate_tetra_polyhedron()
u_grid = vtkUnstructuredGrid()
# u_grid.InsertNextCell(tetra.GetCellType(), tetra.GetPointIds())
u_grid.InsertNextCell(VTK_POLYHEDRON, id_list)
u_grid.SetPoints(points_1)

plane = vtkPlane()
plane.SetOrigin(0.5, 0, 0)
plane.SetNormal(1, 0, 0)

cutter = vtkCutter()
cutter.SetInputData(u_grid)
cutter.SetCutFunction(plane)
cutter.Update()
print(cutter.GetOutput().GetNumberOfCells())

writer = vtkXMLPolyDataWriter()
writer.SetInputConnection(cutter.GetOutputPort())
writer.SetFileName('re011_0.vtp')
writer.Write()

writer = vtkXMLUnstructuredGridWriter()
writer.SetInputData(u_grid)
writer.SetFileName('re011_1.vtu')
writer.Write()

