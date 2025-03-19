from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkPointData
from vtkmodules.vtkCommonCore import vtkDataArray


def copy_cell_data(origin_vtk_model: vtkUnstructuredGrid, target_vtk_model: vtkUnstructuredGrid, attribute_name: str):
    cell_data: vtkCellData = origin_vtk_model.GetCellData()
    data_array: vtkDataArray = cell_data.GetArray(attribute_name)
    print(type(data_array))

    # type() get the class of one object
    # new_data_array = type(data_array)()
    new_data_array = data_array.__class__()
    new_data_array.DeepCopy(data_array)

    target_cell_data = target_vtk_model.GetCellData()
    target_cell_data.AddArray(new_data_array)
