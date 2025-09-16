from NMM.base.VTKBase.find_close_cell import find_close_cell
from NMM.base.VTKBase.load_a_grid import load_a_grid
from NMM.base.VTKBase.write_file import write_file
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkVertex
from vtkmodules.vtkCommonCore import vtkPoints

u_grid = load_a_grid('geometric_tetrahedron.vtu')

point_coord = (2, 0, 4)

element_id = find_close_cell(vtk_model=u_grid, point_coord=point_coord)
print(element_id)

points = vtkPoints()
points.InsertNextPoint(point_coord)

vertex = vtkVertex()
vertex.GetPointIds().SetId(0, 0)

point_grid = vtkUnstructuredGrid()
point_grid.InsertNextCell(vertex.GetCellType(), vertex.GetPointIds())
point_grid.SetPoints(points)

write_file(point_grid, 'point_grid.vtu')


