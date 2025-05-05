from NMM.base.Algorithm.ElementCracker.Criterion.MaximumTensileStress import MaximumTensileStress
from NMM.base.Algorithm.ElementCracker.CrackPointCounter import CrackPointCounter
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.base.Property.Implement.PropertyTensor import PropertyTensor
from NMM.preprocess_3D.Part.NmmDatabase.NmmDatabaseBuilder import NmmDatabaseBuilder
import numpy as np
import shutil

shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example002/geometry/element_surface.vtu', 'element_surface.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example002/geometry/crack_edge.vtu', 'crack_edge.vtu')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example002/geometry/database.db', 'database.db')

builder = NmmDatabaseBuilder()
nmm_database = builder.build('database.db', False)


def test_criterion():
    manifold_element = VtkGrid('manifold_element', 'manifold_element_00009.vtu')
    material_parameter = PropertyMap.generate_from_toml('material_parameter.toml')
    criterion = MaximumTensileStress(element_id=0, manifold_element=manifold_element, material_parameter=material_parameter)
    criterion.update()
    tensor = criterion.stress_tensor

    print()
    print(tensor.max_component_vector[0])
    print(tensor.max_component_vector[1])
    print(tensor.middle_component_vector[0])
    print(tensor.middle_component_vector[1])
    print(tensor.min_component_vector[0])
    print(tensor.min_component_vector[1])


def test_count_crack_point():
    element_surface = VtkGrid('element_surface', 'element_surface.vtu')
    crack_edge = VtkGrid('crack_edge', 'crack_edge.vtu')
    counter = CrackPointCounter(21, element_surface, crack_edge)
    counter.update()

    print(len(counter.point_list))
    print(counter.normal)
    print(counter.origin)
    print(counter.point_list)


def test_property_tensor():
    stress = np.array([[1], [2], [3], [0], [0], [0]])
    tensor = PropertyTensor(stress)
    print(tensor.max_component_vector)
    print(tensor.middle_component_vector)
    print(tensor.min_component_vector)

