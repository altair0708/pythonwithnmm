from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from NMM.base.VTKBase.add_attribute.add_point_attribute import AddPointAttribute
from NMM.base.VTKBase.add_attribute.add_cell_attribute import AddCellAttribute


def add_attribute(vtk_model: vtkUnstructuredGrid, attribute_name: str):

    array_type = None
    tuple_dimensional = -1
    is_id = False

    if 'cell_id' == attribute_name:
        array_type = AddCellAttribute.add_int_array
        tuple_dimensional = 1
        is_id = True
    elif 'point_id' == attribute_name:
        array_type = AddPointAttribute.add_int_array
        tuple_dimensional = 1
        is_id = True
    elif 'math_cover_coordinate' == attribute_name:
        array_type = AddCellAttribute.add_float_array
        tuple_dimensional = 3
    elif 'math_cover_displacement' == attribute_name:
        array_type = AddCellAttribute.add_float_array
        tuple_dimensional = 3
    elif 'surface_id' == attribute_name:
        array_type = AddCellAttribute.add_int_array
        tuple_dimensional = 1
    else:
        raise Exception('Attribute name error!!!')

    array_type(vtk_model, attribute_name, tuple_dimensional, is_id)
