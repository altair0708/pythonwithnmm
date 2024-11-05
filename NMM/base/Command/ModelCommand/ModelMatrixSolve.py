from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.MatrixAssembler import MatrixAssembler
from NMM.base.Algorithm.CoverRefresher import CoverRefresher
from NMM.base.CacheBase import entrance_cache
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver


# TODO: solver for matrix
class ModelMatrixSolve(AbstractCommand):
    def __init__(self):
        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')
        self.__element_list = entrance_cache.get_item('matrix_element_Part')

        self.__mathematics_point = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_element = entrance_cache.get_item('new_element_VtkGrid')
        self.__new_cover = entrance_cache.get_item('new_cover_VtkGrid')

    def execute(self):
        for each_step in range(self.__matrix_solver.total_step):

            self.__matrix_solver.recent_step = each_step

            matrix_assembler = MatrixAssembler(self.__element_list, self.__matrix_solver)
            matrix_assembler.update()

            self.__matrix_solver.solve_conjugate_gradient()

            cover_fresher = CoverRefresher(self.__matrix_solver, self.__mathematics_point, self.__new_cover)
            cover_fresher.update()
