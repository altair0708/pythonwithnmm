from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkCommonCore import vtkPoints
from NMM.base.VTKBase.test_example import generate_point_grid, generate_polygon, generate_tetrahedron, generate_tetra_polyhedron
from NMM.base.VTKBase.add_attribute.add_point_attribute import AddPointAttribute
from NMM.base.VTKBase.add_attribute.add_cell_attribute import AddCellAttribute
from NMM.base.VTKBase.write_file import write_file


_, _, _, point_grid = generate_tetra_polyhedron()

AddPointAttribute.add_int_array(point_grid, 'point', 1, True)
AddCellAttribute.add_int_array(point_grid, 'cell', 1, True)

print(point_grid.GetNumberOfPoints())
print(point_grid.GetPoint(0))

write_file(point_grid, 're000_00.vtu')

points = vtkPoints()
points.ShallowCopy(point_grid.GetPoints())
points.SetPoint(0, (-1, -1, -1))

print(point_grid.GetNumberOfPoints())
print(point_grid.GetPoint(0))

write_file(point_grid, 're000_01.vtu')
