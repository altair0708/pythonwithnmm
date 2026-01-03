from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.CacheBase import entrance_cache, relationship_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class CoverEnrichment(AbstractAlgorithm):
    def __init__(self, manifold_element: VtkGrid, mathematics_point: VtkGrid):
        self.__manifold_element = manifold_element
        self.__mathematics_point = mathematics_point

    def update(self, *args, **kwargs):
        manifold_element = self.__manifold_element
        mathematics_point = self.__mathematics_point

        def get_crack_tip_element_id(element_id: int):
            return manifold_element.get_cell_attribute('cracked', element_id)[0] == 7
        crack_tip_element_id_list = list(filter(get_crack_tip_element_id, range(manifold_element.get_cell_number())))

        id_set = set()
        for each_element_id in crack_tip_element_id_list:
            relationship_list = relationship_cache.get_item(name_0='cover', name_1='element', id_0=None, id_1=each_element_id)
            [id_set.add(each['cover']) for each in relationship_list]

        for each_cover_id in range(mathematics_point.get_cell_number()):
            if each_cover_id in id_set:
                mathematics_point.set_cell_attribute('enrichment', each_cover_id, 1)
            else:
                mathematics_point.set_cell_attribute('enrichment', each_cover_id, 0)

        print(f'cover_id: {id_set}')
