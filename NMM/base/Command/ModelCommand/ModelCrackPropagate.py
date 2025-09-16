from NMM.base.Command.CommandInterface import AbstractCommand
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Algorithm.CrackPropagater.CrackPropagateVector import CrackPropagateVector
from NMM.base.Algorithm.CrackPropagater.CrackQuad import CrackQuad
from NMM.base.Algorithm.CrackPropagater.CrackWithBoundary import CrackWithBoundary
from NMM.base.Algorithm.CrackPropagater.CrackTipPropagate import CrackTipPropagate
import numpy as np


class ModelCrackPropagate(AbstractCommand):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__crack_tip: VtkGrid = entrance_cache.get_item('crack_tip_VtkGrid')
        self.__crack_propagation: VtkGrid = entrance_cache.get_item('crack_propagation_VtkGrid')
        self.__geometric_shell: VtkGrid = entrance_cache.get_item('geometric_shell_VtkGrid')
        self.__geometric_tetrahedron: VtkGrid = entrance_cache.get_item('geometric_tetrahedron_VtkGrid')

    def execute(self):
        crack_tip = self.__crack_tip
        manifold_element = self.__manifold_element
        crack_propagation = self.__crack_propagation
        geometric_shell = self.__geometric_shell
        geometric_tetrahedron = self.__geometric_tetrahedron

        for each_point_id in range(crack_tip.get_point_number()):
            if crack_tip.get_point_attribute('point_on_shell', each_point_id)[0] == 0:
                algorithm = CrackPropagateVector(each_point_id, crack_tip, geometric_tetrahedron)
                algorithm.update()
                vector = algorithm.direction_vector
            else:
                vector = (0, 0, 0)

            if np.linalg.norm(np.array(vector)) != 0:
                crack_tip.set_point_attribute('propagate_direction', each_point_id, vector)
            crack_tip.set_point_attribute('propagate_vector', each_point_id, vector)

        algorithm = CrackWithBoundary(crack_tip, geometric_shell)
        algorithm.update()

        algorithm = CrackQuad(crack_tip, crack_propagation)
        algorithm.update()

        algorithm = CrackTipPropagate(crack_tip)
        algorithm.update()
