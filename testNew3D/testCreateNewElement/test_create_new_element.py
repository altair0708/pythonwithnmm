from NMM.preprocess_3D.Part.ElementList.MatrixElement.MatrixElementFactory import MatrixElementFactory
from NMM.preprocess_3D.Part.ElementList.MatrixElement.MatrixElementBase import MatrixElementBase
from NMM.base.Property.Implement.VtkGrid import VtkGrid


def test_create_new_element():
    vtk_grid = VtkGrid('test_1', 'geometric_tetrahedron.vtu')
    vtk_grid.add_attribute('cell_id', attribute_toml='global_variable.toml')
    vtk_grid.add_attribute('point_id', attribute_toml='global_variable.toml')
    vtk_grid.add_attribute('real', attribute_toml='global_variable.toml')
    vtk_grid.add_attribute('cracked', attribute_toml='global_variable.toml')
    vtk_grid.add_attribute('math_cover_coordinate', attribute_toml='global_variable.toml')

    assert vtk_grid.get_cell_attribute_number() == 4

    element_factory = MatrixElementFactory()
    new_element = element_factory.build(111, vtk_grid, attribute_toml='global_variable.toml')
    print(new_element[0].get_property('cell_id').value)
