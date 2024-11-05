from NMM.base.Algorithm.ElementCreator.ElementCreatorInterface import AbstractElementCreator
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Property.Implement.MatrixElement.MatrixElement import MatrixElement
from NMM.base.Property.Implement.MatrixElement.MatrixSeparateElement import MatrixSeparateElement
from typing import List


class MatrixElementCreator(AbstractElementCreator):
    def __init__(self):
        pass

    def set_input_data(self, element_id: int, manifold_element: VtkGrid, new_element: VtkGrid):
        pass

    # TODO: create a matrix element
    def update(self, *args, **kwargs) -> List:
        pass
