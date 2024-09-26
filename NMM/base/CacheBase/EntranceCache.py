from NMM.base.CacheBase.CacheInterface import AbstractCache


class EntranceCache(AbstractCache):
    def __init__(self):
        super(EntranceCache, self).__init__()
        self._cache_dict = {}

    def add_item(self, node_name: str, node_pointer):
        node_type = node_pointer.type
        item_name = f'{node_name}_{node_type}'
        if item_name in self._cache_dict:
            raise Exception(f'Node name exist: {item_name}!!!')
        self._cache_dict.update({item_name: node_pointer})
        self.insert()

    def get_item(self, node_name: str):
        return self._cache_dict[node_name]


entrance_cache = EntranceCache()

