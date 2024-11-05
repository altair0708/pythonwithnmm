from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase import find_close_cell, debug_write_file, load_a_grid
from NMM.base.CacheBase import relationship_cache


class SpecialPointAdder(AbstractAlgorithm):
    def __init__(self, manifold_element: VtkGrid, special_point: VtkGrid):
        self.__manifold_element = manifold_element
        self.__special_point = special_point

    def update(self):
        # debug_write_file(self.__manifold_element.value, 'manifold_element.vtu')
        # manifold_element = load_a_grid('D:\\science\\NMM\\python-NMM\\debug\\manifold_element.vtu')
        # debug_write_file(self.__special_point.value, 'special_point.vtu')
        for special_point_id, each_point in enumerate(self.__special_point):
            adjacent_cell_id = find_close_cell(each_point, self.__manifold_element.value)
            if adjacent_cell_id >= 0:
                relationship_cache.add_item('element', adjacent_cell_id, 'specialpoint', special_point_id)

