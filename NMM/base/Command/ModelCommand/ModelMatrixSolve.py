from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.ElementMatrixAssembler.ElementMatrixAssembler import ElementMatrixAssembler
from NMM.base.Algorithm.CoverRefresher import CoverRefresher
from NMM.base.CacheBase import entrance_cache
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.base.Property.Implement.VtkGrid import VtkGrid


# TODO: solver for matrix
class ModelMatrixSolve(AbstractCommand):
    def __init__(self):
        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')
        self.__element_list = entrance_cache.get_item('matrix_element_Part')
        self.__global_variable = entrance_cache.get_item('global_variable_Part')

        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        total_step = self.__global_variable.get_variable('total_step')

        for each_step in range(total_step):

            self.__matrix_solver.recent_step = each_step

            element_assemble = ElementMatrixAssembler(self.__element_list)
            element_assemble.update()

            cover_number = self.__mathematics_point.get_cell_number() + (self.__new_cover.get_cell_number() / 2)
            self.__matrix_solver.cover_number = cover_number

            for each_element in self.__element_list:
                self.__matrix_solver.add_element_matrix(each_element)
                self.__matrix_solver.add_force_vector(each_element)

            self.__matrix_solver.solve_conjugate_gradient()

            cover_fresher = CoverRefresher(self.__matrix_solver, self.__mathematics_point, self.__new_cover)
            cover_fresher.update()
