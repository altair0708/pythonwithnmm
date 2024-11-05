from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from abc import abstractmethod


class AbstractElementCreator(AbstractAlgorithm):
    @abstractmethod
    def set_input_data(self, element_id: int, manifold_element: VtkGrid, new_element: VtkGrid):
        pass


