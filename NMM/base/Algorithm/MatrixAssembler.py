from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.MatrixElement.MatrixElementBase import MatrixElementBase
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from typing import List


# TODO: Assemble total Matrix
class MatrixAssembler(AbstractAlgorithm):
    def __init__(self, matrix_element: List[MatrixElementBase], matrix_solver: MatrixSolver):
        self.__matrix_element = matrix_element
        self.__matrix_solver = matrix_solver

    def update(self, *args, **kwargs):
        for each_element in self.__matrix_element:
            self.__matrix_solver.add_element_matrix(each_element.total_matrix)
            self.__matrix_solver.add_force_vector(each_element.total_force)

