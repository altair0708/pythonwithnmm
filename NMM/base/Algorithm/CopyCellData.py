from NMM.base.VTKBase import copy_cell_data
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm


class CopyCellData(AbstractAlgorithm):
    def __init__(self, origin_grid: VtkGrid, target_grid: VtkGrid):
        super(CopyCellData, self).__init__()
        self.__origin_grid = origin_grid
        self.__target_grid = target_grid

    def update(self, *args, **kwargs):
        attribute_name = [self.__origin_grid.get_cell_attribute_name(i) for i in range(self.__origin_grid.get_cell_attribute_number())]
        for each_attribute_name in attribute_name:
            copy_cell_data(self.__origin_grid.value, self.__target_grid.value, each_attribute_name)

