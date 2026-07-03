from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import entrance_cache
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import generate_total_force, generate_fixed_matrix, generate_initial_matrix, generate_mass_matrix, generate_initial_stress
import numpy as np


class CompleteElementIterator(AbstractAlgorithm):
    def __init__(self):
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__boundary_condition = entrance_cache.get_item('boundary_condition_VtkGrid')

    def update(self, element: ElementBase, *args, **kwargs):
        manifold_element: VtkGrid = self.__manifold_element
        mathematics_point: VtkGrid = self.__mathematics_point
        boundary_condition: VtkGrid = self.__boundary_condition

        element_id = element.get_property('cell_id').value

        temp_vector = PropertyVector(np.array(manifold_element.get_cell_attribute('initial_strain_total', element_id), dtype=np.float64).reshape((6, 1)))
        temp_vector.set_name('initial_strain_total')
        element.add_property(temp_vector)

        patch_id = element.get_property('math_cover_id').value

        patch_displacement_velocity = [mathematics_point.get_cell_attribute('math_cover_velocity', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_velocity)
        temp_property.set_name('math_cover_velocity')
        element.add_property(temp_property)

        fixed_point_id = element.get_property('fixed_point_id').value

        fixed_point_displacement_total = [boundary_condition.get_cell_attribute('special_point_displacement_total', i) for i in fixed_point_id]
        temp_property = PropertyList(fixed_point_displacement_total)
        temp_property.set_name('fixed_point_displacement_total')
        element.add_property(temp_property)

        generate_initial_stress(element)
        generate_initial_matrix(element)
        generate_fixed_matrix(element)
        generate_mass_matrix(element)

        generate_total_force(element)

