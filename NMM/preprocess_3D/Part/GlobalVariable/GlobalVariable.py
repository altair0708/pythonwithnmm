from NMM.base.Part.Part import Part
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
from typing import Dict


class GlobalVariable(Part):
    def __init__(self):
        super(GlobalVariable, self).__init__()
        self.name = 'global_variable'  # global_variable_Part

        global_variable_cache.add_observer(self)

    def get_variable(self, variable_name: str):
        global_variable = self.get_property('global_variable')  # global_variable_PropertyMap
        return global_variable[variable_name]

    def set_variable(self, variable_name: str, value):
        global_variable = self.get_property('global_variable')  # global_variable_PropertyMap
        global_variable[variable_name] = value

    # interface in global_variable_cache
    # temp_dict = {'variable_name': variable_name, 'variable_value': variable_value}
    def insert(self, modify_dict: Dict):
        variable_name = modify_dict['variable_name']
        value = modify_dict['variable_value']
        assert variable_name in self.get_property('global_variable').value
        self.set_variable(variable_name, value)

    # interface in global_variable_cache
    # temp_dict = {'variable_name': variable_name, 'variable_value': variable_value}
    def select(self, modify_dict: Dict, result_list):
        variable_name = modify_dict['variable_name']
        assert modify_dict['variable_value'] is None
        assert variable_name in self.get_property('global_variable').value
        value = self.get_property('global_variable')[variable_name]
        result_dict = {'variable_name': variable_name, 'variable_value': value}
        result_list.append(result_dict)
