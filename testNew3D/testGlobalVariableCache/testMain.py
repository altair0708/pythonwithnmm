from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariable import GlobalVariable
from NMM.preprocess_3D.Part.GlobalVariable.GlobalVariableBuilder import GlobalVariableBuilder
from NMM.base.CacheBase.GlobalVariableCache import global_variable_cache
import shutil

shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/global_variable.toml', 'global_variable.toml')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/grid_attribute.toml', 'grid_attribute.toml')
shutil.copy('/Users/suboyi/PycharmProjects/pythonwithnmm/example/example001/mesh/material_parameter.toml', 'material_parameter.toml')


def test_global_variable_cache():
    builder = GlobalVariableBuilder()
    global_variable = builder.build(path='./')

    print(global_variable_cache.get_item('time_increment'))
    print(global_variable_cache.get_item('time_step'))
    global_variable_cache.add_item('time_step', 10)
    print(global_variable_cache.get_item('time_step'))



