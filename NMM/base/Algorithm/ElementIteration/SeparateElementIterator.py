from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import entrance_cache
from NMM.base.Property.Implement import PropertyInteger, PropertyList, PropertyMap, PropertyVector
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from NMM.base.Algorithm.ElementMatrixAssembler.SeparateElementMatrixAssembler import generate_total_force, generate_initial_matrix, generate_mass_matrix, generate_initial_stress
import numpy as np


class SeparateElementIterator(AbstractAlgorithm):
    def __init__(self):
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')

    def update(self, element: ElementBase, *args, **kwargs):
        new_element: VtkGrid = self.__new_element
        new_cover: VtkGrid = self.__new_cover

        element_id = element.get_property('cell_id').value

        temp_vector = PropertyVector(np.array(new_element.get_cell_attribute('initial_strain_total', element_id), dtype=np.float64).reshape((6, 1)))
        temp_vector.set_name('initial_strain_total')
        element.add_property(temp_vector)

        patch_id = element.get_property('new_cover_id').value

        patch_displacement_velocity = [new_cover.get_cell_attribute('math_cover_velocity', i) for i in patch_id]
        temp_property = PropertyList(patch_displacement_velocity)
        temp_property.set_name('math_cover_velocity')
        element.add_property(temp_property)

        generate_initial_stress(element)
        generate_initial_matrix(element)
        generate_mass_matrix(element)

        generate_total_force(element)

