from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from NMM.base.VTKBase.get_edge_length import get_edge_length
from NMM.base.VTKBase.is_empty_cell import is_empty_cell_id
from NMM.base.VTKBase.generate_line import generate_line
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_point import insert_a_point
import numpy as np


class CrackTipSubdivision(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid):
        self.__crack_tip = crack_tip

    def update(self, *args, **kwargs):
        crack_tip = self.__crack_tip
        crack_tip_grid = self.__crack_tip.value

        crack_tip_max = global_variable_cache.get_item('crack_tip_max')
        crack_tip_min = global_variable_cache.get_item('crack_tip_min')

        for each_id in range(crack_tip.get_cell_number()):
            if is_empty_cell_id(vtk_model=crack_tip_grid, cell_id=each_id):
                continue

            if crack_tip.get_cell_attribute('line_on_shell', each_id)[0] == 1:
                continue
            crack_tip_length = get_edge_length(vtk_model=crack_tip_grid, cell_id=each_id)
            if crack_tip_length > crack_tip_max:

                number = crack_tip.get_cell_number()
                point_id = crack_tip.get_cell_point_id(each_id)
                point_number = crack_tip.get_point_number()

                coordinate_0 = crack_tip.get_point_coordinate(point_id[0])
                coordinate_1 = crack_tip.get_point_coordinate(point_id[1])

                coordinate = (np.array(coordinate_0, dtype=np.float64) + np.array(coordinate_1, dtype=np.float64)) / 2

                crack_tip.delete_cell(each_id)

                crack_tip.insert_a_point(coordinate)
                crack_tip.set_point_attribute('point_id', point_number, point_number)
                crack_tip.set_point_attribute('crack_point_type', point_number, 0)
                crack_tip.set_point_attribute('point_on_shell', point_number, 0)

                direction_0 = crack_tip.get_point_attribute('propagate_direction', point_id[0])
                direction_1 = crack_tip.get_point_attribute('propagate_direction', point_id[1])

                direction = [(direction_0[i] + direction_1[i]) / 2 for i in range(3)]
                crack_tip.set_point_attribute('propagate_direction', point_number, direction)
                crack_tip.set_point_attribute('propagate_vector', point_number, direction)

                crack_tip.insert_a_line_with_point_id(point_id[0], point_number)
                crack_tip.set_cell_attribute('cell_id', number, number)
                crack_tip.set_cell_attribute('line_on_shell', number, 0)

                crack_tip.insert_a_line_with_point_id(point_number, point_id[1])
                crack_tip.set_cell_attribute('cell_id', number + 1, number + 1)
                crack_tip.set_cell_attribute('line_on_shell', number + 1, 0)

                # print(crack_tip.get_point_cell_id(point_id[0]))
                # print(crack_tip.get_point_cell_id(point_id[1]))
                # print(crack_tip.get_point_cell_id(point_number))


