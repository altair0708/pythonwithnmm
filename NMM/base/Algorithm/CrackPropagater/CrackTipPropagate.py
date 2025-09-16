from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.VTKBase.crack_propagate.update_crack_tip import update_crack_tip


class CrackTipPropagate(AbstractAlgorithm):
    def __init__(self, crack_tip: VtkGrid):
        self.__crack_tip = crack_tip

    def update(self, *args, **kwargs):
        crack_tip = self.__crack_tip
        propagate_vector = []
        for each_id in range(crack_tip.get_point_number()):
            vector = crack_tip.get_point_attribute('propagate_vector', each_id)
            propagate_vector.append(vector)

        new_crack_tip = update_crack_tip(crack_tip.value, propagate_vector)
        crack_tip.value = new_crack_tip
