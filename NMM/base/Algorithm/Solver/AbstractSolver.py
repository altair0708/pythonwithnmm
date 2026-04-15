from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from scipy.sparse import coo_matrix
from abc import abstractmethod


class AbstractSolver(AbstractAlgorithm):
    def __init__(self, total_matrix: coo_matrix, total_force):
        self._total_matrix = total_matrix
        self._total_force = total_force

        self._result = None

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @property
    def result(self):
        if self._result is None:
            raise ValueError('result is not ready')
        return self._result

