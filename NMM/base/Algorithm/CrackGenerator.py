from NMM.base.Algorithm.AlgorithmInterface import AbstractInterface
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class CrackGenerator(AbstractInterface):
    def __init__(self, crack_grid: VtkGrid, element_grid: VtkGrid, output: VtkGrid):
        super(CrackGenerator, self).__init__()
        self.__crack_grid = crack_grid
        self.__element_grid = element_grid
        self.__output_grid = output

    def update(self, grid_type: str):
        if 'crack_surface' == grid_type:
            pass
        elif 'crack_edge' == grid_type:
            pass
        else:
            raise Exception('Grid type error!!!')
