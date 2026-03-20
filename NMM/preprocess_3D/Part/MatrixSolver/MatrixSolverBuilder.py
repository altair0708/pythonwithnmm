from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.Property.Implement import PropertyList, PropertyMatrix
from NMM.preprocess_3D.Part import ElementListBuilder
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache


class MatrixSolverBuilder(AbstractConstructor):
    def build(self):
        matrix_solver = MatrixSolver()

        matrix_element_list = PropertyList([])
        matrix_element_list.set_name('element_list')
        matrix_solver.add_property(matrix_element_list)

        try:
            if global_variable_cache.get_item('contact_calculate') == 1:
                temp_list = PropertyList([])
                temp_list.set_name('contact_list')
                matrix_solver.add_property(temp_list)
        except AssertionError:
            pass

        displacement_vector = PropertyMatrix()
        displacement_vector.set_name('displacement_vector')
        matrix_solver.add_property(displacement_vector)

        return matrix_solver
