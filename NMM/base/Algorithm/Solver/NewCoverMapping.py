from NMM.base.Algorithm.AlgorithmInterface import AbstractAlgorithm
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.CacheBase.RelationshipCache import relationship_cache
from NMM.base.Property.Implement.VtkGrid import VtkGrid


class NewCoverMapping(AbstractAlgorithm):
    def __init__(self):
        self.__manifold_element: VtkGrid = entrance_cache.get_item('manifold_element_VtkGrid')
        self.__new_element: VtkGrid = entrance_cache.get_item('new_element_VtkGrid')
        self.__mathematics_point: VtkGrid = entrance_cache.get_item('mathematics_point_VtkGrid')
        self.__new_cover: VtkGrid = entrance_cache.get_item('new_cover_VtkGrid')

        self.__new_cover_map = {}

    def update(self, *args, **kwargs):
        new_cover = self.__new_cover
        mathematics_point = self.__mathematics_point
        cover_id = list(range(mathematics_point.get_cell_number()))
        crack_cover_id = filter(lambda x: mathematics_point.get_cell_attribute('cracked', x)[0] == 9, cover_id)

        new_cover_map = {}
        for each_id in crack_cover_id:
            temp = relationship_cache.get_item('cover', 'newcover', id_0=each_id, id_1=None)
            assert len(temp) == 2
            new_cover_list = [int(x['newcover']) for x in temp]
            real_id = list(filter(lambda x: new_cover.get_cell_attribute('real', x)[0] == 1, new_cover_list))
            virtual_id = list(filter(lambda x: new_cover.get_cell_attribute('real', x)[0] == 0, new_cover_list))
            assert len(real_id) == 1 and len(virtual_id) == 1

            real_id = real_id[0]
            real_id = int(new_cover.get_cell_attribute('total_id', real_id)[0])

            virtual_id = virtual_id[0]
            virtual_id = int(new_cover.get_cell_attribute('total_id', virtual_id)[0])

            for x in range(3):
                new_cover_map[3 * virtual_id + x] = 3 * real_id + x

        self.__new_cover_map = new_cover_map

    @property
    def new_cover_map(self):
        return self.__new_cover_map
