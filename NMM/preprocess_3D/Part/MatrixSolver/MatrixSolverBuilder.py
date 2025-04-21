from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement import PropertyList, PropertyMatrix
from NMM.preprocess_3D.Part import ElementListBuilder
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver


# TODO: build matrix solver
class MatrixSolverBuilder(AbstractConstructor):
    def build(self):
        matrix_solver = MatrixSolver()

        matrix_element_list = PropertyList([])
        matrix_element_list.set_name('element_list')
        matrix_solver.add_property(matrix_element_list)

        displacement_vector = PropertyMatrix()
        displacement_vector.set_name('displacement_vector')
        matrix_solver.add_property(displacement_vector)

        return matrix_solver
