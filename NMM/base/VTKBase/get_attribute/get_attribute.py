# Entrance of the function
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkPointData
from vtkmodules.vtkCommonCore import vtkDataArray
from NMM.base.VTKBase.get_attribute.get_cover_element_id import get_cover_element_relationship


def get_attribute(vtk_model: vtkUnstructuredGrid, attribute_name: str, id_value: int):
    property_value = None
    property_cell_data: vtkCellData = vtk_model.GetCellData()
    number = property_cell_data.GetNumberOfArrays()
    flag = False
    for property_id in range(number):
        if property_cell_data.GetArrayName(property_id) == attribute_name:
            property_data: vtkDataArray = property_cell_data.GetArray(property_id)
            property_value = property_data.GetTuple(id_value)
            flag = True

    property_point_data: vtkPointData = vtk_model.GetPointData()
    number = property_point_data.GetNumberOfArrays()
    for property_id in range(number):
        if property_point_data.GetArrayName(property_id) == attribute_name:
            property_data: vtkDataArray = property_point_data.GetArray(property_id)
            property_value = property_data.GetTuple(id_value)
            flag = True

    if not flag:
        raise Exception('Attribute name error!!!')

    return property_value
