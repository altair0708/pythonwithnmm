from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.base.Algorithm.ElementCreator.ElementDirector import ElementDirector
from NMM.base.Algorithm.ElementCreator.CompleteElementBuilder import CompleteElementBuilder


builder = NmmDatabaseBuilder()
nmm_database = builder.build('test.db', False)


def test_complete_element_builder():
    mathematics_point = VtkGrid('mathematics_point', 'mathematics_point.vtu')
    manifold_element = VtkGrid('manifold_element', 'manifold_element.vtu')
    boundary_condition = VtkGrid('boundary_condition', 'boundary_condition.vtu')
    material_parameter = PropertyMap.generate_from_toml('material_parameter.toml')

    director = ElementDirector(mathematics_point, manifold_element, boundary_condition, material_parameter)
    complete_builder = CompleteElementBuilder()

    director.builder = complete_builder
    director.build_matrix_element(549)

    new_element = complete_builder.get_element()

    print(new_element.get_property('material_parameter')['material_name'])
