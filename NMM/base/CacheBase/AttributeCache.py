from NMM.base.CacheBase.CacheInterface import AbstractCache


class AttributeCache(AbstractCache):
    def __init__(self):
        super(AttributeCache, self).__init__()

    def add_item(self, grid_name: str, attribute_name: str, attribute_id: int, value):
        self._cache_list.append({'grid_name': grid_name, 'attribute_name': attribute_name, 'attribute_id': attribute_id, 'value': value})
        self.insert()


attribute_cache = AttributeCache()
