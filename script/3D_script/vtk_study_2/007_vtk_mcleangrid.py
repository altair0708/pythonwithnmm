from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmCleanGrid
from tests3D.object.tetra_polyhedron import generate_tetrahedron
from NMM.base.VTKBase import load_a_grid, get_a_vtk_cell_grid

_, test_grid = generate_tetrahedron()

test_grid.GetPoints().InsertNextPoint((5, 5, 5))
test_grid.GetPoints().InsertNextPoint((6, 5, 5))
test_grid.GetPoints().InsertNextPoint((7, 5, 5))
cleaner = vtkmCleanGrid()
cleaner.SetInputData(test_grid)
cleaner.CompactPointsOn()
cleaner.Update()
result: vtkUnstructuredGrid = cleaner.GetOutput()


a: vtkUnstructuredGrid = load_a_grid('re000_0.vtu')
print(a.GetNumberOfPoints())
b: vtkUnstructuredGrid = get_a_vtk_cell_grid(a, 0)
print(b.GetNumberOfCells())
print(b.GetNumberOfPoints())

cleaner = vtkmCleanGrid()
cleaner.SetInputData(b)
cleaner.CompactPointsOn()
cleaner.Update()
c: vtkUnstructuredGrid = cleaner.GetOutput()
print(c.GetCell(0).GetPoints().GetNumberOfPoints())

print(c.GetNumberOfCells())
print(c.GetNumberOfPoints())


