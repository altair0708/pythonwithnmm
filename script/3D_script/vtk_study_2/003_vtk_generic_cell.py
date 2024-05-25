from vtkmodules.vtkCommonDataModel import vtkGenericCell, vtkUnstructuredGrid, vtkPolyhedron, vtkPolygon, vtkLine, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.ModifyVtkCell import insert_a_grid

points = vtkPoints()
points.InsertNextPoint((-1, -1, -1))
points.InsertNextPoint((1, 0, 0))
points.InsertNextPoint((0, 1, 0))
points.InsertNextPoint((0, 0, 1))

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

cell = vtkGenericCell()
cell.SetCellType(42)  # polyhedron

u_grid = vtkUnstructuredGrid()
u_grid.InsertNextCell(cell.GetCellType(), faces)
u_grid.SetPoints(points)

# Initialize a polyhedron
# cell = vtkPolyhedron()
# cell.GetPoints().InsertNextPoint((0, 0, 0))
# cell.GetPoints().InsertNextPoint((1, 0, 0))
# cell.GetPoints().InsertNextPoint((0, 1, 0))
# cell.GetPoints().InsertNextPoint((0, 0, 1))
# cell.GetPointIds().InsertNextId(0)
# cell.GetPointIds().InsertNextId(1)
# cell.GetPointIds().InsertNextId(2)
# cell.GetPointIds().InsertNextId(3)
# cell.SetFaces(face_id)
# cell.Initialize()

new_grid = vtkUnstructuredGrid()
insert_a_grid(new_grid, u_grid)
print(new_grid.GetNumberOfCells())
print(new_grid.GetNumberOfPoints())

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('003_vtk_generic_cell.vtu')
writer.SetInputData(new_grid)
writer.Write()
