from vtkmodules.vtkCommonDataModel import vtkGenericCell, vtkUnstructuredGrid, vtkPolyhedron, vtkPolygon, vtkLine, vtkVertex, vtkTetra
from vtkmodules.vtkCommonCore import vtkPoints, vtkIdList, reference
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter
from NMM.base.ModifyVtkCellNew import insert_a_grid
from NMM.base.VTKBase.Implement.VTKBase import VTKBase

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

# cell = vtkTetra()
# cell.GetPointIds().DeepCopy(point_id)
# u_grid = vtkUnstructuredGrid()
# u_grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
# u_grid.SetPoints(points)

# a = reference(2)
# b = reference([0, 0, 0, 0])
# u_grid.GetCellPoints(0, a, b)
# print(a)
# print(b)

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

new_grid = VTKBase.get_a_vtk_cell_grid(u_grid, 0)
print(VTKBase.insert_unique_point_grid(new_grid, (1, 1, 1)))
print(VTKBase.insert_unique_point_grid(new_grid, (1.01, 1, 1)))

writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re003_vtk_generic_cell.vtu')
writer.SetInputData(new_grid)
writer.Write()
