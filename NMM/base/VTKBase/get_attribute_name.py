from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkPointData


def get_cell_attribute_name(vtk_model: vtkUnstructuredGrid, attribute_id: int):
    cell_data = vtk_model.GetCellData()
    return cell_data.GetArrayName(attribute_id)


def get_point_attribute_name(vtk_model: vtkUnstructuredGrid, attribute_id: int):
    point_data = vtk_model.GetPointData()
    return point_data.GetArrayName(attribute_id)
