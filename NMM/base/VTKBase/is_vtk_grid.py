from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid


def is_vtk_grid(value) -> bool:
    if type(value) == vtkUnstructuredGrid:
        return True
    else:
        return False
