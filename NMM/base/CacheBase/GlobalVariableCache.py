from NMM.base.CacheBase.CacheInterface import AbstractCache


class GlobalVariableCache(AbstractCache):
    def __init__(self):
        super(GlobalVariableCache, self).__init__()

    def get_item(self, variable_name: str):
        temp_dict = {'variable_name': variable_name, 'variable_value': None}
        self._cache_list.append(temp_dict)
        result_list = self.select()
        return result_list[0]['variable_value']

    def add_item(self, variable_name: str, value):
        temp_dict = {'variable_name': variable_name, 'variable_value': value}
        self._cache_list.append(temp_dict)
        self.insert()

global_variable_cache = GlobalVariableCache()
