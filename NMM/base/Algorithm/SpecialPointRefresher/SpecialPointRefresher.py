from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.Property.Implement.VtkGrid import VtkGrid
from NMM.base.Algorithm.SpecialPointRefresher.GenerlRefresher import GeneralRefresher
from NMM.base.CacheBase import relationship_cache
from NMM.base.Property.Implement.Relationship import Relationship


class SpecialPointRefresher(AbstractAlgorithm):
    def __init__(self, mathematics_point: VtkGrid, special_point: VtkGrid):
        self.__mathematics_point = mathematics_point
        self.__special_point = special_point

    def update(self, *args, **kwargs):
        for each_id in range(self.__special_point.get_cell_number()):
            element_special_relationship_list = relationship_cache.get_item(name_0='element', name_1='specialpoint', id_0=None, id_1=each_id)
            if len(element_special_relationship_list) > 0:
                assert len(element_special_relationship_list) == 1
                element_id = element_special_relationship_list[0]['element']
                cover_element_relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None, id_1=element_id)
                relationship_list = [Relationship(relationship_name='cover_specialpoint', id_0=each_relationship['cover'], id_1=each_id) for each_relationship in cover_element_relationship_list]
                general_refresh = GeneralRefresher(each_id, self.__mathematics_point, self.__special_point, relationship_list)
                general_refresh.update()
