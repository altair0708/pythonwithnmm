from NMM.base.Property.Property import Property
from NMM.base.VTKBase import load_toml_file
from typing import Dict


class PropertyMap(Property):
    @classmethod
    def generate_from_toml(cls, file_path: str, map_name: str = None):
        new_toml_map = cls(load_toml_file(file_path, map_name))
        if map_name is not None:
            new_toml_map.name = map_name
        else:
            new_toml_map.name = new_toml_map.value['name']
        return new_toml_map

    def __init__(self, value: Dict):
        super(PropertyMap, self).__init__()
        self._type = 'PropertyMap'
        self._name = ''
        self._value = value

    def __getitem__(self, item):
        return self.value.get(item, f'Key not exist!!!: {item}')

    def __setitem__(self, key, value):
        self.value[key] = value
