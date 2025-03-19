from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from NMM.base.VTKBase.add_attribute.add_point_attribute import AddPointAttribute
from NMM.base.VTKBase.add_attribute.add_cell_attribute import AddCellAttribute
from NMM.base.VTKBase.load_toml_file import load_toml_file
from NMM.base.CacheBase.EntranceCache import entrance_cache


def add_attribute(vtk_model: vtkUnstructuredGrid, attribute_name: str, attribute_toml: str = None):

    if attribute_toml is None:
        global_variable_path = entrance_cache.get_item('global_variable_Path')
        attribute_toml = global_variable_path.value

    attribute_map = load_toml_file(attribute_toml, 'attribute')

    tuple_dimensional = int(attribute_map[attribute_name]['tuple_dimensional'])
    is_id = attribute_map[attribute_name]['is_id']

    if attribute_map[attribute_name]['cell_point'] == 'cell':
        if attribute_map[attribute_name]['array_type'] == 'int':
            array_type = AddCellAttribute.add_int_array
        elif attribute_map[attribute_name]['array_type'] == 'float':
            array_type = AddCellAttribute.add_float_array
        else:
            raise Exception('Array type error!!!')
    elif attribute_map[attribute_name]['cell_point'] == 'point':
        if attribute_map[attribute_name]['array_type'] == 'int':
            array_type = AddPointAttribute.add_int_array
        elif attribute_map[attribute_name]['array_type'] == 'float':
            array_type = AddPointAttribute.add_float_array
        else:
            raise Exception('Array type error!!!')
    else:
        raise Exception('Data in cell or point???')

    array_type(vtk_model, attribute_name, tuple_dimensional, is_id)
