from vtkmodules.vtkCommonDataModel import vtkGenericCell, vtkUnstructuredGrid, vtkPolyhedron, vtkPolygon, vtkLine, vtkVertex, vtkTetra, VTK_POLYHEDRON
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from vtkmodules.vtkCommonCore import vtkVersion
from vtkmodules.vtkFiltersCore import vtkRemoveUnusedPoints
from NMM.base.VTKBase import clip_a_element

points = vtkPoints()
points.InsertNextPoint((-1, -1, -1))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((0, 1, 0))
points.InsertNextPoint((0, 0, 1))
points.InsertNextPoint((2, 0, 0))
points.InsertNextPoint((0, 2, 0))
points.InsertNextPoint((0, 0, 2))

point_id = vtkIdList()
point_id.InsertNextId(0)
point_id.InsertNextId(1)
point_id.InsertNextId(2)
point_id.InsertNextId(3)

faces = vtkIdList()
face_id = [4,
           3, 0, 2, 1,
           3, 0, 1, 3,
           3, 0, 3, 2,
           3, 1, 2, 3]
[faces.InsertNextId(x) for x in face_id]

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(VTK_POLYHEDRON, faces)
u_grid.SetPoints(points)

cell = vtkTetra()
cell.GetPointIds().DeepCopy(point_id)
u_grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())

print(u_grid.GetNumberOfCells())
print(u_grid.GetNumberOfPoints())
cleaner = vtkRemoveUnusedPoints()
cleaner.SetInputData(u_grid)
cleaner.Update()
u_grid = cleaner.GetOutput()
print(u_grid.GetNumberOfCells())
print(u_grid.GetNumberOfPoints())

# writer = vtkXMLUnstructuredGridWriter()
# writer.SetFileName('re008_vtk_polyhedron.vtu')
# writer.SetInputData(new_grid)
# writer.Write()
