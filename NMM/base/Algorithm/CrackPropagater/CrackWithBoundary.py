from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.crack_propagate.generate_crack_quad import generate_crack_polygon
from NMM.base.VTKBase.insert_a_vtk_cell.insert_a_vtk_cell_0 import insert_a_vtk_cell
from NMM.base.VTKBase.crack_propagate.intersection_with_shell import intersection_with_shell
import numpy as np


class CrackWithBoundary(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid, geometric_shell: VtkGrid):
        self.__crack_tip = crack_tip
        self.__geometric_shell = geometric_shell

    def update(self, *args, **kwargs):
        crack_tip = self.__crack_tip
        geometric_shell = self.__geometric_shell

        for each_id in range(crack_tip.get_point_number()):
            if crack_tip.get_point_attribute('point_on_shell', each_id)[0] == 0:
                origin_coordinate = crack_tip.get_point_coordinate(each_id)
                propagate_vector = crack_tip.get_point_attribute('propagate_vector', each_id)
                propagate_coordinate = np.array(origin_coordinate, dtype=np.float64) + np.array(propagate_vector, dtype=np.float64)

                is_on_boundary, propagate_coordinate = intersection_with_shell(geometric_shell.value, origin_coordinate, propagate_coordinate)

                if is_on_boundary is True:
                    propagate_vector = np.array(propagate_coordinate, dtype=np.float64) - np.array(origin_coordinate, dtype=np.float64)
                    crack_tip.set_point_attribute('propagate_vector', each_id, propagate_vector)
                    # crack_tip.set_point_attribute('point_on_shell', each_id, 1)
