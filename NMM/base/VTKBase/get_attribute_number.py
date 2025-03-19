from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid, vtkCellData, vtkPointData


def get_cell_attribute_number(vtk_model: vtkUnstructuredGrid):
    cell_data: vtkCellData = vtk_model.GetCellData()
    return cell_data.GetNumberOfArrays()


def get_point_attribute_number(vtk_model: vtkUnstructuredGrid):
    point_data: vtkPointData = vtk_model.GetPointData()
    return point_data.GetNumberOfArrays()
