from queue import Queue
from NMM.base.CacheBase.CacheInterface import AbstractCache
from NMM.base.Property.Implement.Relationship import Relationship


class RelationshipCache(AbstractCache):
    def __init__(self):
        super(RelationshipCache, self).__init__()

    def add_item(self, name_0: str, id_0: int, name_1: str, id_1: int):
        temp = Relationship(relationship_name=f'{name_0}_{name_1}', id_0=id_0, id_1=id_1)
        self._cache_list.append(temp)
        self.update()


relationship_cache = RelationshipCache()
