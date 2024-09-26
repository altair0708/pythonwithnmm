from NMM.base.CacheBase.CacheInterface import AbstractCache
from NMM.base.Property.Implement.Relationship import Relationship


class RelationshipCache(AbstractCache):
    def __init__(self):
        super(RelationshipCache, self).__init__()

    def add_item(self, name_0: str, id_0: int, name_1: str, id_1: int):
        temp = Relationship(relationship_name=f'{name_0}_{name_1}', id_0=id_0, id_1=id_1)
        self._cache_list.append(temp)
        self.insert()

    def get_item(self, name_0: str, name_1: str, id_0: int = None, id_1: int = None):
        if id_0 is not None and id_1 is not None:
            raise Exception('Id value error!!!')
        elif id_0 is None and id_1 is None:
            raise Exception('Id value error!!!')
        temp = Relationship(relationship_name=f'{name_0}_{name_1}', id_0=id_0, id_1=id_1)
        self._cache_list.append(temp)
        return self.select()


relationship_cache = RelationshipCache()
