from NMM.base.VTKBase import new_a_grid, get_attribute
from NMM.base.VTKBase.get_a_vtk_cell_grid_1 import get_a_vtk_cell_grid
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.VTKBase.subdivide_polygon_edges_0 import subdivide_polygon_edges_to_lines
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache


class GenerateCrackTip(AbstractAlgorithm):
    def __init__(self, initial_crack, crack_tip, crack_propagation):
        self.__initial_crack = initial_crack
        self.__crack_tip = crack_tip
        self.__crack_propagation = crack_propagation

    def update(self, *args, **kwargs):
        initial_crack = self.__initial_crack.value
        try:
            subdivide = global_variable_cache.get_item('crack_tip')
        except AssertionError:
            print('Message: crack tip set default.')
            subdivide = 0.5
        crack_tip = subdivide_polygon_edges_to_lines(initial_crack, subdivide)
        self.__crack_tip.value = crack_tip

        new_grid = new_a_grid()
        for each_cell in range(initial_crack.GetNumberOfCells()):
            vtk_cell = get_a_vtk_cell_grid(initial_crack, each_cell)
            new_grid = insert_a_vtk_cell(vtk_cell, new_grid)
        self.__crack_propagation.value = new_grid
