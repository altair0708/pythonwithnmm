from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Algorithm.MatrixAssembler import MatrixAssembler
from NMM.base.CacheBase.EntranceCache import entrance_cache


class ModelAssembleTotalMatrix(AbstractCommand):
    def __init__(self):
        self.__matrix_element = entrance_cache.get_item('matrix_element_Part')
        self.__matrix_solver = entrance_cache.get_item('matrix_solver_Part')

    def execute(self):
        assembler = MatrixAssembler(self.__matrix_element, self.__matrix_solver)
        assembler.update()

