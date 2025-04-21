import numpy as np
from typing import List
from NMM.base.Property.Implement import PropertyList
from NMM.base.Part.Part import Part
from NMM.preprocess_3D.Part.ElementList.ElementBase import ElementBase
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve, cg, lsmr, lsqr, gmres, aslinearoperator


class MatrixSolver(Part):
    def __init__(self):
        super(MatrixSolver, self).__init__()

        self.name = 'matrix_solver'
        self.__cover_number = 0

    @property
    def cover_number(self):
        return self.__cover_number

    @cover_number.setter
    def cover_number(self, value):
        self.__cover_number = value
