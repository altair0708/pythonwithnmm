from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkPointData
from vtkmodules.vtkCommonCore import vtkDataArray


def get_point_coordinate(vtk_model: vtkUnstructuredGrid, point_id):

    point_data: vtkPointData = vtk_model.GetPointData()
    number = point_data.GetNumberOfArrays()
    for property_id in range(number):
        if point_data.GetArrayName(property_id) == 'point_id':
            property_data: vtkDataArray = point_data.GetArray(property_id)
            property_value = property_data.GetTuple(point_id)
            attribute_point_id = int(property_value[0])
            assert attribute_point_id == point_id

    return vtk_model.GetPoint(point_id)
