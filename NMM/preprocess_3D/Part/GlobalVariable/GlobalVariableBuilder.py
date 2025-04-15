from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable


class GlobalVariableBuilder(AbstractConstructor):
    def build(self, path: str = None):
        global_variable = GlobalVariable()
        if path is None:
            global_variable_path = entrance_cache.get_item('global_variable_Path').value
        else:
            global_variable_path = path + 'global_variable.toml'
        global_variable_map = PropertyMap.generate_from_toml(global_variable_path)
        global_variable.add_property(global_variable_map)

        if path is None:
            material_parameter_path = entrance_cache.get_item('material_parameter_Path').value
        else:
            material_parameter_path = path + 'material_parameter.toml'
        material_parameter_map = PropertyMap.generate_from_toml(material_parameter_path)
        global_variable.add_property(material_parameter_map)

        if path is None:
            grid_attribute_path = entrance_cache.get_item('grid_attribute_Path').value
        else:
            grid_attribute_path = path + 'grid_attribute.toml'
        grid_attribute_map = PropertyMap.generate_from_toml(grid_attribute_path)
        global_variable.add_property(grid_attribute_map)

        return global_variable
