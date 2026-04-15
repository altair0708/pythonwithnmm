import numpy as np
from scipy.sparse.linalg import cg, spsolve, eigsh
from NMM.base.Algorithm.Solver.AbstractSolver import AbstractSolver


class NormalSolver(AbstractSolver):
    def update(self, *args, **kwargs):
        total_matrix = self._total_matrix
        total_force = self._total_force

        result = spsolve(total_matrix, total_force)

        self._result = result
