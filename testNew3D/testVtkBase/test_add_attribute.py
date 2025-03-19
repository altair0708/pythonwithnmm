from NMM.base.VTKBase.add_attribute.add_attribute_0 import add_attribute
from NMM.base.VTKBase.new_a_grid import new_a_grid
from NMM.base.VTKBase import insert_a_vtk_cell, write_file
from NMM.base.VTKBase.test_example import generate_tetra_polyhedron


def test_add_attribute():
    vtk_model = new_a_grid()

    _, _, _, new_cell = generate_tetra_polyhedron()
    _, _, _, new_cell_0 = generate_tetra_polyhedron(point_1=(1, 1, 1))

    insert_a_vtk_cell(new_cell, vtk_model)
    insert_a_vtk_cell(new_cell_0, vtk_model)

    write_file(vtk_model, 'test_grid_1.vtu')

    add_attribute(vtk_model, 'cell_id', 'global_variable.toml')
    write_file(vtk_model, 'test_grid.vtu')

