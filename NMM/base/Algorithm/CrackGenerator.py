from NMM.base.Algorithm.AlgorithmInterface import AbstractInterface
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.generate_crack_grid.generate_crack_grid import generate_crack_grid
from NMM.base.VTKBase.write_file import write_file


class CrackGenerator(AbstractInterface):
    def __init__(self, crack_grid: VtkGrid, element_grid: VtkGrid, output: VtkGrid):
        super(CrackGenerator, self).__init__()
        self.__crack_grid = crack_grid
        self.__element_grid = element_grid
        self.__output_grid = output

    def update(self, output_name: str):
        initial_crack_grid = self.__crack_grid.value
        manifold_element_grid = self.__element_grid.value

        # Don't return crack_grid, modified by geometry_cache.
        # self.__output_grid.value = generate_crack_grid(initial_crack_grid, manifold_element_grid, output_name)
        generate_crack_grid(initial_crack_grid, manifold_element_grid, output_name)
