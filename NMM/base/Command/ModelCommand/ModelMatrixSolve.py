from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.ElementMatrixAssembler.ElementMatrixAssembler import ElementMatrixAssembler
from NMM.base.Algorithm.CoverRefresher import CoverRefresher
from NMM.base.Algorithm.TotalMatrixAssembler import TotalMatrixAssembler
from NMM.base.CacheBase import entrance_cache
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from scipy.sparse.linalg import cg, spsolve, eigsh


class ModelMatrixSolve(AbstractCommand):
    def __init__(self):
        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')
        self.__global_variable: GlobalVariable = entrance_cache.get_item('global_variable_Part')

    def execute(self):
        element_list = self.__matrix_solver.get_property('element_list')
        cover_number = int(self.__global_variable.get_variable('cover_number')) + \
            int(self.__global_variable.get_variable('new_cover_number') / 2)

        total_assembler = TotalMatrixAssembler(cover_number)
        for each_element in element_list:
            total_assembler.add_element_matrix(each_element)
            total_assembler.add_force_vector(each_element)

        try:
            if global_variable_cache.get_item('contact_calculate') == 1:
                contact_list = self.__matrix_solver.get_property('contact_list')
                for each_element in contact_list:
                    total_assembler.add_contact_element(each_element)
                    total_assembler.add_contact_force(each_element)
        except AssertionError:
            pass

        total_matrix, total_force = total_assembler.update()

        # lam_max = eigsh(total_matrix, 1, which='LM')[0]
        # lam_min = eigsh(total_matrix, 1, which='SM')[0]
        # cond = lam_max / lam_min
        # print(f'condition number: {cond[0]}')
        # if cond[0] > 10000:
        #     result, info = cg(total_matrix, total_force, tol=1e-15, maxiter=1000)
        # else:
        #     result = spsolve(total_matrix, total_force)

        result = spsolve(total_matrix, total_force)

        displacement_vector = self.__matrix_solver.get_property('displacement_vector')
        displacement_vector.value = result

        # clear element list
        element_list.clear()
