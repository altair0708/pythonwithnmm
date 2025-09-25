import sys

from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.check_line_on_shell import check_line_on_shell, is_point_on_surface
from NMM.base.VTKBase.build_vertex_connectivity import build_vertex_connectivity
from NMM.base.Algorithm.Debuger import Debuger


class CrackTipOnSurface(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid, geometric_shell: VtkGrid):
        super(CrackTipOnSurface, self).__init__()
        self.__crack_tip = crack_tip
        self.__geometric_shell = geometric_shell

    def update(self):
        # check crack tip on shell
        geometric_shell = self.__geometric_shell.value
        for each_id, each_line in enumerate(self.__crack_tip):
            if self.__crack_tip.is_empty_cell(each_id):
                continue
            if self.__crack_tip.get_cell_attribute('line_on_shell', each_id)[0] == 1:
                continue
            if check_line_on_shell(geometric_shell, each_line):
                self.__crack_tip.set_cell_attribute('line_on_shell', each_id, 1)

        # check crack point on shell
        for each_point_id in range(self.__crack_tip.get_point_number()):
            assert each_point_id == self.__crack_tip.get_point_attribute('point_id', each_point_id)[0]
            point_coordinate = self.__crack_tip.get_point_coordinate(each_point_id)

            if self.__crack_tip.get_point_attribute('point_on_shell', each_point_id)[0] == 1:
                continue
            if is_point_on_surface(point_coordinate, geometric_shell):
                self.__crack_tip.set_point_attribute('point_on_shell', each_point_id, 1)

        connectivity_dict = build_vertex_connectivity(self.__crack_tip.value)
        for point_id, neighbors in connectivity_dict.items():
            if self.__crack_tip.get_point_attribute('point_on_shell', point_id)[0] == 0:
                continue
            crack_point_type = self.__crack_tip.get_point_attribute('point_on_shell', neighbors[0])[0] + \
                               self.__crack_tip.get_point_attribute('point_on_shell', neighbors[1])[0]
            self.__crack_tip.set_point_attribute('crack_point_type', point_id, crack_point_type)
