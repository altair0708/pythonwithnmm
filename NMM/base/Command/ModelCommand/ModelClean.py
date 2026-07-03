from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.preprocess_3D.Part.MatrixSolver.MatrixSolver import MatrixSolver
from NMM.base.CacheBase import entrance_cache


class ModelClean(AbstractCommand):
    def __init__(self):
        self.__matrix_solver: MatrixSolver = entrance_cache.get_item('matrix_solver_Part')

    def execute(self):
        element_list = self.__matrix_solver.get_property('element_list')
        print(f'Total element number: {len(element_list.value)}')
        element_list.clear()
