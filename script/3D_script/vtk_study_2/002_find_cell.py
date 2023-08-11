from tests3D.object.tetra_polyhedron import generate_tetrahedron
from vtkmodules.vtkCommonDataModel import vtkGenericCell, VTK_TETRA
from vtkmodules.vtkCommonCore import reference, vtkIdList
from vtkmodules.vtkIOXML import vtkXMLUnstructuredGridWriter

_, test_grid = generate_tetrahedron()
points = test_grid.GetPoints()
points.InsertNextPoint((1, 1, 1))

cell_id = vtkIdList()
for i in range(4):
    # cell_id.InsertNextId(i + 1)
    cell_id.InsertNextId(i + 1)
test_grid.InsertNextCell(VTK_TETRA, cell_id)
print(test_grid.GetNumberOfCells())

# There is a bug that when temp_id = 0, it will be mistake assign as -1.
generic_cell = vtkGenericCell()
sub_id = reference(0)
temp_id = test_grid.FindCell([0.9, 0.9, 0.9], generic_cell, 0, 0.00001, sub_id, [0, 0, 0],
                             [0, 0, 0, 0])
print(temp_id)
writer = vtkXMLUnstructuredGridWriter()
writer.SetFileName('re002_0.vtu')
writer.SetInputData(test_grid)
writer.Write()
