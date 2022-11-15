from vtkmodules.vtkCommonDataModel import (vtkUnstructuredGrid, vtkCellData, vtkPointData)
from vtkmodules.vtkCommonCore import vtkDataArray


def get_property(vtk_model: vtkUnstructuredGrid, property_name: str, temp_id: int):
    property_value = None
    property_cell_data: vtkCellData = vtk_model.GetCellData()
    number = property_cell_data.GetNumberOfArrays()
    for property_id in range(number):
        if property_cell_data.GetArrayName(property_id) == property_name:
            property_data: vtkDataArray = property_cell_data.GetArray(property_id)
            property_value = property_data.GetTuple(temp_id)

    property_point_data: vtkPointData = vtk_model.GetPointData()
    number = property_point_data.GetNumberOfArrays()
    for property_id in range(number):
        if property_point_data.GetArrayName(property_id) == property_name:
            property_data: vtkDataArray = property_point_data.GetArray(property_id)
            property_value = property_data.GetTuple(temp_id)

    return property_value


def set_property(vtk_model: vtkUnstructuredGrid, property_name: str, temp_id: int, value):
    property_cell_data: vtkCellData = vtk_model.GetCellData()
    number = property_cell_data.GetNumberOfArrays()
    flag = False
    for property_id in range(number):
        if property_cell_data.GetArrayName(property_id) == property_name:
            property_data: vtkDataArray = property_cell_data.GetArray(property_id)
            property_data.InsertTuple(temp_id, value)
            # try:
            #     property_data.SetTuple(temp_id, value)
            # except ValueError:
            #     property_data.InsertTuple(temp_id, value)
            flag = True

    property_point_data: vtkPointData = vtk_model.GetPointData()
    number = property_point_data.GetNumberOfArrays()
    for property_id in range(number):
        if property_point_data.GetArrayName(property_id) == property_name:
            property_data: vtkDataArray = property_point_data.GetArray(property_id)
            property_data.InsertTuple(temp_id, value)
            # try:
            #     property_data.SetTuple(temp_id, value)
            # except ValueError:
            #     property_data.InsertTuple(temp_id, value)
            flag = True
    if not flag:
        raise Exception('Can\'t find property, value not insert!!!')
