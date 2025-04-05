from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.VTKBase.test_example import generate_tetra_polyhedron, generate_tetrahedron
from NMM.base.VTKBase import write_file


def test_insert():

    _, _, _, cell_0 = generate_tetra_polyhedron(point_2=(1, 0, 0))
    _, _, _, cell_1 = generate_tetra_polyhedron(point_2=(-1, 0, 0))

    new_grid = insert_a_vtk_cell(cell_0, cell_1)
    print(new_grid.GetNumberOfPoints())

    write_file(new_grid, 'new_grid.vtu')




