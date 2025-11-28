from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import entrance_cache
from NMM.base.Algorithm.ElementMatrixAssembler.CalculateMatrix import elastic_matrix
from NMM.base.Algorithm.ElementCracker.Criterion.AverageStressCalculator import AverageStressCalculator
from NMM.base.Property.Implement.PropertyTensor import PropertyTensor
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from abc import ABC, abstractmethod
import numpy as np


class AbstractCriterion(AbstractAlgorithm, ABC):
    def __init__(self, element_id: int = -1, manifold_element: VtkGrid = None, material_parameter: PropertyMap = None):
        super(AbstractCriterion, self).__init__()
        self._element_id = element_id
        self._coordinate = (0, 0, 0)
        if manifold_element is None:
            self._manifold_element = entrance_cache.get_item('manifold_element_VtkGrid')
        else:
            self._manifold_element = manifold_element

        if material_parameter is None:
            self._material_parameter = entrance_cache.get_item('material_parameter_PropertyMap')
        else:
            self._material_parameter = material_parameter

        # result
        self._crack_flag = False
        self._normal = (0, 0, 0)

        # element info
        self._stress = None
        self._stress_tensor = None
        self._strain = None
        self._strain_tensor = None

    def set_element_id(self, element_id: int):
        self._element_id = element_id

    def set_point_coordinate(self, coordinate):
        self._coordinate = coordinate

    def calculate_elastic_stress(self, coordinate=None):
        manifold_element = self._manifold_element
        element_id = self._element_id
        if coordinate is None:
            coordinate = self._coordinate
        material_parameter = self._material_parameter

        strain_algorithm = AverageStressCalculator(coordinate)
        strain_algorithm.update()
        strain = strain_algorithm.strain
        # strain = manifold_element.get_cell_attribute('initial_strain_total', element_id)
        # strain = np.array(strain).reshape((6, 1))

        self._strain = strain
        strain_tensor = PropertyTensor(strain)
        self._strain_tensor = strain_tensor

        material_id = int(manifold_element.get_cell_attribute('material_id', element_id)[0])
        material_parameter = material_parameter[str(material_id)]

        temp_E = material_parameter['elastic_modulus']
        temp_mu = material_parameter['poisson_ratio']
        temp_elastic_matrix = elastic_matrix(temp_E, temp_mu)

        stress = np.dot(temp_elastic_matrix, strain)
        assert stress.shape == (6, 1)

        self._stress = stress
        result = PropertyTensor(stress)
        self._stress_tensor = result
        return result

    @property
    def material_id(self):
        result = self._manifold_element.get_attribute('material_id', self._element_id)[0]
        return result

    @property
    def crack_flag(self):
        return self._crack_flag

    @property
    def normal(self):
        return self._normal

    @property
    def stress(self):
        return self._stress

    @property
    def stress_tensor(self) -> PropertyTensor:
        return self._stress_tensor

    @property
    def strain(self):
        return self._strain

    @property
    def strain_tensor(self) -> PropertyTensor:
        return self._strain_tensor
