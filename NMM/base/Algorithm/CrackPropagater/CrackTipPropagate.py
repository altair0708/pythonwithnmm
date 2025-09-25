from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Algorithm.CrackPropagater.CrackTipSubdivision import CrackTipSubdivision
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.crack_propagate.update_crack_tip import update_crack_tip
from NMM.base.VTKBase.update_point_coordinate import update_point_coordinate
import numpy as np


class CrackTipPropagate(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid):
        self.__crack_tip = crack_tip

    def update(self, *args, **kwargs):
        crack_tip = self.__crack_tip
        # propagate_vector = []
        for each_id in range(crack_tip.get_point_number()):
            vector = crack_tip.get_point_attribute('propagate_vector', each_id)
            coordinate = crack_tip.get_point_coordinate(each_id)
            coordinate = np.array(coordinate, dtype=np.float64) + np.array(vector, dtype=np.float64)
            update_point_coordinate(crack_tip.value, each_id, coordinate)

        # new_crack_tip = update_crack_tip(crack_tip.value, propagate_vector)
        # crack_tip.value = new_crack_tip

        # algorithm = CrackTipSubdivision(crack_tip)
        # algorithm.update()

