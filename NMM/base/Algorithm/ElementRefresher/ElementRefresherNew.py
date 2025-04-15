from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Algorithm.ElementRefresher.CompleteElementRefresher import CompleteElementRefresher
from NMM.base.Algorithm.ElementRefresher.SeparateElementRefresher import SeparateElementRefresher
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.CacheBase import relationship_cache


class ElementRefresher(AbstractAlgorithm):
    def __init__(self, mathematics_point: VtkGrid, manifold_element: VtkGrid, new_cover: VtkGrid, new_element: VtkGrid):
        self.__mathematics_point = mathematics_point
        self.__manifold_element = manifold_element
        self.__new_cover = new_cover
        self.__new_element = new_element

    def update(self, *args, **kwargs):
        for each_id in range(self.__manifold_element.get_cell_number()):
            relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None, id_1=each_id)
            complete_element_refresher = CompleteElementRefresher(each_id, self.__mathematics_point, self.__manifold_element, relationship_list)
            complete_element_refresher.update()

        for each_id in range(self.__new_element.get_cell_number()):
            relationship_list = relationship_cache.get_item(name_0='newcover', name_1='newelement', id_0=None, id_1=each_id)
            separate_element_refresher = SeparateElementRefresher(each_id, self.__new_cover, self.__new_element, relationship_list)
            separate_element_refresher.update()
