from NMM.base.Algorithm.ElementCreator.ElementCreatorInterface import AbstractElementCreator
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.preprocess_3D.Part.ElementList.MatrixElement.MatrixElementFactory import MatrixElementFactory
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from typing import List


class MatrixElementCreator(AbstractElementCreator):

    # For different types of element in the same module
    # design pattern: factory pattern
    @staticmethod
    def get_element_factory(crack_status):
        if crack_status == 0:
            element_factory = MatrixElementFactory()
            return element_factory

    def __init__(self):
        super(MatrixElementCreator, self).__init__()
        self.__element_id = -1
        self.__manifold_element = None
        self.__new_element = None

    def set_input_data(self, element_id: int, manifold_element: VtkGrid, new_element: VtkGrid):
        self.__element_id = element_id
        self.__manifold_element = manifold_element
        self.__new_element = new_element

    # TODO: create a matrix element
    def update(self, *args, **kwargs) -> List:
        crack_status = self.__manifold_element.get_attribute('cracked', self.__element_id)
        element_factory = MatrixElementCreator.get_element_factory(crack_status)
        return element_factory.build()
