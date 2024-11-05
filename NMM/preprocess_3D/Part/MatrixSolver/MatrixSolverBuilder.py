from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver


# TODO: build matrix solver
class MatrixSolverBuilder(AbstractConstructor):
    def build(self):
        matrix_solver = MatrixSolver()
        return matrix_solver

