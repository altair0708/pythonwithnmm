from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm


class CoverRefresher(AbstractAlgorithm):
    def __init__(self, matrix_solver, mathematics_point, new_cover):
        self.__matrix_solver = matrix_solver
        self.__mathematics_point = mathematics_point
        self.__new_cover = new_cover

    def update(self, *args, **kwargs):
        pass
