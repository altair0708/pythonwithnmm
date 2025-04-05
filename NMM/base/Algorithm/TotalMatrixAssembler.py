from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.preprocess_3D.Part.ElementList.MatrixElement.MatrixElementBase import MatrixElementBase
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from typing import List
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve, cg, lsmr, lsqr, gmres, aslinearoperator
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase


# TODO: Assemble total Matrix
class TotalMatrixAssembler(AbstractAlgorithm):
    def __init__(self, cover_number: int):
        self.__cover_number = cover_number
        self.__stiff_matrix = coo_matrix((3 * self.__cover_number, 3 * self.__cover_number), dtype=np.float64)
        self.__force_vector = np.zeros(3 * self.__cover_number, dtype=np.float64)

        self.__total_row = np.array([[]], dtype=np.int32)
        self.__total_column = np.array([[]], dtype=np.int32)
        self.__total_value = np.array([[]], dtype=np.float64)

    def update(self, *args, **kwargs):
        self.__total_row = self.__total_row.astype('int32')
        self.__total_column = self.__total_column.astype('int32')
        self.__stiff_matrix = coo_matrix((self.__total_value[0], (self.__total_row[0], self.__total_column[0])),
                                         dtype=np.float64)
        self.__stiff_matrix = self.__stiff_matrix.tocsc()

        assert self.__stiff_matrix.shape == (3 * self.__cover_number, 3 * self.__cover_number)
        assert self.__force_vector.shape == (3 * self.__cover_number, )

        temp_stiff_matrix = self.__stiff_matrix
        temp_force_vector = self.__force_vector
        return temp_stiff_matrix, temp_force_vector

    def add_element_matrix(self, element: ElementBase):
        temp_list = [[3 * x, 3 * x + 1, 3 * x + 2] for x in element.get_property('math_cover_id').value]
        temp_array = np.array(temp_list, dtype=np.int32).reshape((1, -1))[0]
        row, column = np.meshgrid(temp_array, temp_array)
        row = row.reshape((1, -1))
        column = column.reshape((1, -1))
        value = np.array(element.get_property('total_matrix').value, dtype=np.float64).reshape((1, -1))
        self.__total_row = np.c_[self.__total_row, row]
        self.__total_column = np.c_[self.__total_column, column]
        self.__total_value = np.c_[self.__total_value, value]

    def add_force_vector(self, element: ElementBase):
        # force vector
        temp_vector = np.zeros(3 * self.__cover_number, dtype=np.float64)
        for step, each_location in enumerate(element.get_property('math_cover_id').value):
            total_force = element.get_property('total_force').value
            temp_vector[3 * each_location] = total_force[3 * step][0]
            temp_vector[3 * each_location + 1] = total_force[3 * step + 1][0]
            temp_vector[3 * each_location + 2] = total_force[3 * step + 2][0]
        self.__force_vector = self.__force_vector + temp_vector

