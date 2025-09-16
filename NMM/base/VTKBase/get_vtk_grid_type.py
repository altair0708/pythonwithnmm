from vtkmodules.vtkCommonDataModel import vtkDataSet


def get_vtk_grid_type(vtk_model: vtkDataSet):
    class_name = vtk_model.GetClassName()
    return class_name



