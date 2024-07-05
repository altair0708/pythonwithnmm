from queue import Queue
from NMM.base.CacheBase.CacheInterface import AbstractCache


class RelationshipCache(AbstractCache):
    def __init__(self):
        super(RelationshipCache, self).__init__()

    def __len__(self):
        return len(self._cache_list)

    def __iter__(self):
        return iter(self._cache_list)

    def add_item(self, name_0: str, id_0: int, name_1: str, id_1: int):
        self._cache_list.append({name_0: id_0, name_1: id_1})


relationship_cache = RelationshipCache()
