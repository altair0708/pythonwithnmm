from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Algorithm.ElementMatrixAssembler.CompleteElementMatrixAssembler import *
from typing import List
import numpy as np


def generate_elastic_matrix(element: ElementBase):
    temp_E = float(element.get_property('material_parameter')['elastic_modulus']) * 0.01
    temp_mu = float(element.get_property('material_parameter')['poisson_ratio'])

    elastic_matrix = temp_E / ((1 + temp_mu) * (1 - 2 * temp_mu)) * \
                     np.matrix([[1 - temp_mu, temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, 1 - temp_mu, temp_mu, 0, 0, 0],
                                [temp_mu, temp_mu, 1 - temp_mu, 0, 0, 0],
                                [0, 0, 0, (1 - 2 * temp_mu) / 2, 0, 0],
                                [0, 0, 0, 0, (1 - 2 * temp_mu) / 2, 0],
                                [0, 0, 0, 0, 0, (1 - 2 * temp_mu) / 2]], dtype=np.float64)

    temp_matrix = PropertyMatrix(elastic_matrix)
    temp_matrix.set_name('elastic_matrix')
    element.add_property(temp_matrix)


class CrackTipAssembler(AbstractAlgorithm):
    def __init__(self, element: ElementBase):
        self.__element = element

    def update(self, *args, **kwargs):
        generate_delta_matrix(self.__element)
        generate_B_shape_matrix(self.__element)
        generate_elastic_matrix(self.__element)
        generate_stiff_matrix(self.__element)
        generate_initial_strain_increment(self.__element)
        generate_initial_strain_total(self.__element)
        generate_initial_stress(self.__element)
        generate_initial_velocity(self.__element)
        generate_initial_matrix(self.__element)
        generate_loading_matrix(self.__element)
        generate_body_matrix(self.__element)
        generate_mass_matrix(self.__element)
        generate_fixed_matrix(self.__element)
        generate_total_matrix(self.__element)
        generate_total_force(self.__element)
