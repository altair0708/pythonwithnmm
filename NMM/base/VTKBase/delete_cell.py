from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def delete_vtk_cell(vtk_model: vtkUnstructuredGrid, id_value: int):
    # set to empty cell
    vtk_model.GetCellTypesArray().SetValue(id_value, 0)
