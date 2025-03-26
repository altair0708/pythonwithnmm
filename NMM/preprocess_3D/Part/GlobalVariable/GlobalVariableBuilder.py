from NMM.base.CompositeObject.ConstructorInterface import AbstractConstructor
from NMM.base.CacheBase.EntranceCache import entrance_cache
from NMM.base.Property.Implement.PropertyMap import PropertyMap
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable


# TODO: Global variable
class GlobalVariableBuilder(AbstractConstructor):
    def build(self, *args, **kwargs):
        global_variable = GlobalVariable()
        global_variable_path = entrance_cache.get_item('global_variable_Path')
        global_variable_map = PropertyMap.generate_from_toml(global_variable_path.value)
        global_variable.add_property(global_variable_map)

        material_parameter_path = entrance_cache.get_item('material_parameter_Path')
        material_parameter_map = PropertyMap.generate_from_toml(material_parameter_path.value)
        global_variable.add_property(material_parameter_map)

        grid_attribute_path = entrance_cache.get_item('grid_attribute_Path')
        grid_attribute_map = PropertyMap.generate_from_toml(grid_attribute_path.value)
        global_variable.add_property(grid_attribute_map)

        return global_variable
